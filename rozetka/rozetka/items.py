from scrapy.item import Item, Field

class RozItem(Item):
    product_title = Field()
    product_code = Field()
    product_price = Field()
    price_without_discount = Field()
    product_image = Field()