import sys

"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

### YOUR CODE HERE ###

### Question 1: a) When was the first positive COVID case in Harrisonburg?
### b) When was the first positive case in Rockingham County?

# call data parsing function to get the data from the NYT file
data = parse_nyt_data("../../data/covid/us-counties.csv")

# define two lists to hold the data for Harrisonburg and Rockingham County. 
# It will iterate through the data and only keep the entries for these two localities.
harrisonburg_data = []
rockingham_data = []

# only find Harrisonburg and Rockingham County data
for entry in data:
    if entry[1] == 'Harrisonburg city' and entry[2] == 'Virginia':
        harrisonburg_data.append(entry)

    elif entry[1] == 'Rockingham' and entry[2] == 'Virginia':
        rockingham_data.append(entry)

# find the first positive case in Harrisonburg and print the date
for entry in harrisonburg_data:
    if entry[4] > 0:
        first_positive_harrisonburg = entry[0]
        print("The first positive COVID case in Harrisonburg was on: " + first_positive_harrisonburg)
        break

# find the first positive case in Rockingham County and print the date
for entry in rockingham_data:
    if entry[4] > 0:
        first_positive_rockingham = entry[0]
        print("The first positive COVID case in Rockingham County was on: " + first_positive_rockingham)
        break    

### Question 2: On what date was the greatest number of new cases reported in Harrisonburg?
### What date in Rockingham County?

# define a function to find the greatest number of new cases and the date with the greatest number of new cases
# This function will take in a list of tuples (data) and iterate through the list to find the greatest number of new cases and the date on which that occurred. 
# It will return a tuple containing the date and the number of new cases.
def find_greatest_new_cases(data):
    greatest_new_cases = 0
    greatest_new_cases_date = ''

    for i in range(1, len(data)):
        new_cases = data[i][4] - data[i - 1][4]

        if new_cases > greatest_new_cases:
            greatest_new_cases = new_cases
            greatest_new_cases_date = data[i][0]

    return greatest_new_cases_date, greatest_new_cases

# find the greatest number new cases and the date for Harrisonburg and Rockingham County
harrisonburg_greatest_new_cases = find_greatest_new_cases(harrisonburg_data)
rockingham_greatest_new_cases = find_greatest_new_cases(rockingham_data)

# print the greatest number of new cases and the date for Harrisonburg and Rockingham County
print("The greatest number of new cases in Harrisonburg was on " + harrisonburg_greatest_new_cases[0] +
      " with " + str(harrisonburg_greatest_new_cases[1]) + " new cases.")
print("The greatest number of new cases in Rockingham County was on " + rockingham_greatest_new_cases[0] +
      " with " + str(rockingham_greatest_new_cases[1]) + " new cases.")

### Question 3: What was the worst seven-day period in Harrisonburg city for new COVID cases?
### What period in Rockingham County? (These are seven-day periods when the number of new cases was maximal)

# define a function to find the worst seven-day period for new COVID cases. 
# This function will take in a list of tuples (data) and iterate through the list to find the seven-day period with the greatest number of new cases. 
# It will return a tuple containing the start date, end date, and the number of new cases during that period.
def find_worst_seven_day_period(data):
    daily_new_cases = []
    worst_seven_day_cases = 0
    worst_seven_day_start_date = ''
    worst_seven_day_end_date = ''

    for i in range(1, len(data)):
        new_cases = data[i][4] - data[i - 1][4]
        daily_new_cases.append((data[i][0], new_cases))

    for i in range(len(daily_new_cases) - 6):
        seven_day_total_cases = 0

        for j in range(7):
            seven_day_total_cases += daily_new_cases[i + j][1]

        if seven_day_total_cases > worst_seven_day_cases:
            worst_seven_day_cases = seven_day_total_cases
            worst_seven_day_start_date = daily_new_cases[i][0]
            worst_seven_day_end_date = daily_new_cases[i + 6][0]

    return worst_seven_day_start_date, worst_seven_day_end_date, worst_seven_day_cases

# find the worst seven-day period for new COVID cases in Harrisonburg and Rockingham County
harrisonburg_worst_seven_day_period = find_worst_seven_day_period(harrisonburg_data)
rockingham_worst_seven_day_period = find_worst_seven_day_period(rockingham_data)

# print the worst seven-day period for new COVID cases in Harrisonburg and Rockingham County
print("The worst seven-day period for new COVID cases in Harrisonburg was from " +
      harrisonburg_worst_seven_day_period[0] + " to " + harrisonburg_worst_seven_day_period[1] +
      " with " + str(harrisonburg_worst_seven_day_period[2]) + " new cases.")
print("The worst seven-day period for new COVID cases in Rockingham County was from " +
      rockingham_worst_seven_day_period[0] + " to " + rockingham_worst_seven_day_period[1] +
      " with " + str(rockingham_worst_seven_day_period[2]) + " new cases.")

# Questions 1-3 have been answered and printed to the console. 
# The program has successfully parsed the NYT COVID-19 data and extracted relevant information for Harrisonburg city and Rockingham County!