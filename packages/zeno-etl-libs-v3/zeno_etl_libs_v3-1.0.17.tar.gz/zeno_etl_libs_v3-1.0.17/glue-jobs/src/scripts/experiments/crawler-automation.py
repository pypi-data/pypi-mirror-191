from zeno_etl_libs.helper.aws.crawler import crawler

crawler = crawler()
crawler.start_crawler(crawler_name='datalake-prod-crawler')
