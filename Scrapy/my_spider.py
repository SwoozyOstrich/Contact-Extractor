import logging
import pandas as pd
import re
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from googlesearch import search
from crochet import setup


logging.getLogger('scrapy').propagate = False

def get_urls(tag, n, language):
    urls = [url for url in search(query=tag, stop=n, lang=language)][:n]
    return urls

class MailSpider(scrapy.Spider):
    
    name = 'email'
    
    def parse(self, response):
        
        links = LxmlLinkExtractor(allow=()).extract_links(response)
        links = [str(link.url) for link in links]
        links.append(str(response.url))
        
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_link) 
            
    def parse_link(self, response):
        
        for word in self.reject:
            if word in str(response.url):
                return
            
        html_text = str(response.text)
        mail_list = re.findall('[a-zA-Z0-9_.+-]{3,}@[a-zA-Z0-9-]{3,}\.[a-zA-Z0-9-.]{2,}', html_text)
        

        dic = {'email': mail_list, 'link': str(response.url)}
        df = pd.DataFrame(dic)
        
        df.to_csv(self.path, mode='a', header=False)
        df.to_csv(self.path, mode='a', header=False)

setup()
def get_info(tag, n, language, path, reject=[]):
    
    df = pd.DataFrame(columns=['email', 'link'], index=[0])
    df.to_csv(path, mode='a', header=True)
    
    print('Collecting Google urls...')
    google_urls = get_urls(tag, n, language)
    
    print('Searching for emails...')
    process = CrawlerRunner({'USER_AGENT': 'Mozilla/5.0'})
    process.crawl(MailSpider, start_urls=google_urls, path=path, reject=reject)
    process.start()
    
    print('Cleaning emails...')
    process.stop()
    df = pd.read_csv(path, index_col=0)
    df.columns = ['email', 'link']
    df = df.drop_duplicates(subset='email')
    df = df.reset_index(drop=True)
    df.to_csv(path, mode='w', header=True)
    
    return df

         