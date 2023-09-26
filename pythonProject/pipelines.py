# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# For processing all data into preferred format
# ItemAdapter uses item key defined in items.py
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PythonprojectPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        # Category & Product Type --> switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # Price --> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        # Availability --> extract only the number in stock
        availability_string = adapter.get('availability')
        string_array = availability_string.split('(')
        if len(string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])

        # Reviews --> convert string to int
        num_reviews = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews)

        # Star Rating --> convert string to int
        stars_split = adapter.get('stars').split(' ')
        star_value = stars_split[1].lower()
        if star_value == "zero":
            adapter['stars'] = 0
        elif star_value == "one":
            adapter['stars'] = 1
        elif star_value == "two":
            adapter['stars'] = 2
        elif star_value == "three":
            adapter['stars'] = 3
        elif star_value == "four":
            adapter['stars'] = 4
        elif star_value == "five":
            adapter['stars'] = 5

        return item

