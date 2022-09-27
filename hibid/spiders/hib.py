import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')

class HibSpider(scrapy.Spider):
    name = 'hib'
    def start_requests(self):
        # for url in ['https://hibid.com/lots?q=steel&apage=1','https://hibid.com/lots?q=pipe&apage=1']:            
        yield scrapy.Request('https://hibid.com/lots?q=steel&apage=1', callback=self.parse1, meta={"pyppeteer": True},cb_kwargs={'index':'steel'})
        yield scrapy.Request('https://hibid.com/lots?q=pipe&apage=1', callback=self.parse2, meta={"pyppeteer": True},cb_kwargs={'index':'pipe'})

    def parse1(self, response,index):        
        total_pages = response.xpath("//ul[@class='pagination justify-content-end px-0 .d-sm-inline-block']/li[last()-1]/a/text()").get()       
        current_page =response.css("ul.pagination li.active a::text").get()        
        url = response.url         
        if total_pages and current_page:
            if int(current_page) ==1:
                for i in range(2, int(total_pages)+1): 
                    min = 'page='+str(i-1)
                    max = 'page='+str(i)
                    url = url.replace(min,max)                                                 
                    yield response.follow(url=url, cb_kwargs={'index':index})
        
        links = response.css('a.lot-title-ellipsis::attr(href)')
        for link in links:
            yield response.follow("https://hibid.com"+link.get(), callback=self.parse_item, cb_kwargs={'index':index})  

    def parse2(self, response, index):        
        total_pages = response.xpath("//ul[@class='pagination justify-content-end px-0 .d-sm-inline-block']/li[last()-1]/a/text()").get()       
        current_page =response.css("ul.pagination li.active a::text").get()        
        url = response.url         
        if total_pages and current_page:
            if int(current_page) ==1:
                for i in range(2, int(total_pages)+1): 
                    min = 'page='+str(i-1)
                    max = 'page='+str(i)
                    link = url.replace(min,max)                                                 
                    yield response.follow(link, cb_kwargs={'index':index})
        
        links = response.css('a.lot-title-ellipsis::attr(href)')
        images = response.css('img.lot-thumbnail::attr(src)').getall()
        counter = 0
        for link in links:
            image = images[counter]
            yield response.follow("https://hibid.com"+link.get(), callback=self.parse_item, cb_kwargs={'index':index,'image':image}) 
            counter = counter+1         

    def parse_item(self, response,index,image): 
        print(".................")         
        image_link = image
        print(image_link)
        auction_date = response.css('div.lot-auction-date-range::text').get()
        print(auction_date)
        location = response.xpath("//div[@class='text-decoration-underline']/a/text()").get()
        print(location)
        product_name = response.xpath("//div[@class='page-header']/h1/span/text()[2]").get()
        print(product_name)
        lot_number = response.xpath("//div[@class='page-header']/h1/span/text()[1]").get()
        print(lot_number)
        auctioner = response.css('a.lot-company-page-link::text').get()
        print(auctioner)

        yield{            
            'product_url' : response.url,           
            'item_type' :index.strip(),            
            'image_link' : image_link,          
            'auction_date' : auction_date,            
            'location' : location,           
            'product_name' : product_name,            
            'lot_id' : lot_number,          
            'auctioner' : auctioner,
            'website' : 'hibid',
            'description' : ''             
        }    



      

      
         