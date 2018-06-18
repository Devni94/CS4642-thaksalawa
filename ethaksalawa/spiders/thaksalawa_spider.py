import scrapy
import re
from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector

class ThaksalawaSpider(scrapy.Spider):
	name = "thaksalawa"
	start_urls = [
        'http://www.e-thaksalawa.moe.gov.lk/web/si/library-section/general-knowledge.html',
	]
	#url_matcher = re.compile('^http:\/\/www\.e\-thaksalawa\.moe\.gov\.lk\/moodle\/course\/')	
	url_matcher = re.compile('^http:\/\/www\.e\-thaksalawa\.moe\.gov\.lk')

	def parse(self, response):
		link_extractor = LinkExtractor(allow=ThaksalawaSpider.url_matcher,tags=('li'),attrs=('onclick'))

		links = [link.url.split('"')[1] for link in link_extractor.extract_links(response)]

		#filename = 'links.txt'
		#with open(filename, 'wb') as f:
			#for link in links:
				#f.write(link)
				#f.write('\n')
	
		for link in links:
			yield scrapy.Request(url=link, callback=self.extract_info)
	
	def extract_info(self,response):
		section = response.css("div.activityinstance")

		for sec in section:
			yield{
			'name': sec.css('span.instancename::text').extract_first(),
			'url': sec.css('a::attr(href)').extract_first()
			} 
	

	
        
