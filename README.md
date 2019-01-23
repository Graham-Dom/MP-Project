# Mountain Project scraper and climbing area recommendation system
**This application is inteded to supplement mountain project, not replace it.**

There are 2 components to this application: 
1) **mp-scraper.py** - 
A crawler that generates a list of routes in a user-provided area, e.g. https://www.mountainproject.com/area/105855459/west-virginia
2) **recommender.py** - 
A recommendation system that recommends sub-areas in the provided area that have the most climbs that match user preferences, i.e. trad routes 5.8 - 5.10a, boulder problems V5 and harder, or sport routes of any grade

Feel free to use/modify either or both of these programs as you like

## Why is this useful?
Mountain Project already has a recommendation system called "route finder" which is pretty useful for finding specific routes based on your preferences. **This recommendation tool is geared towards questions of which areas would be good for climbing, instead of which routes** e.g. If you are making a road trip to New Mexico, and want to know areas with high concentrations of boulder problems, or want to find crags within Red River Gorge with a large number of 5.10 sport routes.

### Installation:
$git clone https://github.com/Graham-Dom/MP-Project

### Dependencies:
-requests

-BeautifulSoup

If you use pipenv, use pipenv install, and run program files from pipenv shell



### Scraper Example:
To scrape data from a MP area, run mp-scraper.py with a target URL and an optional csv file to store data, e.g.

$ python3 mp-scraper.py https://www.mountainproject.com/area/105855459/west-virginia ouput.csv

This will make a csv file with the name, type, grade, rating, and location of every single climb and boulder problem in WV. 

**As you can imagine there are lots of sub-areas within WV, so the scraper paces its requests to 1 every 5 seconds, so as not to overload MP's servers. It can take hours to scrape large areas like Colorado or California. If you are impatient, you can change this pacing, but please keep in mind that MP is a free (and awesome) service, and they may restrict access to those that "Interfere with or damage the operation of the Service".**

### Scraper Example:
$python3 recommender.py

Will lead the user through a series of prompts to determine their preferences, and then provide up to 10 destinations and up to 10 individual crags that match those preferences. 
For example, if we search Colorado for hard sport routes (5.13a and up) we get this output:

The top ten destinations based on the data and climbing preferences you input are:
Clear Creek Canyon, 
Rifle Mtn Park, 
Boulder Canyon, 
Boulder, 
Golden, 
Shelf Rd, 
Poudre Canyon, 
S Platte, 
South, 
Ft Collins 

The top ten specific crags based on the data and climbing preferences you input are:
The New River Wall, 
Primo Wall, 
Project Wall, 
The Arsenal, 
Wall of the '90s, 
The Wicked Cave, 
Bauhaus Wall, 
Seal Rock, 
The Industrial Wall, 
Anti-Phil Wall

If we look for trad routes in the 5.7-5.9 range we get this output:

The top ten destinations based on the data and climbing preferences your input are:
Boulder Canyon, 
S Platte, 
Eldorado Canyon SP, 
Boulder, 
S Fork of St Vrain Canyon, 
Lumpy Ridge, 
Estes Park Valley, 
Alpine Rock, 
RMNP - Rock, 
Buena Vista

The top ten specific crags based on the data and climbing preferences your input are:
Redgarden - S Buttress, 
Cracked Canyon, 
Turkey Tail, 
Redgarden - Lumpe to the top, 
Turkey Rock, 
Turkey Perch, 
West Ridge - part C - Pony Express to Long John, 
Hallett Peak, 
Redgarden - Tower One, 
Wind Tower - SW Face 

A CSV file for West Virginia, and some sample input files provided, in the Data and Input Tests directories, respectively. 
