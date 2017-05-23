from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import config
import s3
import json

var = config.get_config()

url = "http://www.itsmarta.com/parking.aspx"
stations = ['North Springs', 'Sandy Springs', 'Dunwoody', 'Doraville',
'Chamblee', 'Brookhaven', 'Lenox', 'Lindbergh Center', 'College Park', 'Kensington']
ignore = ['Train Station', 'Parking Lot', 'Status', 'Train StationParking LotStatus']

# Parse the html into bs4
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# There are two tables - take the second table in the list
table = soup.findAll('table')[1]
rows = table.findAll('tr')

# this deletes the unnecessary rows
del rows[0], rows[0]

s = {}

lots = []

# logic: iterate through table rows. Find the first column that has a station it recognizes (from the `stations` list)
#   Next add the station to the `s` dictionary. If the column is not empty, and not in the `stations` list, it must be
#   a lot. So add the lot to the station key in the dictionary as list to allow for multiple lots.
# flaws in logic: if the station name is not in the stations list, it will be added as a lot to another station
for i in rows:
        # if i != 0:
        # print("____________________")
        station = i.select('td')[0].text.strip()
        lot = i.select('td')[1].text.strip()
        img = str(i.select('td')[2].find('img'))
        if img == '<img src="images\Green.png"/>':
            status = "lot open"
        elif img == '<img src="images\Red.png"/>':
            status = "lot closed"
        else:
            status = "unknown"
        lots.append({"station": "%s %s" % (station, lot),
                     "status":  status})
        # probably the better way to do it
        # lots.append({"station": station,
        #              lot: ""})


# Regex to match Last Updated
r = re.compile('updated on ([^\s]+)\s+(.*)(AM|PM)')

p = str(soup.body.select('.content > p')[0])
m = r.search(p)
d = m.group(1).strip()
t = m.group(2).strip()
p = m.group(3).strip()


# note: this does not take into account time zone differences
# also: this is not added to the dictionary. version 2 of this api should implement a data structure such as
# {"statuses":[{"station":"north springs", "lot 1":"lot open"},{"station":"north springs", "lot 2":"lot closed"}],
# "modified":date}
date = datetime.strptime("%s %s %s" % (d, t, p), "%m-%d-%Y %I:%M %p")

print(json.dumps(lots))

if var["publish_to_s3"]:
    AWS_ACCESS_KEY_ID = var["access_key"]
    AWS_SECRET_ACCESS_KEY = var["secret_access_key"]
    BUCKET = var["bucket"]
    s3.push_to_s3("status", json.dumps(lots), AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET)

## todo: ensure all stations are added to dictionary
## todo: add timezone to ensure correct epoch time

