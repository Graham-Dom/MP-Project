import requests
import time
from bs4 import BeautifulSoup


def collect_routes(area):

	routes = area.select(".mp-sidebar tr")
	location = ">".join([link.text for link in area.select(".mb-half > a")][1:])

	for route in routes:

		name = route.a.text
		grade = route.select_one(".rateYDS").text
		types = route.select_one(".route-type").attrs["class"][1:]
		rating = float(len(route.select("img")))
		if "Half" in route.select("img")[-1].get("src"):
			rating -= 0.5

		print(name, grade, types, rating)

def crawl_from_area(URL):

	# Don't overload their servers!
	time.sleep(10)

	area = BeautifulSoup(requests.get(URL).text, "html.parser")

	# If there are sub areas, crawl each of them
	if "Areas" in area.select_one(".mp-sidebar > h3").string:

		for sub_area in area.select(".lef-nav-row > a"):
			crawl_from_area(sub_area.get("href"))

	else:
		collect_routes(area)




if __name__ == "__main__":

	crawl_from_area("https://www.mountainproject.com/area/105810440/second-tier")