import scrapy
from pythonProject import items


# followed freeCodeCamp scrapy tutorial
class BookSpiderSpider(scrapy.Spider):
    name = "book_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]  # spider goes to this start url

    def parse(self, response):  # response is caught by the parse function
        books = response.css('article.product_pod')  # retrieves all books in main page
        for book in books:  # loops until there are no more books in the webpage, then follows next_page if it exists
            relative_url = book.css('h3 a ::attr(href)').get()  # get partial url that then is passed to if statement
            # check if catalogue is in tag and creates full book url
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield response.follow(book_url, callback=self.parse_book_webpage)
            # ^^ spider goes into book_url and calls function parse_book_webpage
        next_page = response.css('li.next a ::attr(href)').get()  # stores next page in variable
        if next_page is not None:  # if next page exists then generate the appropriate url
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)  # follows url of next

    def parse_book_webpage(self, response):  # retrieves all specified information from book_url
        table_rows = response.css("table tr")

        yield {
            'url': response.url,
            'title': response.css('.product_main h1::text').get(),
            'product_type': table_rows[1].css("td ::text").get(),
            'price_excl_tax': table_rows[2].css("td ::text").get(),
            'price_incl_tax': table_rows[3].css("td ::text").get(),
            'tax': table_rows[4].css("td ::text").get(),
            'availability': table_rows[5].css("td ::text").get(),
            'num_reviews': table_rows[6].css("td ::text").get(),
            'stars': response.css('p.star-rating').attrib['class'],
            'category': response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li["
                                       "1]/a/text()").get(),
            'description': response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'price': response.css('p.price_color ::text').get(),
        }
