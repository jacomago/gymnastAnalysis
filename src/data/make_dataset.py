# -*- coding: utf-8 -*-
import os
import click
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from dotenv import find_dotenv, load_dotenv
from gymter_spider import GymnastSiteSpider

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': output_filepath+"/%(name)s/%(time)s.json",
        'ROBOTSTXT_OBEY' :True,
        'LOG_LEVEL' : logging.INFO,
        'DOWNLOAD_DELAY':3.0
    })

    process.crawl(GymnastSiteSpider)
    process.start() # the script will block here until the crawling is finished

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
