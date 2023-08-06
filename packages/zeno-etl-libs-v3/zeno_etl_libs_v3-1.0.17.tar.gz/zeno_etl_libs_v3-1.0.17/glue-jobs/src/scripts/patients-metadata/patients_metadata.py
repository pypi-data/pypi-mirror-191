#!/usr/bin/env python
# coding: utf-8
import argparse
import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
import numpy as np
import pandas as pd

# from memory_profiler import profile

status = {
    "updated": "updated",
    "pending": "pending",
    "updating": "updating",
}

patients_metadata_table = "patients-metadata-2"
bill_metadata_table = "bills-1-metadata"
schema = "prod2-generico"


def insert_new_patients(db):
    limit_str = f" limit {limit}; " if limit else ""
    query = f'''
        insert
            into
            "{schema}"."{patients_metadata_table}" (id,
            "created-at",
            "updated-at",
            "created-by",
            "etl-status"
            )
        select
            p.id,
            p."created-at",
            convert_timezone('Asia/Calcutta', GETDATE()),
            'etl-job',
            '{status['pending']}'
        from
            "{schema}"."patients" p
        inner join (
            select
                "patient-id"
            from
                "{schema}"."{bill_metadata_table}" bm
            group by
                "patient-id"
            ) bm1 on
            bm1."patient-id" = p.id
        left join "{schema}"."{patients_metadata_table}" pm on
            pm.id = p.id
        where
            pm.id is null
            -- and date(p."updated-at") between '2021-06-01' and '2021-11-30'
            and (pm."etl-status" != '{status['updated']}'
            or pm."etl-status" is null)
    {limit_str}
    '''
    db.execute(query, params=None)


def mark_old_patients_pending(db):
    # mark old patients etl-status pending if they have transacted
    query = f"""
            update
                "{schema}"."{patients_metadata_table}" pm2
            set
                "etl-status" = '{status['pending']}',
                "updated-at" = convert_timezone('Asia/Calcutta', GETDATE())
            from
                (
                select
                    pm.id
                from
                    "{schema}"."{patients_metadata_table}" pm
                inner join
                    "{schema}"."{bill_metadata_table}" bm on
                    pm.id = bm."patient-id"
                where
                    pm."updated-at" < bm."updated-at" ) ab
            where 
                pm2.id = ab.id;
        """
    db.execute(query, params=None)

    """ Sometimes jobs fails and updating count keeps increasing and we always get memory error, so to fix this mark 
     all updating status to pending """
    query = f"""
    update
        "{schema}"."{patients_metadata_table}"
    set
        "etl-status" = 'pending'
    where
        "etl-status" = 'updating'
    """
    db.execute(query, params=None)


def mark_pending_patients_updating(db):
    limit_str = f"limit {batch_size} " if batch_size else ""

    query = f"""
        update
            "{schema}"."{patients_metadata_table}" pm2
        set
            "etl-status" = '{status['updating']}'
        from
            (
            select
                pm.id
            from
                "{schema}"."{patients_metadata_table}" pm
            where
                "etl-status" = '{status['pending']}'
            {limit_str}
            ) ab
        where 
            pm2.id = ab.id;
    """
    db.execute(query, params=None)


def get_to_be_updated_patients(db):
    # ## Considering only changed patients
    query = f'''
     select
        id,
        "created-at",
        "updated-at",
        "created-by",
        "etl-status"
    from
        "{schema}"."{patients_metadata_table}" pm
    where
        "etl-status" = '{status['updating']}'
    '''
    db.execute(query, params=None)
    _changed_patients: pd.DataFrame = db.cursor.fetch_dataframe()
    return _changed_patients


