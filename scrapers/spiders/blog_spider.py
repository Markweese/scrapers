import re
import scrapy
import calendar

class PostItem(scrapy.Item):
    handle = scrapy.Field()
    command = scrapy.Field()
    title = scrapy.Field()
    body_html = scrapy.Field()
    summary_html = scrapy.Field()
    tags = scrapy.Field()
    published = scrapy.Field()
    published_at = scrapy.Field()
    image_src = scrapy.Field()
    image_alt = scrapy.Field()


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
      month_raw = article.css('span.month *::text').extract_first()
      month_clean = str(month_dict[month_raw]).zfill(2)
      # year is all good
      year = article.css('span.year *::text').extract_first()
      # extract URL handle for Shopify
      url = article.css('a::attr(href)').extract_first()
      url_arr = url.split('/')
      url_handle = url_arr[len(url_arr) - 2]
      # parse tags from article class
      classes_raw = article.css('::attr(class)').extract_first()
      classes_tagged = [tag for tag in classes_raw.split() if tag.startswith('tag-')]
      # remove tag- prefix from tag
      classes_clean = [string.replace('tag-', '') for string in classes_tagged]
      tags = ','.join(classes_clean)
      # make image sources generic
      prefix = 'https://www.newtonrunning.com'
      image_src_raw = article.css('figure.post-image a img::attr(src)').extract_first()
      image_src = image_src_raw if image_src_raw.startswith('http') else prefix + image_src_raw


      post['handle'] = url_handle
      post['command'] = 'NEW'
      post['title'] = article.css('h2.post-title a::attr(title)').extract_first()
      post['tags'] = tags
      post['published'] = 'TRUE'
      post['published_at'] = f'{month_clean}/{day}/{year}'
      post['image_src'] = image_src
      post['image_alt'] = article.css('figure.post-image a img::attr(alt)').extract_first()

      yield scrapy.Request(
          url,
          callback=self.parse_post,
          dont_filter=True,
          meta={'post_item': post}
      )

  def parse_post(self, response):
    post = response.meta.get('post_item')
    content_raw = response.css('div.entry-content').extract_first()
    html_removed = re.sub('<[^<]+?>', '', content_raw)
    content_clean = re.sub('\s+',' ', html_removed)
    content_summary = content_clean[0:300]
    post['summary_html'] = content_summary
    post['body_html'] = content_raw
    yield post
