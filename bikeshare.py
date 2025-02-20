import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_valid_input(user_input, valid_answers, common_alternatives):
    """Checks if inputs are valid and coverts to alternatives if neccessary"""
    if user_input.lower() in valid_answers:
        return True, user_input
    #check if user input is one of the common alternative or misspelled names
    if user_input.lower() in common_alternatives:
        corrected_input = common_alternatives[user_input.lower()]
        print(f"We assume you mean {corrected_input.title()}")
        return True, corrected_input
    return False, user_input

def find_indices_sublist(main_list, sublist):
    """Find indices of each unique item in the sublist within the main list."""
    indices_list = []
    for item in sublist:
        try:
            index = main_list.index(item)
            indices_list.append(index)
        except ValueError:
            indices_list.append(None)  # Append None if the item is not found
    return indices_list

# Function to convert 0 to 1 based indices
def convert_to_1_based_indices(indices_list):
    """Moves each value of list of integers up by 1"""
    return [index + 1 if index is not None else None for index in indices_list]

# Function to print data 5 rows at a time
def print_dataframe_chunks(df,chunk_size=5):
    """Prints out data five rows at a time"""
    for start in range(0, len(df), chunk_size):
        end = start + chunk_size
        prnt_chunk = df.iloc[start:end]
        print(prnt_chunk)
        user_input = input("\nPress Enter to continue or type 'no' to exit:\n").lower().strip()
        if user_input in ['no','n']:
            print("Exiting")
            break

# Translate month index to month name
def translate_month_index_name(month_index):
    """Formats index as month name"""
    if 1 <= month_index <= 12:
        # Create a Timestamp for first monday of the year
        timestamp = pd.Timestamp(year=2017, month=month_index, day=1)
        month_name = timestamp.strftime('%B')  # get month name
        return month_name
    
# Translate day of week index to dow name
def translate_dow_index_name(dow_index):
    """Formats index as name of the day of the week"""
    if 0 <= dow_index <= 7:
        # Create a Timestamp for the first of the month
        first_monday = pd.Timestamp("2017-01-02")
        date_offset = first_monday + pd.Timedelta(days=dow_index)
        day_name = date_offset.strftime('%A')  # get day name
        return day_name
    
