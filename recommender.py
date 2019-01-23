import csv
from heapq import nlargest

climb_grades = ['Easy 5th', '5', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', 
          '5.7',  '5.7+',    '5.8-',   '5.8', '5.8+',    '5.9-',   '5.9', ' 5.9+', 
        '5.10a', '5.10-', '5.10a/b', '5.10b', '5.10', '5.10b/c', '5.10c', '5.10+', '5.10c/d', '5.10d', 
        '5.11a', '5.11-', '5.11a/b', '5.11b', '5.11', '5.11b/c', '5.11c', '5.11+', '5.11c/d', '5.11d',
        '5.12a', '5.12-', '5.12a/b', '5.12b', '5.12', '5.12b/c', '5.12c', '5.12+', '5.12c/d', '5.12d',
        '5.13a', '5.13-', '5.13a/b', '5.13b', '5.13', '5.13b/c', '5.13c', '5.13+', '5.13c/d', '5.13d',
        '5.14a', '5.14-', '5.14a/b', '5.14b', '5.14', '5.14b/c', '5.14c', '5.14+', '5.14c/d', '5.14d',
        '5.15a',' 5.15-', '5.15a/b', '5.15b', '5.15', '5.15b/c', '5.15c', '5.15+',' 5.15c/d', '5.15d']

boulder_grades = ['V-easy', 'V0-',  'V0',  'V0+', 'V0-1', 'V1-', 'V1', 'V1+', 
        'V1-2', 'V2-', 'V2', 'V2+', 'V2-3', 'V3-', 'V3', 'V3+', 'V3-4', 'V4-', 'V4', 'V4+', 
        'V4-5', 'V5-', 'V5', 'V5+', 'V5-6', 'V6-', 'V6', 'V6+', 'V6-7', 'V7-', 'V7', 'V7+', 
        'V7-8', 'V8-', 'V8', 'V8+', 'V8-9', 'V9-', 'V9', 'V9+', 'V9-10', 'V10-', 'V10', 'V10+', 
        'V10-11', 'V11-', 'V11', 'V11+', 'V11-12', 'V12-', 'V12', 'V12+', 'V12-13', 'V13-', 'V13', 'V13+', 
        'V13-14', 'V14-', 'V14', 'V14+', 'V14-15', 'V15-', 'V15', 'V15+', 'V15-16', 'V16-', 'V16', 'V16+', 'V?']

# These functions return a list of grades in the user specified range
# grade1 and grade2 must be in climb_grades/climb_grades
# if '' is grade1: returns grade2 and lower
# if '' is grade2: returns grade1 and higher

def get_climb_grades(grade1, grade2):

    # Make sure that the given grades are in the correct order, swap if they aren't
    lower, upper = climb_grades.index(grade1), climb_grades.index(grade2)

    # Include + and - for 5.7, 5.8, 5.9
    if lower in [11,14]:
        lower -= 1 

    if upper in [8,11,14]:
        upper += 1

    return set(climb_grades[lower:upper+1])


def get_boulder_grades(grade1, grade2):

    lower, upper = boulder_grades.index(grade1), boulder_grades.index(grade2)

    # Make sure that the given grades are in the correct order, swap if they aren't
    if lower > upper:
        lower, upper = upper, lower
    
    # Include - and + grades
    lower -= 1
    upper += 1

    return set(boulder_grades[lower:upper+1])


def open_user_csv():

    while True:

        in_file = input (
        'If you have a csv file with data scraped from Mountain Project, please enter the file name now.\n' 
        'Otherwise, enter "Q" to quit and use mp-scraper.py to scrape climbing data.\n\n')

        if in_file == 'Q':
            exit()

        elif in_file[-4:] != '.csv':
            print('Error: given input is not a csv file or "Q"\n')

        else:

            try:
                csvfile = open(in_file, 'r', newline = '', encoding='latin-1')
                print("Sucessfully opened " + in_file + '\n')
                return csvfile

            except OSError:
                print('Couldn\'t open ' + in_file + ' please try again.\n')