def update_bill_agg_fields(db):
    query = f"""
        update
            "{schema}"."{patients_metadata_table}" t
        set
            -- "first-bill-date" = s."first-bill-date",
            "last-bill-date" = s."last-bill-date",
            -- "first-bill-id" = s."first-bill-id",
            "last-bill-id" = s."last-bill-id",
            "average-bill-value" = s."average-bill-value",
            "total-quantity" = s."total-quantity",
            "quantity-generic" = s."quantity-generic",
            "quantity-chronic" = s."quantity-chronic",
            "quantity-ethical" = s."quantity-ethical",
            "quantity-rx" = s."quantity-rx",
            "quantity-repeatable" = s."quantity-repeatable",
            "quantity-goodaid" = s."quantity-goodaid",
            "quantity-others-type" = s."quantity-others-type",
            "number-of-bills" = s."number-of-bills",
            "hd-bills" = s."hd-bills",
            "is-repeatable" = s."is-repeatable",
            "is-generic" = s."is-generic",
            "is-chronic" = s."is-chronic",
            "is-goodaid" = s."is-goodaid",
            "is-ethical" = s."is-ethical",
            "is-rx" = s."is-rx",
            "is-others-type" = s."is-others-type",
            "hd-flag" = s."hd-flag",
            "ecom-flag" = s."ecom-flag",
            "crm-flag" = s."crm-flag",
            "pr-flag" = s."pr-flag",
            "total-spend" = s."total-spend",
            "spend-generic" = s."spend-generic",
            "promo-min-bill-date" = s."promo-min-bill-date",
            "hd-min-bill-date" = s."hd-min-bill-date",
            "ecom-min-bill-date" = s."ecom-min-bill-date",
            "pr-min-bill-date" = s."pr-min-bill-date",
            "generic-min-bill-date" = s."generic-min-bill-date",
            "goodaid-min-bill-date" = s."goodaid-min-bill-date",
            "ethical-min-bill-date" = s."ethical-min-bill-date",
            "chronic-min-bill-date" = s."chronic-min-bill-date",
            "repeatable-min-bill-date" = s."repeatable-min-bill-date",
            "others-type-min-bill-date" = s."others-type-min-bill-date",
            "digital-payment-min-bill-date" = s."digital-payment-min-bill-date",
            "rx-min-bill-date" = s."rx-min-bill-date",
            "digital-payment-flag" = s."digital-payment-flag",
            "total-mrp-value" = s."total-mrp-value",
            "recency-customer-days" = s."recency-customer-days",
            "system-age-days" = s."system-age-days",
            "quantity-generic-pc" = s."quantity-generic-pc",
            "quantity-chronic-pc" = s."quantity-chronic-pc",
            "quantity-ethical-pc" = s."quantity-ethical-pc",
            "quantity-repeatable-pc" = s."quantity-repeatable-pc",
            "quantity-goodaid-pc" = s."quantity-goodaid-pc",
            "quantity-others-type-pc" = s."quantity-others-type-pc",
            "spend-generic-pc" = s."spend-generic-pc"
        from
            (
            select
                pm.id ,
                -- min(bm."created-at") as "first-bill-date",
                max(bm."created-at") as "last-bill-date",
                -- min(bm.id) as "first-bill-id",
                max(bm.id) as "last-bill-id",
                round(sum(bm."total-spend")/ count(distinct bm.id), 4) as "average-bill-value",
                sum(bm."total-quantity") as "total-quantity",
                sum(bm."quantity-generic") as "quantity-generic",
                case when sum(bm."total-quantity") in (0, null) then -1 else round(100.0 * sum(bm."quantity-generic")/ 
                sum(bm."total-quantity"), 4) end as "quantity-generic-pc",
                sum(bm."quantity-chronic") as "quantity-chronic",
                case when sum(bm."total-quantity") in (0, null) then -1 else round(100.0 * sum(bm."quantity-chronic")/ 
                sum(bm."total-quantity"), 4) end as "quantity-chronic-pc",
                sum(bm."quantity-ethical") as "quantity-ethical",
                case when sum(bm."total-quantity") in (0, null) then -1 else round(100.0 * sum(bm."quantity-ethical")/ 
                sum(bm."total-quantity"), 4) end as "quantity-ethical-pc",
                sum(bm."quantity-repeatable") as "quantity-repeatable",
                case when sum(bm."total-quantity") in (0, null) then -1 else round(100.0 * sum(bm."quantity-repeatable")
                / sum(bm."total-quantity"), 4) end as "quantity-repeatable-pc",
                sum(bm."quantity-goodaid") as "quantity-goodaid",
                case when sum(bm."total-quantity") in (0, null) then -1 else round(100.0 * sum(bm."quantity-goodaid")/ 
                sum(bm."total-quantity"), 4) end as "quantity-goodaid-pc",
                sum(bm."quantity-others-type") as "quantity-others-type",
                case when sum(bm."total-quantity") in (0, null) then -1 else round(100.0 * 
                sum(bm."quantity-others-type")/ sum(bm."total-quantity"), 4) end as "quantity-others-type-pc",
                sum(bm."quantity-generic" + bm."quantity-ethical") as "quantity-rx",
                case when sum(bm."total-quantity") in (0, null) then -1 else round(100.0 * sum(bm."quantity-generic" + 
                bm."quantity-ethical")/ sum(bm."total-quantity"), 4) end as "quantity-rx-pc",
                count(distinct bm.id) as "number-of-bills",
                count(distinct (case when bm."hd-flag" is true then bm.id else null end)) as "hd-bills",
                case when count(distinct bm.id) in (0, null) then -1 else round(100.0 * count(distinct (case when 
                bm."hd-flag" is true then bm.id else null end))/ count(distinct bm.id), 4) end  as "hd-bills-pc",
                bool_or(bm."is-repeatable") as "is-repeatable",
                bool_or(bm."is-generic") as "is-generic",
                bool_or(bm."is-chronic") as "is-chronic",
                bool_or(bm."is-goodaid") as "is-goodaid",
                bool_or(bm."is-ethical") as "is-ethical",
                bool_or(bm."is-rx") as "is-rx",
                bool_or(bm."is-others-type") as "is-others-type",
                bool_or(bm."hd-flag") as "hd-flag",
                bool_or(bm."ecom-flag") as "ecom-flag",
                bool_or(bm."crm-flag") as "crm-flag",
                bool_or(bm."pr-flag") as "pr-flag",
                bool_or(bm."digital-payment-flag") as "digital-payment-flag",
                sum(bm."total-spend") as "total-spend",
                sum(bm."spend-generic") as "spend-generic",
                case when sum(bm."total-spend") in (0, null) then -1 else round(100.0 * sum(bm."spend-generic")/ 
                sum(bm."total-spend")) end as "spend-generic-pc",
                min(case when bm."promo-code-id" is not null then bm."created-at" else null end) as 
                "promo-min-bill-date",
                min(case when bm."hd-flag" is true then bm."created-at" else null end) as "hd-min-bill-date",
                min(case when bm."ecom-flag" is true then bm."created-at" else null end) as "ecom-min-bill-date",
                min(case when bm."crm-flag" is true then bm."created-at" else null end) as "crm-min-bill-date",
                min(case when bm."pr-flag" is true then bm."created-at" else null end) as "pr-min-bill-date",
                min(case when bm."is-generic" is true then bm."created-at" else null end) as "generic-min-bill-date",
                min(case when bm."is-goodaid" is true then bm."created-at" else null end) as "goodaid-min-bill-date",
                min(case when bm."is-ethical" is true then bm."created-at" else null end) as "ethical-min-bill-date",
                min(case when bm."is-chronic" is true then bm."created-at" else null end) as "chronic-min-bill-date",
                min(case when bm."is-repeatable" is true then bm."created-at" else null end) as 
                "repeatable-min-bill-date",
                min(case when bm."is-others-type" is true then bm."created-at" else null end) as 
                "others-type-min-bill-date",
                min(case when bm."digital-payment-flag" is true then bm."created-at" else null end) as 
                "digital-payment-min-bill-date",
                min(case when bm."is-rx" is true then bm."created-at" else null end) as "rx-min-bill-date",
                sum(bm."total-mrp-value") as "total-mrp-value",
                case
                    when max(bm."created-at") = '0101-01-01' then null
                    else datediff(day,
                    max(bm."created-at"),
                    current_date)
                end as "recency-customer-days",
                case
                    when min(bm."created-at") = '0101-01-01' then null
                    else datediff(day,
                    min(bm."created-at"),
                    current_date)
                end as "system-age-days"
            from
                "{schema}"."{patients_metadata_table}" pm
            inner join "{schema}"."{bill_metadata_table}" bm on
                pm.id = bm."patient-id"
            where
                pm."etl-status" = '{status['updating']}'
            group by
                pm.id
        ) s
        where
            t.id = s.id;
    """
    db.execute(query, params=None)


