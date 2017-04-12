from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

url = "http://www.itsmarta.com/parking.aspx"
stations = ['North Springs', 'Sandy Springs', 'Dunwoody', 'Doraville',
'Chamblee', 'Brookhaven', 'Lenox', 'Lindbergh Center', 'College Park', 'Kensington']
ignore = ['Station', 'Parking Status']

# Parse the html into bs4
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# There are two tables - take the second table in the list
table = soup.findAll('table')[1]
rows = table.findAll('tr')


s = {}


# logic: iterate through table rows. Find the first column that has a station it recognizes (from the `stations` list)
#   Next add the station to the `s` dictionary. If the column is not empty, and not in the `stations` list, it must be
#   a lot. So add the lot to the station key in the dictionary as list to allow for multiple lots.
# flaws in logic: if the station name is not in the stations list, it will be added as a lot to another station
for i in rows:
    for j in i.findAll('td'):
        v = j.text.strip()
        if v in stations:
            station = v
            s[station] = []
        elif (v != "") and (v not in ignore) and station:
            s[station].append(v)


# Regex to match Last Updated
r = re.compile('<\/b>([^\s]+)\s+(.*)(AM|PM)')

# Search all of the body of HTML
m = r.search(str(soup.body))
# assign the Date to d, time to t, and the Period (AM/PM) to p
d = m[1].strip()
t = m[2].strip()
p = m[3].strip()


date = datetime.strptime("%s %s %s" % (d, t, p), "%m/%d/%Y %I:%M %p")
s["last modified"] = date.strftime('%s')

print(s)


## todo: ensure all stations are added to dictionary
## todo: add timezone to ensure correct epoch time

