# scrapers
This scrapes blog pages/staging sites for the purpose of content transfer and 404 testing primarily

- This repo uses scrapy, here is an (installation reference)[https://doc.scrapy.org/en/latest/intro/install.html#mac-os-x]
- In `scrapers > spiders > blog_spider` you can adjust settings to scrape desired sites
- Run `scrapy crawl blog` in your terminal to execute the program.
- Run `scrapy crawl blog -o '<filename>.csv' -t csv` to export to a csv in the app folder.
