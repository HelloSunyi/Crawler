import scrapy
from scrapy import Request

from Crawler.items import FootballItem
from Crawler.pipelines import FootballPipeline


class football_saishi_Spider(scrapy.Spider):
    name = "football_name"

    pipeline = set([FootballPipeline, ])

    start_urls = ['http://saishi.zgzcw.com/',
                  ]

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)


    def parse3(self, response):
        print "-----------"
        country = response.xpath("//dl[@class='star_dl']/dd[1]/var/text()").extract()
        founded_time = response.xpath("//dl[@class='star_dl']/dd[2]/var/text()").extract()
        league = response.xpath("//dl[@class='star_dl']/dd[3]/var/text()").extract()
        coach = response.xpath("//dl[@class='star_dl']/dd[4]/var/text()").extract()
        city = response.xpath("//dl[@class='star_dl']/dd[5]/var/text()").extract()
        court = response.xpath("//dl[@class='star_dl']/dd[6]/var/text()").extract()
        team_name = response.xpath("//dl[@class='star_dl']/dt/span/text()").extract()
        official_website = response.xpath("//dl[@class='star_dl']/dd[8]/var/text()").extract()

        item = FootballItem()
        if len(country) > 0 :
            item['country'] = country[0]
        else :
            item['country'] = ''

        if len(founded_time) > 0 :
            item['founded_time'] = founded_time[0]
        else :
            item['founded_time'] = ''

        if len(league) > 0 :
            item['league'] = league[0]
        else :
            item['league'] = ''

        if len(coach) > 0 :
            item['coach'] = coach[0]
        else :
            item['coach'] = ''

        if len(city) > 0 :
            item['city'] = city[0]
        else :
            item['city'] = ''

        if len(court) > 0 :
            item['court'] = court[0]
        else :
            item['court'] = ''

        if len(team_name) > 0 :
            item['team_name'] = team_name[0]
        else :
            item['team_name'] = ''

        if len(official_website) > 0 :
            item['official_website'] = official_website[0]
        else :
            item['official_website'] = ''

        return item


    def parse2(self, response):

        for url in response.xpath("//div[@class='tongji_list'][2]/ul/a/@href").extract():
            yield Request(url = url, callback=self.parse3)


    def parse(self, response):
        print "-----------------------------------"

        url_prefix = 'http://saishi.zgzcw.com'

        urls = []
        for sel in response.xpath('//div[@class="mainbottom"]/div[@class="gamesContent"]/div[1]/div[@class="ls"]/div[@class="lslogo fl"]/div[@class="kuang"]/a/@href'):
            urls.append(url_prefix + sel.extract())

        for sel in response.xpath('//div[@class="mainbottom"]/div[@class="gamesContent"]/div[1]/div[@class="ls"]/div[@class="lslogo fl"]/a/@href'):
            urls.append(url_prefix + sel.extract())

        for url in urls:
            print url

        for url in urls :
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0"}
            yield Request(url=url, callback=self.parse2, headers=headers)

        '''

            item = FootballItem()
            item["team_name"] = 'sw'
            item["country"] = ''
            item["founded_time"] = ''
            item['league'] = ''
            item['coach'] = ''
            item['city'] = ''
            item['court'] = ''
            item['official_website'] = ''

            yield item
        '''