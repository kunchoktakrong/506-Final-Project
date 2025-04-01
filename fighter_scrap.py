import scrapy
import string

class fighter_scrap(scrapy.Spider):

    name = 'fighters'

    def start_requests(self):
        start_urls = ['http://www.ufcstats.com/statistics/fighters?char=' + char + '&page=all' for char in string.ascii_lowercase]

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.css('tr.b-statistics__table-row td.b-statistics__table-col a::attr(href)').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_fighter)

    def parse_fighter(self, response):
        height = response.css('li.b-list__box-list-item.b-list__box-list-item_type_block::text')[1].get().strip()
        weight = response.css('li.b-list__box-list-item.b-list__box-list-item_type_block::text')[3].get().strip()
        reach  = response.css('li.b-list__box-list-item.b-list__box-list-item_type_block::text')[5].get().strip()
        stance = response.css('li.b-list__box-list-item.b-list__box-list-item_type_block::text')[7].get().strip()
        date_birth = response.css('li.b-list__box-list-item.b-list__box-list-item_type_block::text')[9].get().strip()

        SLpM = response.xpath(
        "//i[contains(@class, 'b-list__box-item-title') and contains(., 'SLpM:')]/following-sibling::text()"
        ).get(default='').strip()
    
        StrAcc = response.xpath(
        "//i[contains(@class, 'b-list__box-item-title') and contains(., 'Str. Acc.:')]/following-sibling::text()"
        ).get(default='').strip()
    
        SApM = response.xpath(
        "//i[contains(@class, 'b-list__box-item-title') and contains(., 'SApM:')]/following-sibling::text()"
        ).get(default='').strip()
    
        StrDef = response.xpath(
        "//i[contains(@class, 'b-list__box-item-title') and contains(., 'Str. Def:')]/following-sibling::text()"
        ).get(default='').strip()
    
        TDAvg = response.xpath(
        "//i[contains(@class, 'b-list__box-item-title') and contains(., 'TD Avg.:')]/following-sibling::text()"
        ).get(default='').strip()
    
        TDAcc = response.xpath(
        "//i[contains(@class, 'b-list__box-item-title') and contains(., 'TD Acc.:')]/following-sibling::text()"
        ).get(default='').strip()
    
        TDDef = response.xpath(
        "//i[contains(@class, 'b-list__box-item-title') and contains(., 'TD Def.:')]/following-sibling::text()"
        ).get(default='').strip()
    
        SubAvg = response.xpath(
        "//i[contains(@class, 'b-list__box-item-title') and contains(., 'Sub. Avg.:')]/following-sibling::text()"
        ).get(default='').strip()

        yield {
        'name': response.xpath('/html/body/section/div/h2/span[1]/text()').get(default='').strip(),
        'height': height,
        'weight': weight,
        'reach': reach,
        'stance': stance,
        'date_birth': date_birth,
        'SLpM': SLpM,
        'StrAcc': StrAcc,
        'SApM': SApM,
        'StrDef': StrDef,
        'TDAvg': TDAvg,
        'TDAcc': TDAcc,
        'TDDef': TDDef,
        'SubAvg': SubAvg,
    }