def update_diagnostic_customer(db):
    query = f"""
        update
            "{schema}"."{patients_metadata_table}" t
        set
            "is-diagnostic-customer" = 1
        from
            (
            select
                r."patient-id"
            from
                "{schema}"."{patients_metadata_table}" pm
            inner join "{schema}"."redemption" r on
                pm.id = r."patient-id"
            where
                r.status in ('REDEMPTION', 'COMPLETED')
                and
                pm."etl-status" = '{status['updating']}'
                and
                (pm."is-diagnostic-customer" != 1 or pm."is-diagnostic-customer" is NULL)
            group by
                r."patient-id"
        ) s
        where
            t.id = s."patient-id";
    """
    db.execute(query, params=None)


def get_customer_feedback(db):
    # get customer feedback data (nps)
    query = f"""
        select
            p.id,
            f.rating,
            f.suggestion,
            f."store-id",
            s."name" as "store-name",
            f."created-at"
        from
            "{schema}"."{patients_metadata_table}" pm
        inner join "{schema}".patients p on
             p.id = pm.id
        inner join "{schema}".feedback f on
            f.phone = p.phone
        inner join "{schema}".stores s on
            f."store-id" = s."id"
        where pm."etl-status" = '{status['updating']}'
    """
    db.execute(query, params=None)
    nps: pd.DataFrame = db.cursor.fetch_dataframe()

    if not isinstance(nps, type(None)) and len(nps):
        nps.head(2)
        nps['created-at'] = pd.to_datetime(nps['created-at'])
        nps['nps-rating-date'] = nps['created-at'].dt.strftime("%Y-%m-%d")
        nps['is-nps'] = True
        nps = nps.sort_values(by=['id', 'created-at'], ascending=[True, False])

        # Keep only latest entry
        nps['rank'] = nps.groupby(['id']).cumcount() + 1
        nps = nps[nps['rank'] == 1]
        nps.drop('rank', axis='columns', inplace=True)
        nps = nps.rename(
            columns={
                'rating': 'latest-nps-rating',
                'suggestion': 'latest-nps-rating-comment',
                'nps-rating-date': 'latest-nps-rating-date',
                'store-id': 'latest-nps-rating-store-id',
                'store-name': 'latest-nps-rating-store-name'
            }
        )
    else:
        nps = pd.DataFrame(
            columns=['id', 'created-at', 'nps-rating-date', 'is-nps', 'latest-nps-rating',
                     'latest-nps-rating-comment',
                     'latest-nps-rating-date', 'latest-nps-rating-store-id',
                     'latest-nps-rating-store-name'])

    return nps


