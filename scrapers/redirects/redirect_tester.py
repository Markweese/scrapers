from urllib.request import urlopen, Request, HTTPError
from time import sleep
import csv
import ssl

# set up csv read
with open('redirect_urls.csv', 'r') as csv_file:
    # SSL bypass
  ssl._create_default_https_context = ssl._create_unverified_context
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
  csv_reader = csv.reader(csv_file, delimiter=',')
  target_index = 4

  # set up csv write
  with open('checked.csv', 'w', newline='') as output_target:
    write_csv = csv.writer(output_target, delimiter=',')

    for row in csv_reader:
      # swap url
      url = row[target_index]

      # send request
      try:
        req = Request(url=url, headers=headers)
        status = urlopen(req).getcode()

      # catch 404s and whatever else
      except HTTPError as error:
        status = error.code

      # output
      print(f'{url}{status}')
      write_csv.writerow([f'{url}', f'{status}'])

      # sleep(2)
