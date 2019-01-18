import sys
import csv
import time
import requests
from bs4 import BeautifulSoup

def collect_routes(area, writer):

    routes = area.select('.mp-sidebar tr')
    location = '>'.join([link.text for link in area.select('.mb-half > a')][1:] 
        + [area.select_one('.mp-sidebar > h3').string[10:]])


    for route in routes:

        # Screen for non-route elements in sidebar
        if route.has_attr('id'):
            continue

        # Only scrape rock routes
        yds = route.select_one('.rateYDS')
        if yds:
            grade = yds.text
        else:
            continue

        name = route.a.text
        type = ', '.join(route.select_one('.route-type').attrs['class'][1:])
        rating = float(len(route.select('img')))
        if 'Half' in route.select('img')[-1].get('src'):
	        rating -= 0.5

        writer.writerow({
            'Name'    : name,
            'Type'    : type,
            'Grade'   : grade,
            'Rating'  : rating,
            'Location': location
        })


def crawl_from_area(URL, writer):

    # Don't overload their servers!
    time.sleep(10)

    area = BeautifulSoup(requests.get(URL).text, 'html.parser')

    # If there are sub areas, crawl each of them
    area_info = area.select_one('.mp-sidebar > h3')
    if area_info: 

        if 'Areas' in area_info.string:
            for sub_area in area.select('.lef-nav-row > a'):
            	crawl_from_area(sub_area.get('href'), writer)

        elif 'Routes' in area_info.string:
            collect_routes(area, writer)




if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = sys.argv[1]
        with open('mp-crawl-output.csv', 'w', newline = '') as csvfile:
            fieldnames = ['Name', 'Type', 'Grade', 'Rating', 'Location']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            crawl_from_area(url, writer)
    else:
        print("Please enter a mountain project area URL to search from")

     

