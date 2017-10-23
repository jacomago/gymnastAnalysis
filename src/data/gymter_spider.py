import scrapy
import logging
from datetime import datetime
from dateutil import parser

class GymnastSiteSpider(scrapy.Spider):
    name = 'gymter'
    start_urls = ['https://thegymter.net/gymnast-database/']

    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('scrapy.spidermiddlewares.httperror')
        logger.setLevel(logging.WARNING)
        super().__init__(*args, **kwargs)

    def parse(self, response):
        for a in response.css('div.entry-content table a'):
            yield response.follow(a, callback=self.parse_gymnast)

    def parse_gymnast(self, response):
        name = response.css('h1.entry-title::text').extract_first()
        data = {}
        for name_data in response.xpath(
                '//div[@class="entry-content"]/table[1]'):
            rows = name_data.css('tr')
            items = {}
            for row in rows:
                items[row.css(
                    'td ::text').extract_first()
                ] = row.css('td ::text')[1].extract()
            data[name] = items

        events_data = []
        div =response.xpath('//div[@class="entry-content"]')
        count = len([0 for t in div.xpath('//table').extract()])-1
        key = ["Date","Competition","Type","Gymnast","VT","UB","BB","FX","AA"]
        for i in range(1, count+1):
            year = div.xpath('//p[' +
                             str(i+2) +
                             ']/strong/text()').extract_first()
            events  =  div.xpath('//table[' + str(i+1) + ']').css('tr')[1:]
            for event in events:
                event_name = event.css('a::text').extract_first()
                row_data = event.css('td')

                number_of_columns = len(row_data)
                date = datetime.now()
                if number_of_columns == 6:
                    previous_data = events_data[-1]
                    time = previous_data["Date"]
                    event_name = previous_data["Competition"]
                    row_data.insert(0, "blah_comp")
                    row_data.insert(0, "blah_time")
                else:
                    time_string = row_data[0].css(
                            'td::text').extract_first()
                    if number_of_columns ==9:
                        time_string += row_data[1].css(
                            'td::text').extract_first()
                        row_data[0:1] = "blah"
                    time = parser.parse(year.split(' ')[0]+ ' '
                                            +time_string.split('-')[0])
                row_dict = {}
                row_dict["Date"] = time
                row_dict["Competition"]= event_name
                row_dict["Type"] = row_data[2].css(
                            'td::text').extract_first()
                row_dict["Gymnast"] = name
                row_dict["VT"] = row_data[3].css(
                            'td::text').extract_first()
                row_dict["UB"] = row_data[4].css(
                            'td::text').extract_first()
                row_dict["BB"] = row_data[5].css(
                            'td::text').extract_first()
                row_dict["FX"] = row_data[6].css(
                            'td::text').extract_first()
                row_dict["AA"] = row_data[7].css(
                            'td::text').extract_first()

                events_data.append(row_dict)
        data[name]["Events"] = events_data
        yield data