def get_referral_count(db):
    # Referral count
    query = f"""
        select
            a."patient-id" as id,
            SUM(b."total-used") as "referred-count"
        from
            "{schema}"."{patients_metadata_table}" pm
        left join 
            "{schema}"."patients-promo-codes" a on
            pm.id = a."patient-id"
        left join "{schema}"."promo-codes" b on
            a."promo-code-id" = b."id"
        where
            b."code-type" = 'referral'
            and pm."etl-status" = '{status['updating']}'
        group by
            a."patient-id"
    """
    db.execute(query=query)
    _referral: pd.DataFrame = db.cursor.fetch_dataframe()
    return _referral


def get_patient_bills(db):
    # ## Primary Store, System Age Days and Recency Customer Days
    query = f"""
        select
            pm.id,
            bm."store-id",
            bm.id as "bill-id",
            bm."bill-year",
            bm."bill-month",
            bm."bill-date",
            bm."created-at",
            bm."total-spend"
        from
            "{schema}"."{patients_metadata_table}" pm
        inner join 
            "{schema}"."{bill_metadata_table}" bm on
            pm.id = bm."patient-id"
        where
            pm."etl-status" = '{status['updating']}'
    """
    db.execute(query=query)
    _patient_bills: pd.DataFrame = db.cursor.fetch_dataframe()
    return _patient_bills


def get_patient_drugs(db):
    # ## Number of drug and primary disease
    query = f"""
        select
            b."patient-id" ,
            b.id as "bill-id",
            bi."inventory-id",
            i."drug-id"
        from
            "{schema}"."{patients_metadata_table}" pm
        inner join "{schema}"."bills-1" b on
            pm.id = b."patient-id"
        inner join "{schema}"."bill-items-1" bi on
            b.id = bi."bill-id"
        inner join "{schema}"."inventory-1" i on
            bi."inventory-id" = i.id
        inner join "{schema}".drugs d on
            i."drug-id" = d.id
        where
            pm."etl-status" = '{status['updating']}';
    """
    db.execute(query=query)
    _patient_drugs: pd.DataFrame = db.cursor.fetch_dataframe()

    return _patient_drugs


def get_drug_subgroup(db):
    # primary disease calculation
    query = f"""
    select
        a."id" as "drug-id",
        c."subgroup"
    from
        "{schema}".drugs a
    inner join "{schema}"."composition-master-molecules-master-mapping" b on
        a."composition-master-id" = b."composition-master-id"
    inner join "{schema}"."molecule-master" c on
        b."molecule-master-id" = c."id"
    group by
        a."id",
        c."subgroup"
    """

    db.execute(query=query)
    _drug_subgroup: pd.DataFrame = db.cursor.fetch_dataframe()

    return _drug_subgroup


def get_referral_code(db):
    # Get referral code for patient
    query = f"""
                SELECT
                    "patient-id" as "id",
                    "promo-code" as "referral-code"
                FROM
                (
                    SELECT
                        ppc."patient-id",
                        row_number() over (partition by ppc."patient-id" order by ppc."id" ASC) as rank_entry,
                        pc."promo-code"
                    FROM
                        "{schema}"."patients-promo-codes" ppc
                    INNER JOIN 
                        "{schema}"."promo-codes" pc 
                    ON
                        ppc."promo-code-id" = pc."id"
                    WHERE
                        pc."code-type" = 'referral') sub
                left join
                    "{schema}"."{patients_metadata_table}" pm 
                    on 
                    pm.id = sub."patient-id"
                where
                    sub.rank_entry = 1
                    and
                    pm."etl-status" = '{status['updating']}'"""
    db.execute(query=query)
    referral_code: pd.DataFrame = db.cursor.fetch_dataframe()
    return referral_code


def get_value_segment_anytime(db):
    q1 = f"""
            select
                value."patient-id" as "patient-id",
                value."value-segment" as "value-segment"
            from
                "{schema}"."customer-value-segment" value
                left join 
                "{schema}"."{patients_metadata_table}" pm 
                on
                pm.id = value."patient-id"
            where 
                pm."etl-status" = '{status['updating']}'
            group by
                value."patient-id",
                value."value-segment"
        """
    data_vs = db.get_df(q1)
    data_vs.columns = [c.replace('-', '_') for c in data_vs.columns]
    data_vs['value_segment_rank'] = data_vs['value_segment'].map(
        {'platinum': 3, 'gold': 2, 'silver': 1, 'others': 0})
    data_vs = data_vs.sort_values(by=['patient_id', 'value_segment_rank'], ascending=[True, False])
    data_vs['rank'] = data_vs.groupby(['patient_id']).cumcount() + 1
    data_vs_r1 = data_vs[data_vs['rank'] == 1]
    data_vs_f = data_vs_r1[['patient_id', 'value_segment']]
    data_vs_f.columns = ['id', 'value-segment-anytime']
    return data_vs_f


