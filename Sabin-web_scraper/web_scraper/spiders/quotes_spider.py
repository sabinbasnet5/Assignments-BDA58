import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.css('div.quote'):
            try:
                yield {
                    'quote': quote.css('span.text::text').get().replace('“', '').replace('”', ''),
                    'author': quote.css('span small.author::text').get(),
                    'tags': quote.css('div.tags a.tag::text').getall(),
                }
            except Exception as e:
                self.logger.error(f"Error parsing quote: {e}")
    
        # Follow pagination link to scrape all pages
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
