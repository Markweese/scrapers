# Primary Tools
1. Blog Content: Exports WordPress blog pages into a CSV filed to be parsed into Shopify with [excelify](excelifiy.io).
2. URL Redirects: Exports redirects for WordPress individual blog, blog category, and blog tag pages for Shopify integration using [excelify](excelifiy.io).
3. Redirect tester: This allows you to check the status of your new URLs

## Basic Setup
This repo uses scrapy, here is an [installation reference](https://doc.scrapy.org/en/latest/intro/install.html#mac-os-x).

## Blog Content
- In `scrapers > spiders > blog_spider` you can adjust settings.
- Run `scrapy crawl blog` in your terminal to execute the program.
- Run `scrapy crawl blog -o '<filename>.csv' -t csv` to export to a csv in the app folder.

#### CSV headers need to be changed from the 'header_name' paradigm to 'Header Name' to cooperate with Excelify.

## URL Redirects
- In `scrapers > spiders > redirect_spider` you can adjust settings.
- Run `scrapy crawl redirect` in your terminal to execute the program.
- Run `scrapy crawl redirect -o '<filename>.csv' -t csv` to export to a csv in the app folder.

## Redirect Tester
- cd into /scrapers/redirects
- Populate the `redirect_urls.csv` with the URLs you want to test
- run python3 redirect_tester.py

