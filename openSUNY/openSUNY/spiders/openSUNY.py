from scrapy.spiders import BaseSpider

class OpenSunySpider(BaseSpider):
    name = 'openSUNY'
    start_urls = ['http://navigator.suny.edu/courses/search?cat=31','http://navigator.suny.edu/courses/search?cat=29','http://navigator.suny.edu/courses/search?cat=30','http://navigator.suny.edu/courses/search?cat=28']
    
    def parse(self, response):
        for course in response.css('.title a::attr(href)'):
            yield response.follow(course, self.parse_course)
        
        next_page = response.css('.next_page::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)
        
    
    def parse_course(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = {}
        item['Title'] = response.css('h1.title::text').extract_first()
        item['Location'] = response.xpath('//*[@id="suny-content"]/div[2]/div/div[2]/div/div/div[2]/div[2]/a/text()').extract_first()
        item['Description'] = response.xpath('//*[@id="suny-content"]/div[2]/div/div[2]/div/div/div[2]/div[4]/text()').extract()[1].strip()
        if len(response.xpath('//*[@id="suny-content"]/div[2]/div/div[2]/div/div/div[2]/div[9]/text()')) > 1:
            item['Instructor']  = response.xpath('//*[@id="suny-content"]/div[2]/div/div[2]/div/div/div[2]/div[9]/text()').extract()[1].strip()
        else:
            item['Instructor'] = "Unlisted"
        item['Date'] = response.xpath('//*[@id="suny-content"]/div[2]/div/div[2]/div/div/div[2]/div[10]/text()').extract()[1].strip()
        item['URL'] = response.request.url
        yield item
        