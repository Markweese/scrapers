import scrapy
import calendar

class PostItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    date = scrapy.Field()
    url = date = scrapy.Field()
    content = scrapy.Field()


class Blog(scrapy.Spider):
  name = 'blog'
  max_pages = 18
  current_page = 1
  start_urls = []

  # Grab every page and put it into start_urls
  while current_page <= max_pages:
    start_urls.append(f'https://www.newtonrunning.com/blog/page/{current_page}/?themify_builder_infinite_scroll=yes')

    current_page += 1

  def parse(self, response):
    # set up a  dictionary of month abbr/value pairs to pull from below
    month_dict = {v: k for k,v in enumerate(calendar.month_abbr)}

    for article in response.css('div.loops-wrapper article'):
      post = PostItem()

      # Format date, z-fill adds leading 0 for single digit
      day = article.css('span.day *::text').extract_first().zfill(2)
      # Swap month to number with month_dict
      month = article.css('span.month *::text').extract_first()
      month_clean = str(month_dict[month]).zfill(2)
      # year is all good
      year = article.css('span.year *::text').extract_first()
      url = article.css('a::attr(href)').extract_first()

      post['url'] = url
      post['date'] = f'{month_clean}/{day}/{year}'
      post['title'] = article.css('h2.post-title a::attr(title)').extract_first()
      post['image'] = article.css('figure.post-image a img::attr(src)').extract_first()

      yield scrapy.Request(
          url,
          callback=self.parse_post,
          dont_filter=True,
          meta={'post_item': post}
      )

  def parse_post(self, response):
    post = response.meta.get('post_item')
    post['content'] = response.css('div.entry-content').extract_first()
    yield post