# Translate 24 hour index to 12 hour time
def translate_24hr_index_to_12hr_time(hour_index):
    """Formats hour index into 12 hour time with AM/PM marker"""
    if 0 <= hour_index <= 23:
        # Create timestamp that contains the hour being indexed
        timestamp = pd.Timestamp.today().replace(hour=hour_index, minute=0, second=0, microsecond=0)
        time_12hr = timestamp.strftime('%I:%M %p')
        return time_12hr

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    user_city = ""
    city = ""
    valid_city = ["chicago","new york city","washington"]
    common_city_alternatives = {
        "chitown": "chicago",
        "new york": "new york city",
        "nyc": "new york city",
        "dc": "washington",
        "washington d.c.": "washington",
        "washington dc": "washington",
        "chigaco": "chicago",
        "chcago": "chicago",
        "chigago": "chicago",
        "chciago": "chicago",
        "new yrok city": "new york city",
        "new yourk city": "new York City",
        "new yor city": "new York City",
        "washinton": "washington",
        "washingotn": "washington",
        "washngton": "washington",
        "wahsington": "washington"
    }
    is_valid_city = False
    while not is_valid_city:
        #have the user input is one of the cities for which we have data
        user_city = input("\nWhich city's data would you like to explore (Chicago, New York City, or Washington)\n").lower().strip()
        is_valid_city, corrected_city = check_valid_input(user_city, valid_city, common_city_alternatives)
        if not is_valid_city:
            print("\nPlease input the name one of these cities (Chicago, New York City, or Washington).\n")
        else:
            city = corrected_city
            print("Thank you!")
            
    print(f"You selected: {city.title()}")
    # get user input for month (all, january, february, ... , june)
    user_month = "" #initialize variables
    valid_month = ["january","february","march","april","may","june"]
    common_month_alternatives = {
        "janury": "january",
        "januray": "january",
        "janaury": "january",
        "janauary": "january",
        "jan": "january",
        "feburary": "february",
        "febuary": "february",
        "febrary": "february",
        "februray": "february",
        "febraury": "february",
        "feb": "february",
        "marh": "march",
        "mrach": "march",
        "mach": "march",
        "mar": "march",
        "aprl": "april",
        "apirl": "april",
        "aprile": "april",
        "apr": "april",
        "mai": "may",
        "mey": "may",
        "jue": "june",
        "jun": "june",
        "juin": "mune"
    }
    month = ["january","february","march","april","may","june"]
    selected_month = []
    print("You may choose to narrow the data down to a month or months")
    print("Not selecting any month will default to using data across all months")
    while True:
        user_month = input("\nType a month and hit enter\n(January, February, March, April, May, or June).\nType 'done' to finish selecting month(s).)\n").lower().strip()
        if user_month == 'done':
            break
        is_valid_month, corrected_month = check_valid_input(user_month, valid_month, common_month_alternatives)
        if not is_valid_month:
            print("\nPlease pick from these months?\n(January, February, March, April, May, or June).\n")
        else:
            selected_month.append(corrected_month)
            print("\nThank you! Would you like to select another month?\n")
    if selected_month:
        month = selected_month
    print(f"You selected: {' '.join(month).title()}")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    user_day = ""
    selected_day = []
    valid_day = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    common_day_alternatives = {
        "monady": "monday",
        "mondy": "monday",
        "munday": "monday",
        "monay": "monday",
        "mon": "monday",
        "mo": "monday",
        "m": "monday",
        "tusday": "tuesday",
        "tuseday": "tuesday",
        "tuesady": "tuesday",
        "tuesdy": "tuesday",
        "tues": "tuesday",
        "tu": "tuesday",
        "wensday": "wednesday",
        "wedensday": "wednesday",
        "wednsday": "wednesday",
        "wendsday": "wednesday",
        "wed": "wednesday",
        "we": "wednesday",
        "w": "wednesday",
        "thrusday": "thursday",
        "thurday": "thursday",
        "thursady": "thursday",
        "thurdsay": "thursday",
        "thurs": "thursday",
        "thur": "thursday",
        "thu": "thursday",
        "th": "thursday",
        "firday": "friday",
        "fridy": "friday",
        "firady": "friday",
        "fryday": "friday",
        "fri": "friday",
        "fr": "friday",
        "saterday": "saturday",
        "satuday": "saturday",
        "satrday": "saturday",
        "saturdy": "saturday",
        "sat": "saturday",
        "sa": "saturday",
        "sundy": "sunday",
        "sundey": "sunday",
        "sunady": "sunday",
        "sundday": "sunday",
        "sund": "sunday",
        "sun": "sunday",
        "su": "sunday"
    }
    print("You may choose to narrow the data down to a day or days of the week")
    print("Not selecting any day will default to using data across all days of the week")
    while True:
        user_day = input("\nType a day and hit enter\n(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday).\nType 'done' to finish selecting day(s))\n").lower().strip()
        if user_day == 'done':
            break
        is_valid_day, corrected_day = check_valid_input(user_day, valid_day, common_day_alternatives)
        if not is_valid_day:
            print("\nPlease pick from these days?\n(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday).")
        else:
            selected_day.append(corrected_day)
            print("\nThank you! Would you like to select another day?\n")
    if selected_day:
        day = selected_day
    print(f"\nYou selected: {' '.join(day).title()}\n")

    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month(s) to filter by
        (str) day - name of the day(s) of week to filter by
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])


    #view raw data
    view_raw_df = input(f"\nWould you like to see the raw data from {city.title()} (Yes or No):\n").lower().strip()
    if(view_raw_df in ['yes', 'y']):
        print_dataframe_chunks(df)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract year, month, and day of week from Start Time to create new columns
    df['year'] = df['Start Time'].dt.year
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    ## extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # use the index of the months list to get the corresponding int
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = convert_to_1_based_indices(find_indices_sublist(months,month))
 
    # filter by month to create the new dataframe
    df = df[df['month'].isin(month)]

    # filter by day of week if applicable
    days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    day = find_indices_sublist(days,day)
    # filter by day of week to create the new dataframe
    df = df[df['day_of_week'].isin(day)]

    #view filtered data
    view_filtered_df = input(f"\nWould you like to see the filtered data from {city.title()} (Yes or No):\n").lower().strip()
    if(view_filtered_df in ['yes', 'y']):
        print_dataframe_chunks(df)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print(f"Most common month: {translate_month_index_name(popular_month)}")

    # display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    print(f"Most common day of the week: {translate_dow_index_name(popular_dow)}")

    # display the most common start hour
    ## find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print(f"Most common hour: {translate_24hr_index_to_12hr_time(popular_hour)}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_cts = df['Start Station'].value_counts(dropna=False)
    print(f"\nMost common start station: {start_station_cts.idxmax()}\nNumbers of Starts: {start_station_cts.iloc[0]}\n")

    # display most commonly used end station
    end_station_cts = df['End Station'].value_counts(dropna=False)
    print(f"\nMost common stop station: {end_station_cts.idxmax()}\nNumbers of Ends: {end_station_cts.iloc[0]}\n")

    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + ' : ' + df['End Station']
    route_cts = df['Route'].value_counts(dropna=False)
    print(f"\nMost common route: {route_cts.idxmax()}\nNumbers of trips on route: {route_cts.iloc[0]}\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_days = df['Trip Duration'].sum() // (60 * 60 * 24)
    remaining_seconds_less_days = df['Trip Duration'].sum() % (60 * 60 *24)
    remaining_hours =  remaining_seconds_less_days // (60 * 60) 
    remaining_seconds_less_hours = remaining_seconds_less_days % (60 * 60)
    remaining_mins = remaining_seconds_less_hours // 60
    remaining_seconds = remaining_seconds_less_hours % 60
    print(f"Total travel time: {total_days} day(s), {remaining_hours} hour(s), {remaining_mins} minute(s), and {remaining_seconds} second(s)")

    # display mean travel time
    print(f"Mean travel time: {df['Trip Duration'].mean() // 60} minute(s) and {round(df['Trip Duration'].mean() % 60)} second(s)")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_cts = df['User Type'].value_counts(dropna=False)
    user_types_cts = user_types_cts.rename({np.nan: 'Unknown'})
    print("\nUser Types Counts")
    for user_type, utct in user_types_cts.items():
        print(f"{user_type}: {utct}\n")

    # Display counts of gender
    if(city) in ["new york city", "chicago"]:
        gender_cts = df['Gender'].value_counts(dropna=False)
        gender_cts = gender_cts.rename({np.nan: 'Unknown'})
        print("\nGender Counts")
        for gender, gnct in gender_cts.items():
            print(f"{gender}: {gnct}\n")
    else:
        print(f"Gender data is not available for {city.title()}")


    # Display earliest, most recent, and most common year of birth
    if(city) in ["new york city", "chicago"]:
        print(f"\nRider age extremes\nBeware only {df['Birth Year'].notna().sum()} of the {df.shape[0]} riders reported a Birth Year\n")
        max_yob = pd.to_numeric(df['Birth Year'].dropna()).astype('Int64').min()
        min_yob = pd.to_numeric(df['Birth Year'].dropna()).astype('Int64').max()
        mode_yob = pd.to_numeric(df['Birth Year'].dropna()).astype('Int64').mode().iloc[0]
        print(f"The older rider(s) was born in: {max_yob}")
        print(f"The youngest rider(s) was born in: {min_yob}")
        print(f"The most common year of birth was: {mode_yob}")
    else:
        print(f"Birth year data is not available for {city.title()}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