class Location():


    def __init__(self, location, rating):
        self.data = {'name': location, 'total rating': rating, 'sublocations' : {}}


    def __getitem__(self, key):
        return self.data[key]


    def __gt__(self, other):
        # This allows areas to be sorted according to their destination value
        return self.destination_value() > other.destination_value()


    def add_sublocation(self, subloc):
        self.data['sublocations'][subloc['name']] = subloc 


    def add_climb(self, rating):
        self.data['total rating'] += rating

    
    def destination_value(self):
        # This is an attempt at measuring whether or not an area is a destination
        # A destination is somewhere you'd go in hopes of finding many different 
        # sublocations or crags that have climbs you like
        # For example, Boulder is a huge climbing destination, but if you wanted to trad climb in boulder,
        # you'd probably like to know about Eldorado Canyon or Boulder Canyon, both of which have numerous 
        # sub areas where you can trad climb. This metric helps those locations stand out above their parent locations
        if len(self.data['sublocations']) == 0:
            return self.data['total rating']
        else:
            return self.data['total rating'] * len(self.data['sublocations'])


    def get_subtree(self):
        # Returns a list of every node in the subtree
        if self.data['sublocations']:
            return [self] + sum([subloc.get_subtree() for subloc in self.data['sublocations'].values()],[])

        else:
            return [self]


    def get_crags(self):
        # This returns a list of every crag in the subtree, where a crag is defined as a location without sublocations
        # A crag actually has climbs, whereas non-crag areas just hold sub-areas
        if self.data['sublocations']:
            return sum([subloc.get_crags() for subloc in self.data['sublocations'].values()],[])

        else:
            return [self]


    def print_subtree(self):
        if self.destination_value() > 0:
            print('(' + self.data['name'] + ', ' + str(self.data['total rating']) + ' ' + str(self.destination_value()) + ')')
            for subloc in self.data['sublocations'].values():
                subloc.print_subtree()


class Location_Tree():
    # A hierarchical location - sublocation tree with 'All Locations' as root    
    # A location keeps the total number of stars of all the routes in it's sublocations
    # This allows for comparison between of the number and quality of its routes locations 
    def __init__(self):
        self.root = Location('All Locations', 0)

    def add_route(self, location, rating):
        parent_loc = self.root

        for loc in location:
            # If the sublocation is already in the tree, add to it's total rating
            if loc in parent_loc['sublocations']:
                parent_loc['sublocations'][loc].add_climb(rating)

            # Otherwise create a new location node for that sublocation      
            else:
                parent_loc.add_sublocation(Location(loc, rating))

            parent_loc = parent_loc['sublocations'][loc]


def destination_recommendations(loc_tree):
    # First, make a list of every location in the tree
    all_locations = loc_tree.root.get_subtree()
    
    # Print the 10 best destinations based on the users preferences, if there are not 10 then skip
    if len(all_locations) >= 10:

        # Remove the highest level location - this is the location that the user provided the URL for - not helpful
        del all_locations[1]
        print('The top ten destinations based on the data and climbing preferences you input are:')
        for destination in nlargest(10, all_locations):
            print(destination['name'])
    print()


def crag_reccomendations(loc_tree):
    # First, make a list of every location in the tree
    all_crags = loc_tree.root.get_crags()
    
    # Print the 10 best crags based on the users preferences, 
    if len(all_crags) >= 10:
        print('The top ten specific crags based on the data and climbing preferences you input are:')
        for crag in nlargest(10, all_crags):
            print(crag['name'])

    # If there are not 10 then print all of them
    elif len(all_crags) > 1:
        print('The top specific crags based on the data and climbing preferences you input are:')
        for crag in all_crags:
            print(crag['name'])

    else: 
        print('There are no routes matching your preferences in the provided file\n')

    print()


