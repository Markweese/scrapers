# Serenova Scrapers
This repo is focused on building scrapers to output content from the serenova.com marketing site.

## Installation
This repo uses Scrapy, be sure to install it locally before you begin by referencing [these instrucdtions](https://doc.scrapy.org/en/latest/intro/install.html#mac-os-x).

## Testing
To test you scraper out, you can run `scrapy crawl serenovablog` where `serenovablog` is the name of the scraper.

## Next steps
- Create a scraper for the [prodct updates](https://www.serenova.com/product-updates/all) posts. We need to store the category and it can be found in the idividual pst URL. For example `https://www.serenova.com/product-updates/reporting/agent-presence-reason-reports` this post is in the reporting category. This scraper does not need pagination but does need to follow the link to each post to gather its content.
- Output a single .csv file with the following fields:
1. title - should be self-explanatory
2. category - string from URL
3. excerpt - this is the short blurb on the listing page
4. content - this is the raw html of the post body, it should not have any needless markup surrounding it, get as close to the lowest wrapper as possible. See the other scraper for details