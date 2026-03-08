import csv
import requests

airport_lookup = {}

url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"

response = requests.get(url)
lines = response.text.splitlines()

reader = csv.reader(lines)

for row in reader:
    city = row[2].lower()
    iata = row[4]

    if iata and iata != "\\N":
        if city not in airport_lookup:
            airport_lookup[city] = []

        airport_lookup[city].append(iata)