def make_reccomendations(csvfile, preferences):
    loc_tree = Location_Tree()

    reader = csv.DictReader(csvfile)

    for row in reader:
        # If a route matches user preferences, add it to the location tree
    	if preferences[1] <= set(row['Type'].split(', ')) and row['Grade'] in preferences[0]:
            loc_tree.add_route(row['Location'].split('>'), float(row['Rating']))

    destination_recommendations(loc_tree)
    crag_reccomendations(loc_tree)
    
    

boulder_message = """
What grades are you looking to climb?
examples:
"V3-V6" returns V3- thru V6+
"V3-V3" returns V3- thru V3+
"-V4"   returns V4 and easier
"V4-"   returns V4 and harder
"any"   returns routes of any grade
"Q"     quits program\n
"""

climb_message = """
What grades are you looking to climb?
examples:
"5.8-5.10d" returns 5.8- thru 5.10d
"5.8-5.8"   returns 5.8- thru 5.8+
"-5.11a"    returns 5.11a and easier
"5.11a-"    returns 5.11a and harder
"any"       returns routes of any grade
"Q"         quits program\n
"""

def get_preferences():
    BorC = grades = type = None

    while not BorC:

        inp = input('Would you like to search for climbing Areas "C" or bouldering areas "B"?\n\n')

        if inp == 'B' or inp == 'C':
            BorC = inp

        else: 
            print('You entered ' + inp + '. Please enter either "C" or "B"\n')
    
    while not grades:

        if BorC == 'B':
            type = {'Boulder'}
            inp = input(boulder_message)

            if inp == 'any':
                grades = set(boulder_grades)

            elif len(inp.split('-')) == 2 and '+' not in inp:
                lower, upper = inp.split('-')

                # V0- and V16+ are the second lowest and second highest grades according to index in boulder_grades
                # When passed to the get_boulder_grades function, they will be incremented/decremented 
                if lower == '':
                    lower = 'V0-'

                elif upper == '':
                    upper = 'V16+'

                if lower in boulder_grades and upper in boulder_grades:
                    grades = get_boulder_grades(lower, upper)

                else:
                    print('Please check examples and reformat your input.\n')

            elif inp == 'Q':
                return []

            else:
                print('Please check examples and reformat your input.\n')


        else:
            inp = input(climb_message)

            if inp == 'any':
                grades = set(climb_grades)

            elif len(inp.split('-')) == 2:
                lower, upper = inp.split('-')

                if lower == '':
                    lower = 'Easy 5th'

                elif upper == '':
                    upper = '5.15d'

                if lower in climb_grades and upper in climb_grades:
                    grades = get_climb_grades(lower, upper)

                else:
                    print("Please check examples and reformat your input.\n")

            # The program ends when an empty list is returned as preferences
            elif inp == 'Q':
                return []

            else:
                print("Please check examples and reformat your input.\n")

    while not type:
        inp = input('\nDo you want to search for sport "S", trad "T", toprope "TR", alpine "A", or any "any" routes? "Q" to quit.\n\n')

        if inp == 'S':
            type = {'Rock', 'Sport'}

        elif inp == 'T':
            type = {'Rock', 'Trad'}

        elif inp == 'TR':
            type = {'Rock', 'Toprope'}

        elif inp == 'A':
            type = {'Rock', 'Alpine'}

        elif inp == 'any':
            type = {'Rock'}
        
        # The program ends when an empty list is returned as preferences
        elif inp == 'Q':
            return []

        else:
            print(inp + ' is not one of "S", "T, "TR", "A", "any", or "Q".')

    return [grades, type]        


def main():

    print('\nWelcome to the climb recommender program!\n')

    csvfile = open_user_csv()
    preferences = get_preferences()

    if preferences:
        make_reccomendations(csvfile, preferences)

    csvfile.close()




if __name__ == '__main__':
    main()
