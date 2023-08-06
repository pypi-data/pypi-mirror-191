from zeno_etl_libs.helper.email.email import Email, any_email_in_string


def create_temp_table(db, table):
    """ creates table_temp table and truncates the data if table already exists """
    temp_table = table.replace("-", "_") + "_temp"
    query = """
            create temporary table if not exists 
                "%s" (LIKE "prod2-generico"."%s");
        """ % (temp_table, table)

    db.execute(query=query)

    query = """truncate "%s";""" % (temp_table)
    db.execute(query=query)

    return temp_table


def month_diff(date_a, date_b):
    """
    This function returns month difference between calendar dates 'date_a' and 'date_b'
    """
    return 12 * (date_a.dt.year - date_b.dt.year) + (date_a.dt.month - date_b.dt.month)


def drop_table(db, table_name, is_temp=True):
    try:
        if is_temp:
            db.execute(query="""drop table "%s";""" % table_name)
        else:
            db.execute(query="""drop table "prod2-generico"."%s";""" % table_name)
        print(f"table dropped: {table_name}")
    except Exception as e:
        print(f"Error in table drop: {str(e)}")


def get_table_info(db, table_name, schema=None):
    """

    :param db: db class object
    :param table_name: table name
    :param schema: is schema is None --> temp table without schema
    :return: table info data frame
    """
    if schema:
        schema_filter = f"and table_schema = '{schema}'"
    else:
        schema_filter = ''

    query = f"""
        select
            ordinal_position as position,
            column_name,
            data_type,
            case
                when character_maximum_length is not null
                    then character_maximum_length
                else numeric_precision
            end as max_length,
            is_nullable,
            column_default as default_value
        from
            information_schema.columns
        where
            table_name = '{table_name}'
            -- enter table name here
            {schema_filter}
        order by
            ordinal_position;
    """
    db.execute(query=query)
    return db.cursor.fetch_dataframe()


def batch(iterable, n=1):
    """
    splits any iterable in batches

    Example:

    data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] # list of data

    for x in batch(data, 3):
        print(x)

    # Output

    [0, 1, 2]
    [3, 4, 5]
    [6, 7, 8]
    [9, 10]

    :param iterable: list, tuple, df
    :param n: batch size

    """

    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def log_or_email_error(logger, exception: Exception, email_to,
                       subject='132-supply-chain JOB FAILURE'):
    """
    if email_to string has any email id in it, email will be sent and code will be terminated.
    else exception will be raised.

    :param logger: logger object
    :param exception: Exception object
    :param email_to: csv list of emails eg: abc@zeno.health,xyz@zeno.health
    """
    email = Email()
    if any_email_in_string(email_to):
        logger.exception(exception)
        email.send_email_file(subject=subject,
                              mail_body='The subject job has failed due to: {}'.format(exception),
                              to_emails=email_to)
        exit(0)
    else:
        raise exception
