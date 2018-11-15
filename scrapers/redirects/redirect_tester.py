from urllib.request import urlopen, Request, HTTPError
import csv

# set up csv read
with open('urls.csv', 'r') as csv_file:
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
  csv_reader = csv.reader(csv_file, delimiter=',')

  # set up csv write
  with open('checked.csv', 'w', newline='') as output_target:
    write_csv = csv.writer(output_target, delimiter=',')

    for row in csv_reader:
      # swap url
      url = row[0].split('/')
      clean_url = 'https://serenovastage.wpengine.com/' + '/'.join(url[3:len(url)])
      # send request
      try:
        req = Request(url=clean_url, headers=headers)
        status = urlopen(req).getcode()

      # catch 404s and whatever else
      except HTTPError as error:
        status = error.code

      # output
      print(f'{clean_url}{status}')
      write_csv.writerow([f'{clean_url}', f'{status}'])

