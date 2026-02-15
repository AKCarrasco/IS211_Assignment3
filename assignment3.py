import argparse
# other imports go here
import urllib.request
import csv
import re
from collections import Counter
from datetime import datetime

def downloadData(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')

def processData(file_content):
    reader = csv.reader(file_content.splitlines())
    data = list(reader)
    return data

def imageStats(data):
    image_hits = [row for row in data if re.search(r'\.(jpg|gif|png)$', row[0], re.IGNORECASE)]
    percent = (len(image_hits) / len(data)) * 100
    print(f"Image requests account for {percent:.1f}% of all requests")
    return image_hits

def popularBrowser(data):
    browsers = []
    for row in data:
        ua = row[2]
        if 'Firefox' in ua:
            browsers.append('Firefox')
        elif 'Chrome' in ua:
            browsers.append('Chrome')
        elif 'MSIE' in ua or 'Trident' in ua:
            browsers.append('Internet Explorer')
        elif 'Safari' in ua:
            browsers.append('Safari')
    most_common = Counter(browsers).most_common(1)
    if most_common:
        print(f"Most popular browser is {most_common[0][0]}")

def hitsPerHour(data):
    hours = []
    for row in data:
        dt = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
        hours.append(dt.hour)
    hour_counts = Counter(hours)
    for hr in range(24):
        print(f"Hour {hr:02d} has {hour_counts.get(hr,0)} hits")

def main(url):
    print(f"Running main with URL = {url}...")
    csvData = downloadData(url)
    data = processData(csvData)
    imageStats(data)
    popularBrowser(data)
    hitsPerHour(data)

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)

#py week3assignmnt.py --url http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv

