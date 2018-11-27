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
    author = scrapy.Field()
    blog_commentable = scrapy.Field()
    # # For use in the excelify redirects sheet
    path = scrapy.Field()
    target = scrapy.Field()


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

    for article in response.css('div.loops-wrapper article'):
      post = PostItem()

      # Format date
      published_at = self.format_date(article)

      # URL Data Extraction
      url_data = self.format_url(article)

      # parse categories as tags from the article class
      tags = self.parse_tags(article)

      # return image source and alt
      prefix = 'https://www.newtonrunning.com'
      cover_image = self.format_image_import(article, prefix)

      # summary_html
      summary_html = article.css('div.entry-content p').extract_first()


      post['handle'] = url_data['handle']
      post['command'] = 'NEW'
      post['title'] = article.css('h2.post-title a::attr(title)').extract_first()
      post['tags'] = tags
      post['published'] = 'TRUE'
      post['published_at'] = published_at
      post['summary_html'] = summary_html
      post['author'] = 'Newton'
      post['blog_commentable'] = 'moderate'
      post['image_src'] = cover_image['src']
      post['image_alt'] = cover_image['alt']
      # For use in the excelify redirects sheet
      post['path'] = url_data['path']
      post['target'] = url_data['target']

      yield scrapy.Request(
          url_data['url'],
          callback=self.parse_post,
          dont_filter=True,
          meta={'post_item': post}
      )

  def parse_post(self, response):
    post = response.meta.get('post_item')
    content_raw = response.css('div.entry-content').extract_first()
    body_html = self.format_image_nested(content_raw)
    post['body_html'] = body_html
    yield post

  def format_image_nested(self, content):
    class_attr = re.sub(r'class="[^\"]*"', '', content)
    srcset_attr = re.sub(r'srcset="[^\"]*"', '', class_attr)
    size_attr = re.sub(r'sizes="[^\"]*"', '', srcset_attr)
    style_attr = re.sub(r'style="[^\"]*"', '', size_attr)
    # Update this to take a current and target root
    href_update = re.sub(r'href="http(s)?:\/\/www.newtonrunning.com\/blog\/wp-content\/uploads\/', 'href="//cdn.shopify.com/s/files/1/0071/6698/4310/files/', style_attr)
    href_alt_update = re.sub(r'href="\/blog\/wp-content\/uploads\/', 'href="//cdn.shopify.com/s/files/1/0071/6698/4310/files/', href_update)
    src_update = re.sub(r'src="http(s)?:\/\/www.newtonrunning.com\/blog\/wp-content\/uploads\/', 'src="//cdn.shopify.com/s/files/1/0071/6698/4310/files/', href_alt_update)
    src_alt_update = re.sub(r'src="\/blog\/wp-content\/uploads\/', 'src="//cdn.shopify.com/s/files/1/0071/6698/4310/files/', src_update)

    return src_alt_update

  def parse_tags(self, article):
      classes_raw = article.css('::attr(class)').extract_first()

      classes_categorized = [tag for tag in classes_raw.split() if tag.startswith('category-')]
      # remove category- prefix from tag
      classes_clean = [string.replace('category-', '') for string in classes_categorized]
      tags = ','.join(classes_clean)

      return tags

  def format_date(self, article):
    month_dict = {v: k for k,v in enumerate(calendar.month_abbr)}

    day = article.css('span.day *::text').extract_first().zfill(2)
    month_raw = article.css('span.month *::text').extract_first()
    month_clean = str(month_dict[month_raw]).zfill(2)
    year = article.css('span.year *::text').extract_first()
    published_at = f'{year}-{month_clean}-{day}'

    return published_at
  
  def format_image_import(self, article, prefix):
    image_src_raw = article.css('figure.post-image a img::attr(src)').extract_first()

    if image_src_raw:
      image_src = image_src_raw if image_src_raw.startswith('http') else prefix + image_src_raw
      image_alt = article.css('figure.post-image a img::attr(alt)').extract_first()

    else:
      image_src = ''
      image_alt = ''

    return {'src': image_src, 'alt': image_alt}
  
  def format_url(self, article):
      url = article.css('a::attr(href)').extract_first()
      url_arr = url.split('/')
      url_handle = url_arr[len(url_arr) - 2]

      # clean urls for redirects
      url_path = '/' + '/'.join(url_arr[3:len(url_arr)])
      url_target = f'/blogs/blog/{url_handle}'

      return {'url': url,
              'handle': url_handle,
              'path': url_path,
              'target': url_target
            }