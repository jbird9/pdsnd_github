import time
import pandas as pd
import numpy as np
import config

def get_user_inputs(input_type, valid_options):
    """
    Allows the user to enter multiple values (e.g., days or months) and collects them in a list.
    If no input is provided, defaults to all options.
    """
    inputs = []
    prompt = f"Please enter one {input_type} at a time ({", ".join(list(valid_options.keys())).title()}) or type 'done' to finish. Press Enter to select all: "
    print(prompt)

    while True:
        user_input = input(f"Enter a {input_type}, or type 'done' to finish: ").lower().strip()
        if user_input == 'done' or user_input == '':
            if not inputs:  # No inputs collected, default to all
                inputs = list(valid_options.keys())
                print(f"All {input_type}s have been selected.")
            break

        # Check each possible key and its synonyms in the dictionary
        found = False
        for key, synonyms in valid_options.items():
            if user_input in synonyms:
                if key not in inputs:
                    inputs.append(key)
                    print(f"{key.title()} added. You can add more or type 'done' to finish.")
                else:
                    print(f"{key.title()} is already added. Please enter another or type 'done'.")
                found = True
                break

        if not found and user_input:
            print(f"Invalid {input_type}. Please try again using valid options.")

    return inputs

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
    
# Translate 24 hour index to 12 hour time
def translate_24hr_index_to_12hr_time(hour_index):
    """Formats hour index into 12 hour time with AM/PM marker"""
    if 0 <= hour_index <= 23:
        # Create timestamp that contains the hour being indexed
        timestamp = pd.Timestamp.today().replace(hour=hour_index, minute=0, second=0, microsecond=0)
        time_12hr = timestamp.strftime('%I:%M %p')
        return time_12hr

def load_data(cities, months, days, CITY_DATA_FILES):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city(ies) to analyze
        (str) month - name of the month(s) to filter by
        (str) day - name of the day(s) of week to filter by
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    dfs = []
    for city in cities:
        if city in CITY_DATA_FILES:
            # load data from a city
            df = pd.read_csv(CITY_DATA_FILES[city])

            # Handle missing gender and birth year data if Washington is selected
            if city == 'Washington':
                df['Gender'] = np.nan
                df['Birth Year'] = np.nan
            dfs.append(df)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract year, month, and day of week from Start Time to create new columns
    df['year'] = df['Start Time'].dt.year
    df['month'] = df['Start Time'].dt.strftime('%B').str.lower()  # Use strftime('%B') for month names
    df['day_of_week'] = df['Start Time'].dt.strftime('%A').str.lower()  # Use strftime('%A') for day names


    ## extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # view raw data
    view_raw_df = input(f"\nWould you like to see the raw data from {' AND '.join(str(c).title() for c in cities)} (Yes or No):\n").lower().strip()
    if(view_raw_df in ['yes', 'y']):
        print_dataframe_chunks(df)

    ## filter selected months
    if months:
        df = df[df['month'].isin(months)]

    ## filter selected days
    if days:
        df = df[df['day_of_week'].isin(days)]

    #view filtered data
    view_filtered_df = input(f"\nWould you like to see the filtered data from\n{' AND '.join(str(c).title() for c in cities)}\n{' AND '.join(str(m).title() for m in months)}\n{' AND '.join(str(d).title() for d in days)}\n(Yes or No):\n").lower().strip()
    if(view_filtered_df in ['yes', 'y']):
        print_dataframe_chunks(df)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print(f"Most common month: {popular_month.title()}")

    # display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    print(f"Most common day of the week: {popular_dow.title()}")

    # display the most common start hour
    ## find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print(f"Most common hour: {translate_24hr_index_to_12hr_time(popular_hour)}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # display most commonly used start station
    start_station_cts = df['Start Station'].value_counts(dropna=False)
    print(f"\nMost common start station: {start_station_cts.idxmax()}\nNumbers of Starts: {start_station_cts.iloc[0]}")

    # display most commonly used end station
    end_station_cts = df['End Station'].value_counts(dropna=False)
    print(f"\nMost common stop station: {end_station_cts.idxmax()}\nNumbers of Ends: {end_station_cts.iloc[0]}")

    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + ' : ' + df['End Station']
    route_cts = df['Route'].value_counts(dropna=False)
    print(f"\nMost common route: {route_cts.idxmax()}\nNumbers of trips on route: {route_cts.iloc[0]}")

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


def user_stats(df, cities):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    user_types_cts = df['User Type'].value_counts(dropna=False)
    user_types_cts = user_types_cts.rename({np.nan: 'Unknown'})
    print("\nUser Types Counts")
    for user_type, utct in user_types_cts.items():
        print(f"{user_type}: {utct}")

    # Display counts of gender
    if("washington") in cities:
        print(f"\nGender data is not available for Washington")
    else:
        gender_cts = df['Gender'].value_counts(dropna=False)
        gender_cts = gender_cts.rename({np.nan: 'Unknown'})
        print(f"\nGender Counts")
        for gender, gnct in gender_cts.items():
            print(f"{gender}: {gnct}")
    



    # Display earliest, most recent, and most common year of birth
    if("washington") in cities:
        print(f"Birth year data is not available for Washington")
    else:
        print(f"\nRider age extremes\nBeware only {df['Birth Year'].notna().sum()} of the {df.shape[0]} riders reported a Birth Year\n")
        max_yob = pd.to_numeric(df['Birth Year'].dropna()).astype('Int64').min()
        min_yob = pd.to_numeric(df['Birth Year'].dropna()).astype('Int64').max()
        mode_yob = pd.to_numeric(df['Birth Year'].dropna()).astype('Int64').mode().iloc[0]
        print(f"The oldeest rider(s) was born in: {max_yob}")
        print(f"The youngest rider(s) was born in: {min_yob}")
        print(f"The most common year of birth was: {mode_yob}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
#        city, month, day = get_filters()
        print('Hello! Let\'s explore some US bikeshare data!')
        cities = get_user_inputs("city", config.CITIES)
        print(f"Selected cities: {" ".join(cities).title()}")
        months = get_user_inputs("month", config.MONTHS)
        print(f"Selected months: {" ".join(months).title()}")
        days = get_user_inputs("day of the week", config.DAYS)
        print(f"Selected days: {" ".join(days).title()}")
        df = load_data(cities, months, days, config.CITY_DATA)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, cities)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