def get_behaviour_segment_anytime(db):
    q1 = f"""
            select
                behaviour."patient-id" as "patient-id",
                behaviour."behaviour-segment" as "behaviour-segment" 
            from
                "{schema}"."customer-behaviour-segment" behaviour
                left join 
                "{schema}"."{patients_metadata_table}" pm 
                on
                pm.id = behaviour."patient-id"
            where 
                pm."etl-status" = '{status['updating']}'
            group by
                behaviour."patient-id",
                behaviour."behaviour-segment"
        """

    data_bs = db.get_df(q1)
    data_bs.columns = [c.replace('-', '_') for c in data_bs.columns]

    data_bs['behaviour_segment_rank'] = data_bs['behaviour_segment'].map({'super': 7,
                                                                          'regular': 6,
                                                                          'generic_heavy': 5,
                                                                          'ethical_heavy': 4,
                                                                          'other_type': 3,
                                                                          'singletripper': 2,
                                                                          'newcomer_repeat': 1,
                                                                          'newcomer_singletripper': 0
                                                                          })
    data_bs = data_bs.sort_values(by=['patient_id', 'behaviour_segment_rank'],
                                  ascending=[True, False])

    data_bs['rank'] = data_bs.groupby(['patient_id']).cumcount() + 1

    data_bs_r1 = data_bs[data_bs['rank'] == 1]

    data_bs_f = data_bs_r1[['patient_id', 'behaviour_segment']]
    data_bs_f.columns = ['id', 'behaviour-segment-anytime']
    return data_bs_f


def update_data_in_patients_metadata_table(db, s3, patient_data):
    # ## Create temp table and update (nps and other) from that
    patient_temp_table = patients_metadata_table.replace("-", "_") + "_temp"
    db.execute(query=f"DROP table IF EXISTS {patient_temp_table};")
    query = f"""
        CREATE TEMP TABLE {patient_temp_table}
        (
            id INTEGER ENCODE az64
            ,"is-nps" bool
            ,"latest-nps-rating" INTEGER  ENCODE az64
            ,"latest-nps-rating-comment" VARCHAR(1500)   ENCODE lzo
            ,"latest-nps-rating-store-id" INTEGER ENCODE az64
            ,"latest-nps-rating-store-name" VARCHAR(765)   ENCODE lzo
            ,"latest-nps-rating-date" date  ENCODE az64
            ,"referred-count" int  ENCODE az64
            ,"primary-store-id" INTEGER ENCODE az64
            ,"num-drugs" INTEGER ENCODE az64
            ,"primary-disease" VARCHAR(100)   ENCODE lzo
            ,"avg-purchase-interval" numeric
            ,"std-purchase-interval" numeric
            -- ,"value-segment-calculation-date" date
            -- ,"value-segment" VARCHAR(50)
            ,"previous-bill-date" DATE   ENCODE az64
            ,"previous-store-id" INTEGER   ENCODE az64
            -- ,"min-bill-date-in-month" DATE   ENCODE az64
            -- ,"store-id-month" INTEGER   ENCODE az64
            ,"referral-code" VARCHAR(765) ENCODE lzo
            ,"value-segment-anytime" varchar(255) ENCODE lzo
            ,"behaviour-segment-anytime" varchar(255) ENCODE lzo
            ,"first-bill-date" timestamp   ENCODE az64
            ,"first-bill-id" INTEGER   ENCODE az64
            ,PRIMARY KEY (id)
        );
    """
    db.execute(query=query)
    patient_temp_table_info = helper.get_table_info(db=db, table_name=patient_temp_table,
                                                    schema=None)

    # ### Fixing the data types
    patient_data['latest-nps-rating'] = patient_data['latest-nps-rating'].fillna(-1).astype('int64')
    patient_data['latest-nps-rating-store-id'] = patient_data['latest-nps-rating-store-id'].fillna(
        -1).astype('int64')
    patient_data['referred-count'] = patient_data['referred-count'].fillna(-1).astype('int64')
    patient_data['num-drugs'] = patient_data['num-drugs'].fillna(-1).astype('int64')
    patient_data['previous-store-id'] = patient_data['previous-store-id'].fillna(-1).astype('int64')

    s3.write_df_to_db(
        df=patient_data[list(dict.fromkeys(patient_temp_table_info['column_name']))],
        db=db, table_name=patient_temp_table, schema=None
    )

    # ## Updating the data in patient-metadata-2 table
    query = f"""
        update
            "{schema}"."{patients_metadata_table}" t
        set
            "is-nps" = s."is-nps",
            "latest-nps-rating" = s."latest-nps-rating",
            "latest-nps-rating-comment" = s."latest-nps-rating-comment",
            "latest-nps-rating-store-id" = s."latest-nps-rating-store-id",
            "latest-nps-rating-store-name" = s."latest-nps-rating-store-name",
            "latest-nps-rating-date" = s."latest-nps-rating-date",
            "referred-count" = s."referred-count",
            "primary-store-id" = s."primary-store-id",
            "num-drugs" = s."num-drugs",
            "primary-disease" = s."primary-disease",
            "avg-purchase-interval" = s."avg-purchase-interval",
            "std-purchase-interval" = s."std-purchase-interval",
            -- "value-segment-calculation-date" = s."value-segment-calculation-date",
            -- "value-segment" = s."value-segment",
            "previous-bill-date" = s."previous-bill-date",
            "previous-store-id" = s."previous-store-id",
            -- "min-bill-date-in-month" = s."min-bill-date-in-month",
            -- "store-id-month" = s."store-id-month",
            "referral-code" = s."referral-code",
            "value-segment-anytime" = s."value-segment-anytime",
            "behaviour-segment-anytime" = s."behaviour-segment-anytime",
            "first-bill-date" = s."first-bill-date",
            "first-bill-id" = s."first-bill-id",
            "etl-status" = 'updated'
        from
             {patient_temp_table} s
        where
            t.id = s.id;
    """
    db.execute(query=query)


