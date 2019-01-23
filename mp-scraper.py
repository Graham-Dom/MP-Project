import sys
import csv
import time
import requests
import string
from bs4 import BeautifulSoup

def collect_routes(area, writer):

    routes = area.select('.mp-sidebar tr')
    location  = ('>'.join([link.get('href').split('/')[-1].replace('-', ' ') 
        for link in area.select('.mb-half > a')][1:] + [area.select_one('.mp-sidebar > h3').string[10:]]))

    for route in routes:

        # Some areas have notes in their sidebar, these notes have an ID, which we use to ignore them
        if route.has_attr('id'):
            continue

        # Only scrape rock routes - sorry ice climbers
        yds = route.select_one('.rateYDS')
        if yds:
            grade = yds.text
        else:
            continue

        name = route.a.text
        
        # The route's type is stored as a list of qualifiers, e.g. ['Rock', 'Sport'], or ['Boulder', 'Alpine']
        type = ', '.join(route.select_one('.route-type').attrs['class'][1:])

        # The sidebar shows stars and half-star images to give a rough rating of the route.
        # This is not the exact rating of the route, but prevents having to open each route individually
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
    time.sleep(5)

    area = BeautifulSoup(requests.get(URL).text, 'html.parser')

    # If there are sub areas, crawl each of them
    area_info = area.select_one('.mp-sidebar > h3')

    # Empty areas don't have a header, ignore them
    if area_info: 

        # The mountain project sidebar either says "Areas in ..." or "Routes in ..."
        # Use this information to decide whether or not to keep exploring subareas

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

            # This creates a writer object, which we pass to the crawler, and use to record route information
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            crawl_from_area(url, writer)
    else:
        print("Please enter a mountain project area URL to search from")

     

