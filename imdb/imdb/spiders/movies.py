from email import header
import imp
from operator import ne
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time

class MoviesSpider(CrawlSpider):
    name = 'movies'
    allowed_domains = ['imdb.com']
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?title_type=feature&release_date=1921-01-01,1945-12-31',
                            headers={'User-Agent':self.user_agent})

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True,process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="lister-page-next next-page"][1]'),process_request='set_user_agent')
    )
    
    # Order of the rule matters

    def set_user_agent(self,request,spider):
        request.headers['User-Agent'] = self.user_agent
        spider = 'movies'
        return request


    def parse_item(self, response):
        time.sleep(0.02)
        yield {
            'title':response.xpath("//div[@class='sc-80d4314-1 fbQftq']/h1/text()").get(),
            'gener':response.xpath('//div//a[@class="sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt"]/span/text()').getall(),
            'year':response.xpath("//div[@class='sc-80d4314-1 fbQftq']/div/ul/li[1]/a/text()").get(),
            'rating':response.xpath("//div[@class='sc-80d4314-1 fbQftq']/div/ul/li[2]/a/text()").get(),
            'duration':"".join(response.xpath("//div[@class='sc-80d4314-1 fbQftq']/div/ul/li[3]/text()").getall()),
            'directors':response.xpath("//div[@class='sc-fa02f843-0 fjLeDR']/ul/li[1]/div/ul/li[1]/a/text()").getall(),
            'writers':response.xpath("//div[@class='sc-2a827f80-2 kqTacj']/div/div/div/ul/li/div/ul/li[2]/a/text()").getall(),
            'lead_actors':response.xpath("//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[3]/div/ul/li/a/text()").getall(),
            'release_date':response.xpath("//div[@class='sc-f65f65be-0 ktSkVi']/ul[@class='ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base']/li[@class='ipc-metadata-list__item ipc-metadata-list-item--link']/div/ul/li[1]/a/text()").get(),
            'locations':response.xpath("//div[@class='sc-f65f65be-0 ktSkVi']/ul[@class='ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base']/li[@class='ipc-metadata-list__item ipc-metadata-list-item--link']/div/ul/li[3]/a/text()").getall(),
            'user_reviews':response.xpath('//span[@class="score"][1]/text()').get(),
            'critic_reviews':response.xpath('//span[@class="score"][2]/text()').get(),
            'meta_score':response.xpath('//span[@class="score"][3]/text()').get(),
            'url':response.url

        }
        