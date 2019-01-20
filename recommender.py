import csv
import treelib as tl

Grades = ['3rd', '4th', 'Easy 5th', '5', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', 
          '5.7',  '5.7+',    '5.8-',   '5.8', '5.8+',    '5.9-',   '5.9', ' 5.9+', 
        '5.10a', '5.10-', '5.10a/b', '5.10b', '5.10', '5.10b/c', '5.10c', '5.10+', '5.10c/d', '5.10d', 
        '5.11a', '5.11-', '5.11a/b', '5.11b', '5.11', '5.11b/c', '5.11c', '5.11+', '5.11c/d', '5.11d',
        '5.12a', '5.12-', '5.12a/b', '5.12b', '5.12', '5.12b/c', '5.12c', '5.12+', '5.12c/d', '5.12d',
        '5.13a', '5.13-', '5.13a/b', '5.13b', '5.13', '5.13b/c', '5.13c', '5.13+', '5.13c/d', '5.13d',
        '5.14a', '5.14-', '5.14a/b', '5.14b', '5.14', '5.14b/c', '5.14c', '5.14+', '5.14c/d', '5.14d',
        '5.15a',' 5.15-', '5.15a/b', '5.15b', '5.15', '5.15b/c', '5.15c', '5.15+',' 5.15c/d', '5.15d']

Boulder_Grades = ['V'+ x for x in ['-easy'] + [str(n) + qual for n in range(17) for qual in ['-','','+','-'+str(n+1)]] + ['?']]

def get_climb_grades(grade1, grade2):
    pass
    #This returns a list of grades in the user specified range

def get_boulder_grades(grade1, grade2):
    pass
    #This returns a list of grades in the user specified range

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
                csvfile = open(in_file, 'r', newline = '')
                print("Sucessfully opened " + in_file + '\n')
                return csvfile

            except OSError:
                print('Couldn\'t open ' + in_file + ' please try again.\n')

boulder_message = """
What grades are you looking to climb?
examples:
"V3-V6" returns V3- thru V6+
"v3-V3" returns V3- thru V3+
"-V4"   returns V4 and easier
"V4-"   returns V4 and harder
"any"   returns routes of any grade\n
"""

climb_message = """
What grades are you looking to climb?
examples:
"5.9-5.10d" returns 5.9- thru 5.10d
"5.9-5.9"   returns 5.9- thru 5.9+
"-5.11a"    returns 5.11a and easier
"5.11a-"    returns 5.11a and harder
"any"       returns routes of any grade\n
"""

def get_preferences():
    BorC = grades = None

    while not BorC:

        inp = input('Would you like to search for climbing Areas "C" or bouldering areas "B"?\n\n')

        if inp == 'B' or inp == 'C':
            BorC = inp

        else: 
            print('You entered ' + inp + '. Please enter either "C" or "B"\n')
    
    while not grades:

        if BorC == 'B':
            inp = input(boulder_message)
            if inp == 'any':
                pass
            elif len(inp.split('-')) == 2:
                pass
            else:
                print("Please check examples and reformat your input.\n")


        else:
            inp = input(climb_message)
            if inp == 'any':
                pass
            elif len(inp.split('-')) == 2:
                pass
            else:
                print("Please check examples and reformat your input.\n")


def main():

    print("\nWelcome to the climb recommender program!\n")

    csvfile = open_user_csv()

    get_preferences()

    csvfile.close()




if __name__ == "__main__":

    main()
