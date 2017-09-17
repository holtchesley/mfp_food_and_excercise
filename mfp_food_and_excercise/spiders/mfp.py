# -*- coding: utf-8 -*-
import os
import scrapy
from datetime import datetime, timedelta
from dateutil import parser as dtparser

class MfpSpider(scrapy.Spider):
    name = "mfp"
    allowed_domains = ["myfitnesspal.com"]
    start_urls = (
        'https://www.myfitnesspal.com/account/login',
    )

    def __init__(self, username='', password='', start_date=None, target_date='', 
        target_file='', outdir='output', *args, **kwargs):
        super(MfpSpider, self).__init__(*args, **kwargs)
        self.username = username
        self.password = password
        self.target_date = target_date
        self.target_file = target_file
        self.outdir = outdir

        self.start_date = dtparser.parse(target_date)
        self.end_date = dtparser.parse(target_date)
        if start_date is not None:
            self.start_date = dtparser.parse(start_date)
        self.dts = self.get_dts()

    def get_dts(self):
        ndays = (self.end_date-self.start_date).days
        return [self.start_date + timedelta(i) for i in xrange(ndays+1)]

    def parse(self, response):
        return scrapy.FormRequest.from_response(response,
            formdata={'username': self.username,
                'password':self.password},
            callback=self.logged_in)

    def logged_in(self, response):
        print 'LOGGED IN. PROCESSING...'
        for dt in self.dts:
            dtstr = dt.strftime('%Y-%m-%d')
            yield scrapy.Request(url="http://www.myfitnesspal.com/reports/printable_diary?from="+ dtstr + "&to="+ dtstr,
                callback=self.dump_tables)

    def write_table(self, rows, filename):
        with open(filename, "w") as f:
            f.write('\n'.join(rows))

    def get_outfile(self, name):
        return os.path.join(self.outdir, name + '.csv')
    
    def read_tables(self, response, name, delimiter='\t'):
        frmt = lambda x: delimiter.join(x).encode('UTF-8')# + u"\n".encode('UTF-8')
        outputs = []
        for table in response.xpath("//table[@id='" + name + "']"):
            for row in table.xpath(".//tr"):
                contents = row.xpath("./td/text()").extract()
                outputs.append(frmt(contents))
        return outputs

    def dump_tables(self, response):
        # get data
        dts = response.xpath('//h2/text()').extract()
        foods = self.read_tables(response, 'food')
        exercise = self.read_tables(response, 'excercise') # n.b. the typo
        title = dtparser.parse(dts[0]).strftime('%Y-%m-%d') if dts else ''
        
        # write data
        self.write_table(foods, self.get_outfile(title + "-food"))
        self.write_table(exercise, self.get_outfile(title + "-exercise"))
