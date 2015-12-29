# -*- coding: utf-8 -*-
import scrapy

class MfpSpider(scrapy.Spider):
    name = "mfp"
    allowed_domains = ["myfitnesspal.com"]
    start_urls = (
        'https://www.myfitnesspal.com/account/login',
    )

    def __init__(self, username='', password='', target_date='', target_file='', *args, **kwargs):
        super(MfpSpider, self).__init__(*args, **kwargs)
        self.username=username
        self.password=password
        self.target_date=target_date
        self.target_file=target_file

    def parse(self, response):
        return scrapy.FormRequest.from_response(response,
                               formdata={'username': self.username,
                                         'password':self.password},
                                                callback=self.logged_in)

    def logged_in(self,response):
        yield scrapy.Request(url="http://www.myfitnesspal.com/reports/printable_diary?from="+self.target_date + "&to="+ self.target_date,
                             callback=self.dump_tables)

    def dump_tables(self, response):
        with open(self.target_date + "-excercise.dsv", "w") as exfile:
            for row in response.xpath("(//table[@id='excercise']//tr[count(.//td)>3])[position() < last()]"):
                exfile.write( '|'.join(row.xpath("./td/text()").extract()).encode('UTF-8') + u"\n".encode('UTF-8') )
        with open(self.target_date + "-food.dsv", "w") as foofile:
            for row in response.xpath("(//table[@id='food']//tr[count(.//td)>3])[position() < last()]"):
                foofile.write( '|'.join(row.xpath("./td/text()").extract()).encode('UTF-8') + u"\n".encode('UTF-8'))
