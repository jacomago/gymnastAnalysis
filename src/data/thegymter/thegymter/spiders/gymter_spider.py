import scrapy
import logging

class GymnastSiteSpider(scrapy.Spider):
    name = 'gymter'
    start_urls = ['https://thegymter.net/gymnast-database/']

    def parse(self, response):
        for a in response.css('div.entry-content table a'):
            yield response.follow(a, callback=self.parse_gymnast)

    def parse_gymnast(self, response):
        name = response.css('h1.entry-title::text').extract_first()
        data = {}
        for name_data in response.xpath('//div[@class="entry-content"]/table[1]'):
            rows = name_data.css('tr')
            items = {}
            for row in rows:
                items[row.css('td ::text').extract_first()] = row.css('td ::text')[1].extract()
            data[name] = items

        events_data = {}
        div =response.xpath('//div[@class="entry-content"]')
        count = len([0 for t in div.xpath('//table').extract()])-1
        logging.log(logging.DEBUG,"The count is " + str(count))
        key = ["Date","Type","VT","UB","BB","FX","AA"]
        for i in range(1, count+1):
            year = div.xpath('//p[' + str(i+2) + ']/strong/text()').extract_first()
            events_data[year] = []
            events  =  div.xpath('//table[' + str(i+1) + ']').css('tr')[1:]
            for event in events:
                event_name = event.css('a::text').extract_first()
                row_data = event.css('td::text').extract()
                logging.log(logging.DEBUG,"The length is " + str(len(row_data)))
                if len(row_data) == 6:
                    previous_data = events_data[year][-1]
                    row_data.insert(0, previous_data["Date"])
                    event_name = previous_data["Competition"]
                row_dict = {key[i]:row_data[i] for i in range(len(key))}
                row_dict["Competition"]= event_name
                events_data[year].append(row_dict)
        data[name]["Events"] = events_data
        yield data