# @profile
def process_batch(changed_patients, db, s3, pg_db):
    """ updating some fields directly from bills-1-metadata table """
    update_bill_agg_fields(db=db)
    update_diagnostic_customer(db=db)
    nps = get_customer_feedback(db=db)
    referral = get_referral_count(db=db)
    patient_bills = get_patient_bills(db=db)
    referral_code = get_referral_code(db=db)
    value_segment_anytime = get_value_segment_anytime(db=db)
    behaviour_segment_anytime = get_behaviour_segment_anytime(db=db)

    # purchase interval calculation
    patient_bills_2 = patient_bills.sort_values(
        by=["id", "created-at"])  # soring on patient id and bill-created-at

    patient_bills_2['bill-date'] = patient_bills_2['bill-date'].apply(
        lambda x: x.strftime("%Y-%m-%d"))

    # Fetch previous bill date, against every bill
    patient_bills_2['previous-bill-date'] = patient_bills_2.groupby("id")['bill-date'].shift(1)

    patient_bills_2['purchase-interval'] = (
            pd.to_datetime(patient_bills_2['bill-date']) - pd.to_datetime(
        patient_bills_2['previous-bill-date'])).dt.days
    patient_bills_avg_std = patient_bills_2.groupby(['id']).agg(
        {'purchase-interval': ['mean', 'std']})
    patient_bills_avg_std = patient_bills_avg_std.reset_index(col_level=1)
    patient_bills_avg_std.columns = patient_bills_avg_std.columns.droplevel(0)
    patient_bills_avg_std.columns = ['id', 'avg-purchase-interval', 'std-purchase-interval']

    # ### Primary Store
    # Patient store wise, NOB and Total spend
    patient_store_agg = patient_bills.groupby(
        ['id', 'store-id']).agg({'bill-id': 'nunique', 'total-spend': 'sum'}).reset_index()
    patient_store_agg = patient_store_agg.rename(
        columns={'bill-id': 'store-bills', 'total-spend': 'store-spend'})
    patient_store_agg['rank'] = patient_store_agg.sort_values(
        ['store-bills', 'store-spend'], ascending=[False, False]).groupby(['id']).cumcount() + 1
    # Shortlist 1 store per patient
    patient_primary_store = patient_store_agg[patient_store_agg['rank'] == 1]
    patient_primary_store = patient_primary_store.rename(columns={'store-id': 'primary-store-id'})

    # ### Previous Bill Date and Store id
    previous_store_bill = patient_bills_2.sort_values(
        by=["id", "created-at"], ascending=[True, False]).drop_duplicates(subset='id')
    previous_store_bill = previous_store_bill.rename(columns={'store-id': 'previous-store-id'})

    # First bill date and first bill id calculation
    patient_first_bill = patient_bills_2.groupby('id').head(1)[['id', "bill-id", "created-at"]]
    patient_first_bill.rename(columns={"bill-id": "first-bill-id", "created-at": "first-bill-date"},
                              inplace=True)

    # # last bill date and last bill id calculation
    # patient_last_bill = patient_bills_2.groupby('id').tail(1)[['id', "bill-id", "created-at"]]
    # patient_last_bill.rename(columns={"bill-id": "last-bill-id", "created-at": "last-bill-date"}, inplace=True)
    #
    # Number of drug calculation
    patient_drugs = get_patient_drugs(db=db)

    patient_drug_agg = patient_drugs.groupby(['patient-id']).agg(
        {'drug-id': "nunique"}).reset_index().rename(
        columns={'drug-id': 'num-drugs', 'patient-id': 'id'})

    drug_subgroup = get_drug_subgroup(db=db)

    # Merge subgroups, take only relevant columns
    patient_drugs_count = patient_drugs.groupby(
        ['patient-id', 'drug-id'])['inventory-id'].count().reset_index().rename(
        columns={'inventory-id': 'count'})
    patient_drugs_subgroup_count = patient_drugs_count.merge(drug_subgroup, how='left',
                                                             on=['drug-id'])
    # Sub subgroup instances in each patient
    patient_subgroup = patient_drugs_subgroup_count.groupby(
        ['patient-id', 'subgroup'])['count'].sum().reset_index().rename(
        columns={'count': 'drug-count'})
    # Rank on use
    patient_subgroup = patient_subgroup.sort_values(by=['patient-id', 'drug-count'],
                                                    ascending=[True, False])
    patient_subgroup['rank'] = patient_subgroup.groupby(['patient-id']).cumcount() + 1
    # keep top2 subgroups
    patient_subgroup_top_2 = patient_subgroup[patient_subgroup['rank'] <= 2]
    # Make 2 columns, first for rank1, other for rank2
    patient_subgroup_top_2_pivot = patient_subgroup_top_2.pivot(index='patient-id', columns='rank',
                                                                values='subgroup').reset_index()
    patient_subgroup_top_2_pivot = patient_subgroup_top_2_pivot.reset_index(drop=True)

    patient_subgroup_top_2_pivot.columns = ['patient-id', 'disease-rank1', 'disease-rank2']

    # Assignment of primary disease
    # If rank1 is not others, then rank1 as it is
    # If rank1 is others, and rank2 is null, then rank1 as it is
    # If rank1 is others, and rank2 is something, then rank2
    patient_subgroup_top_2_pivot['primary-disease'] = np.where(
        (
                (patient_subgroup_top_2_pivot['disease-rank1'] == 'others') &
                (patient_subgroup_top_2_pivot['disease-rank2'].isnull() is False)
        ),
        patient_subgroup_top_2_pivot['disease-rank2'],
        patient_subgroup_top_2_pivot['disease-rank1']
    )
    patient_subgroup_top_2_pivot.head(2)
    patient_primary_disease = patient_subgroup_top_2_pivot[
        ['patient-id', 'primary-disease']].rename(
        columns={'patient-id': 'id'})

    # patient_value_segment = get_patient_value_segment(db=db)

    # patient_behaviour_segment = get_patient_behaviour_segment(changed_patients=changed_patients, pg_db=pg_db)

    # Merging all data points
    patient_data = changed_patients[['id']]

    # ### Feedback (nps)
    patient_data = patient_data.merge(nps, how='left', on=['id'])

    # ### Referral
    patient_data = patient_data.merge(referral, how='left', on=['id'])

    # ### Referral Primary Store
    patient_data = patient_data.merge(patient_primary_store[['id', 'primary-store-id']], how='left',
                                      on='id')

    # ### Primary Disease
    patient_data = patient_data.merge(patient_primary_disease, how='left', on='id')

    # ### Drug count
    patient_data = patient_data.merge(patient_drug_agg, how='left', on='id')

    # ### Average and Standard Purchase Interval
    patient_data = patient_data.merge(patient_bills_avg_std, how='left', on='id')

    # ### Previous store id
    patient_data = patient_data.merge(
        previous_store_bill[['id', 'previous-bill-date', 'previous-store-id']],
        how='left', on='id')

    # first bill id and date
    patient_data = patient_data.merge(patient_first_bill, how='left', on='id')

    patient_data = patient_data.merge(referral_code, how='left', on='id')

    patient_data = patient_data.merge(value_segment_anytime, how='left', on='id')

    patient_data = patient_data.merge(behaviour_segment_anytime, how='left', on='id')

    patient_data['is-nps'] = patient_data['is-nps'].fillna(False)

    """ Finally updating the batch data in table """
    update_data_in_patients_metadata_table(db, s3, patient_data)


