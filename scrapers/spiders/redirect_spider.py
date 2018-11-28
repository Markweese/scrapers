import scrapy

class urlItem(scrapy.Item):
    # For use in the excelify redirects sheet
    Path = scrapy.Field()
    Target = scrapy.Field()
    ID = scrapy.Field()
    Command = scrapy.Field()

class Redirect(scrapy.Spider):
  name = 'redirect'
  max_pages = 18
  current_page = 1
  start_urls = []
  blog_name = 'blog'

  # Grab every page and put it into start_urls
  while current_page <= max_pages:
    start_urls.append(f'https://www.newtonrunning.com/blog/page/{current_page}/?themify_builder_infinite_scroll=yes')
    current_page += 1

  def parse(self, response):
    blog_name = 'blog'
    url_category_start = '/blog/'
    url_category_target = f'/blogs/{blog_name}/tagged/'
    url_tag_start = '/blog/tag/'
    url_tag_target = f'/blogs/{blog_name}/'
    category_arr = []
    tag_arr = []

    for article in response.css('div.loops-wrapper article'):
      new_categories = self.parse_categories(article, 'category')
      new_tags = self.parse_categories(article, 'tag')
      category_arr = category_arr + new_categories
      tag_arr = tag_arr + new_tags
      url = urlItem()
      url_data = self.format_url(article)

      for category in new_categories:
        url_data['category'] = category

        # blog/category/post
        url['ID'] = ''
        url['Command'] = 'NEW'
        url['Path'] = '/blog/%(category)s/%(handle)s' % url_data
        url['Target'] = url_data['target']

        yield url

    for category in self.remove_duplicates(category_arr):
      url = urlItem()

      url['ID'] = ''
      url['Command'] = 'NEW'
      url['Path'] = url_category_start + category
      url['Target'] = url_category_target + category

      yield url

    for tag in self.remove_duplicates(tag_arr):
      url = urlItem()

      url['ID'] = ''
      url['Command'] = 'NEW'
      url['Path'] = url_tag_start + tag
      url['Target'] = url_tag_target

      yield url
  
  def format_url(self, article):
      url = article.css('a::attr(href)').extract_first()
      url_arr = url.split('/')
      url_handle = url_arr[len(url_arr) - 2]

      url_path = '/' + '/'.join(url_arr[3:len(url_arr)])
      url_target = f'/blogs/blog/{url_handle}'

      return {
              'handle': url_handle,
              'path': url_path,
              'target': url_target
            }

  def parse_categories(self, article, cat_type):
    classes_raw = article.css('::attr(class)').extract_first()

    classes_categorized = [category for category in classes_raw.split() if category.startswith(f'{cat_type}-')]
    categories = [string.replace(f'{cat_type}-', '') for string in classes_categorized]

    return categories

  def remove_duplicates(self, items):
    return list(set(items))