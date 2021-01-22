import re
import json

class RozetkaPipeline(object):
    def process_item(self, item, spider):
        #clean item's title
        title = item['product_title'][0].strip()
        title = title.split(' ')[1:]
        item['product_title'] = ' '.join(title)

        #clean item's code
        code = re.search(r'[0-9]+', item['product_code'][0])
        item['product_code'] = code.group()

        #clean item's price
        price_js = json.loads(item['product_price'][0])
        price = re.search(r'[0-9]+', price_js['offers']['price'])
        item['product_price'] = price.group()

        #process item's price_without_discount
        dis_price = re.search(r'[0-9]+', re.search(r'old_price&q;:&q;[0-9]+', item['price_without_discount'][0]).group())
        if int(dis_price.group()) > int(price.group()):
            item['price_without_discount'] = dis_price.group()
        else:
            del item['price_without_discount']

        #clean item's image url
        image = item['product_image'][0]
        item['product_image'] = image

        return item
