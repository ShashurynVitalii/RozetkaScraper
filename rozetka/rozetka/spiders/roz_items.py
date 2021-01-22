import scrapy
from rozetka.items import RozItem
from scrapy.loader import ItemLoader

class RozetkaItemsSpider(scrapy.Spider):
    name = 'roz_items'
    allowed_domains = ['web']
    start_urls = ['https://rozetka.com.ua/ua/computers-notebooks/c80253/']

    #function for scraping categories urls
    def parse(self, response):
        for cat_url in response.xpath('//a[@class="tile-cats__picture"]/@href').extract()[:3]:
            yield scrapy.Request(url = cat_url, callback = self.parse_pages, dont_filter = True)

    #function for scraping all pages inside one categorie
    def parse_pages(self, response):
        for item_url in response.xpath('//a[@class="goods-tile__heading"]/@href').extract():
            yield scrapy.Request(url = item_url, callback = self.parse_item, dont_filter = True)

        next_page = response.xpath('//div[@class="pagination"]/a[@class="button button_color_gray '
                                    'button_size_medium pagination__direction '
                                    'pagination__direction_type_forward"]/@href').get()
        if next_page:
            yield scrapy.Request(url = next_page, callback = self.parse_pages, dont_filter = True) 

    #function for scraping item from it's page
    def parse_item(self, response):
        l = ItemLoader(item = RozItem(), response = response)

        l.add_xpath('product_title', '//h1[@class="product__title"]/text()')
        l.add_xpath('product_code', '//p[@class="product__code detail-code"]/text()')
        l.add_xpath('product_price', '//script[@type="application/ld+json"][3]/text()')
        l.add_xpath('price_without_discount', '//script[@id="rz-client-state"]/text()')
        l.add_xpath('product_image', '//img[@class="product-photo__picture"]/@src')

        return l.load_item()