def update_value_segment():
    # Extracting max date from patients metadata for value_seg
    query = f''' 
            select
                max(date("value-segment-calculation-date")) as max_date
            from
                "{schema}"."patients-metadata-2" '''
    rs_db.execute(query=query, params=None)
    pm_data: pd.DataFrame = rs_db.cursor.fetch_dataframe()

    # Extracting max date from customer value segment
    query = f''' 
            select
                max("segment-calculation-date") as max_date 
            from
                "{schema}"."customer-value-segment" '''
    rs_db.execute(query=query, params=None)
    cvs_data: pd.DataFrame = rs_db.cursor.fetch_dataframe()
    pm_max_vs_date = pm_data['max_date'][0]  # max value segment date in patients metadata
    cvs_max_vs_date = cvs_data['max_date'][0]  # max value segment date in customer-value-segment

    if str(pm_max_vs_date) != str(cvs_max_vs_date):
        logger.info('Condition passed for update: value-segment')
        # rs_db.execute('Begin;')
        update_q1 = f'''
            update 
                "{schema}"."patients-metadata-2"
            set 
                "value-segment"=cbs."value-segment",
                "value-segment-calculation-date"=cbs."segment-calculation-date"
            from 
                "{schema}"."patients-metadata-2" pm2
                    inner join 
                "{schema}"."customer-value-segment"  cbs
                    on 
                pm2."id"=cbs."patient-id"
            where 
                cbs."segment-calculation-date" = '{str(cvs_max_vs_date)}';
            '''

        update_q2 = f'''
            update 
                "{schema}"."patients-metadata-2"
            set 
                "value-segment"=null,
                "value-segment-calculation-date"=null
            from 
                "{schema}"."patients-metadata-2" pm2
            where 
                date(pm2."value-segment-calculation-date") != '{str(cvs_max_vs_date)}';
            '''
        rs_db.execute(query=update_q1, params=None)
        rs_db.execute(query=update_q2, params=None)
        # rs_db.execute('commit;')
        logger.info('value-segment Update Successful')


