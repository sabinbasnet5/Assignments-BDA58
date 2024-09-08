import scrapy 


class QuotesSpiderSpider(scrapy.Spider):
    name = "quotes_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.css('div.quote'):

            quote_text = quote.css('span.text::text').get()
            # Remove unwanted characters using string method
            cleaned_quote = quote_text.strip("‚Äú")  # Removes leading and trailing characters

            yield {
                'quote': cleaned_quote,
                'author': quote.css('span small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        # Follow pagination link
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
