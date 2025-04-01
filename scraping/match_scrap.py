import scrapy

class match_scrap(scrapy.Spider):
    name = 'matches'

    def start_requests(self):
        start_urls = [
            'http://ufcstats.com/statistics/events/completed?page=all'
        ]

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # get the match event links
        links = response.css('td.b-statistics__table-col i.b-statistics__table-content a::attr(href)').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_matches)

    def parse_matches(self, response):
        # get matches links on the same date
        links = response.css('tr::attr(data-link)').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_each_match)

    '''
    def parse_each_match(self, response):
        # get the single match data
        fighter_data1 = response.css('div.b-fight-details__person')[0]
        fighter_data2 = response.css('div.b-fight-details__person')[1]

        yield {
            'event_name': response.css('a.b-link::text').get(default='').strip(),
            'method': response.css('i.b-fight-details__text-item_first i::text')[1].get(),
            'round': response.css('i.b-fight-details__text-item::text')[1].get().strip(),
            'time': response.css('i.b-fight-details__text-item::text')[3].get().strip(),

            'fighter_1': fighter_data1.css('a::text').get().strip(),
            'fighter_1_result': fighter_data1.css('i::text').get().strip(),

            'fighter_2': fighter_data2.css('a::text').get().strip(),
            'fighter_2_result': fighter_data2.css('i::text').get().strip(),

            'KD_1': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[2]/p[1]/text()').get().strip(),
            'KD_2': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[2]/p[2]/text()').get().strip(),
            'sig_str_1': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[3]/p[1]/text()').get().strip(),
            'sig_str_2': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[3]/p[2]/text()').get().strip(),
            'sig_str_pct_1': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[4]/p[1]/text()').get().strip(),
            'sig_str_pct_2': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[4]/p[2]/text()').get().strip(),
            'total_str_1': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[5]/p[1]/text()').get().strip(),
            'total_str_2': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[5]/p[2]/text()').get().strip(),
            'td_1': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[6]/p[1]/text()').get().strip(),
            'td_2': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[6]/p[2]/text()').get().strip(),
            'td_pct_1': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[7]/p[1]/text()').get().strip(),
            'td_pct_2': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[7]/p[2]/text()').get().strip(),
            'sub_att_1': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[8]/p[1]/text()').get().strip(),
            'sub_att_2': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[8]/p[2]/text()').get().strip(),
            'rvs1': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[9]/p[1]/text()').get().strip(),
            'rvs2': response.xpath(
                '//html/body/section/div/div/section[2]/table/tbody/tr/td[9]/p[2]/text()').get().strip(),
        }
        '''
    def parse_each_match(self, response):
        # Get fighter data elements from the match page
        fighter_data1 = response.css('div.b-fight-details__person')[0]
        fighter_data2 = response.css('div.b-fight-details__person')[1]

        # Extract raw fighter result texts and create win indicators
        fighter1_result_raw = fighter_data1.css('i::text').get(default='').strip()
        fighter2_result_raw = fighter_data2.css('i::text').get(default='').strip()
        fighter1_win = 1 if fighter1_result_raw.upper() == 'W' else 0
        fighter2_win = 1 if fighter2_result_raw.upper() == 'W' else 0

        # Extract percentage fields and convert them to floats
        def convert_percentage(raw):
            if raw:
                return float(raw.replace('%', '').strip())
            return None

        fighter1_sig_str_pct_raw = response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[4]/p[1]/text()').get(default='').strip()
        fighter2_sig_str_pct_raw = response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[4]/p[2]/text()').get(default='').strip()
        fighter1_td_pct_raw = response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[7]/p[1]/text()').get(default='').strip()
        fighter2_td_pct_raw = response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[7]/p[2]/text()').get(default='').strip()

        fighter1_sig_str_pct = convert_percentage(fighter1_sig_str_pct_raw)
        fighter2_sig_str_pct = convert_percentage(fighter2_sig_str_pct_raw)
        fighter1_td_pct = convert_percentage(fighter1_td_pct_raw)
        fighter2_td_pct = convert_percentage(fighter2_td_pct_raw)

        yield {
            'event_name': response.css('a.b-link::text').get(default='').strip(),
            'win_method': response.css('i.b-fight-details__text-item_first i::text')[1].get(default='').strip(),
            'round': response.css('i.b-fight-details__text-item::text')[1].get(default='').strip(),
            'time': response.css('i.b-fight-details__text-item::text')[3].get(default='').strip(),

            'fighter1_name': fighter_data1.css('a::text').get(default='').strip(),
            'fighter1_result': fighter1_result_raw,
            'fighter1_win': fighter1_win,

            'fighter2_name': fighter_data2.css('a::text').get(default='').strip(),
            'fighter2_result': fighter2_result_raw,
            'fighter2_win': fighter2_win,

            'fighter1_KD': response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[2]/p[1]/text()').get(default='').strip(),
            'fighter2_KD': response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[2]/p[2]/text()').get(default='').strip(),

            'fighter1_sig_str': response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[3]/p[1]/text()').get(default='').strip(),
            'fighter2_sig_str': response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[3]/p[2]/text()').get(default='').strip(),

            'fighter1_sig_str_pct': fighter1_sig_str_pct,
            'fighter2_sig_str_pct': fighter2_sig_str_pct,

            'fighter1_total_str': response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[5]/p[1]/text()').get(default='').strip(),
            'fighter2_total_str': response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[5]/p[2]/text()').get(default='').strip(),

            'fighter1_td': response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[6]/p[1]/text()').get(default='').strip(),
            'fighter2_td': response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[6]/p[2]/text()').get(default='').strip(),

            'fighter1_td_pct': fighter1_td_pct,
            'fighter2_td_pct': fighter2_td_pct,

            'fighter1_sub_att': response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[8]/p[1]/text()').get(default='').strip(),
            'fighter2_sub_att': response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[8]/p[2]/text()').get(default='').strip(),

            'fighter1_reversals': response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[9]/p[1]/text()').get(default='').strip(),
            'fighter2_reversals': response.xpath('//html/body/section/div/div/section[2]/table/tbody/tr/td[9]/p[2]/text()').get(default='').strip(),
        }