def update_behaviour_segment():
    # Extracting max date from customer behaviour segment
    query = f'''
            select 
                max("segment-calculation-date") as max_date
            from 
                "{schema}"."customer-behaviour-segment" '''

    rs_db.execute(query=query, params=None)
    cbs_data: pd.DataFrame = rs_db.cursor.fetch_dataframe()

    # Extracting max date from patients metadata for behaviour_seg
    query = f'''
            select
                max(date("behaviour-segment-calculation-date")) as max_date
            from 
                "{schema}"."patients-metadata-2" '''
    rs_db.execute(query=query, params=None)
    pm_data: pd.DataFrame = rs_db.cursor.fetch_dataframe()

    cbs_bs_max_date = cbs_data['max_date'][0]  # max date from customer value segment
    pm_bs_max_date = pm_data['max_date'][0]  # max behaviour segment date in patients metadata

    # cur_nmz_date = (datetime.datetime.today()).replace(day=1).strftime('%Y-%m-%d')  # current date

    if str(cbs_bs_max_date) != str(pm_bs_max_date):
        logger.info('Condition passed for update: behaviour-segment')
        # rs_db.execute('Begin;')
        update_q1 = f'''
            update 
                "{schema}"."patients-metadata-2"
            set 
                "behaviour-segment"=cbs."behaviour-segment",
                "behaviour-segment-calculation-date"=cbs."segment-calculation-date"
            from 
                "{schema}"."patients-metadata-2" pm2 
                    inner join 
                "{schema}"."customer-behaviour-segment" cbs 
                    on pm2."id"=cbs."patient-id"
            where 
                cbs."segment-calculation-date" = '{cbs_bs_max_date}';
            '''
        update_q2 = f'''
            update 
                "{schema}"."patients-metadata-2"
            set 
                "behaviour-segment"= null,
                "behaviour-segment-calculation-date"= null 
            from 
                "{schema}"."patients-metadata-2" pm2
            where 
                pm2."behaviour-segment-calculation-date" != '{cbs_bs_max_date}';
            '''
        rs_db.execute(query=update_q1, params=None)
        rs_db.execute(query=update_q2, params=None)
        # rs_db.execute('commit;')

        logger.info('behaviour-segment update successful')


# @profile
def main(db, s3, pg_db):
    insert_new_patients(db)
    mark_old_patients_pending(db)

    is_still_pending = True
    count = 1
    while is_still_pending:
        mark_pending_patients_updating(db=db)
        logger.info(f"batch: {count}, mark_pending_patients_updating done.")
        changed_patients = get_to_be_updated_patients(db=db)
        if isinstance(changed_patients, type(None)) or changed_patients.empty:
            is_still_pending = False
            logger.info("Completed all batches.")
        else:
            process_batch(changed_patients=changed_patients, db=db, s3=s3, pg_db=pg_db)
            logger.info(f"batch: {count}, process_batch done.")
            count += 1

    """ Updating the value and behaviour-segment """
    update_value_segment()
    update_behaviour_segment()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This is ETL script.")
    parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                        help="This is env(dev, stag, prod)")
    parser.add_argument('-b', '--batch_size', default=100, type=int, required=False,
                        help="batch size")
    parser.add_argument('-l', '--limit', default=None, type=int, required=False,
                        help="Total patients to process")
    args, unknown = parser.parse_known_args()
    env = args.env
    os.environ['env'] = env
    logger = get_logger()
    logger.info("I am in the right code.")
    batch_size = args.batch_size
    limit = args.limit
    logger.info(f"env: {env}, limit: {limit}, batch_size: {batch_size}")

    rs_db = DB(read_only=False)
    rs_db.open_connection()

    pg_db = None
    _s3 = S3()

    """ calling the main function """
    main(db=rs_db, s3=_s3, pg_db=pg_db)

    # Closing the DB Connection
    rs_db.close_connection()
