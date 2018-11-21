from urllib.request import urlopen, Request, HTTPError
import csv

# set up csv read
with open('export_html.csv', 'r') as csv_file:
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
  csv_reader = csv.reader(csv_file, delimiter=',')

  # This is for writing to html
  for row in csv_reader:
    html_file = open(f'rendered-html/{row[3]}.html', 'w')
    html_file.write(row[0])
    html_file.close()

