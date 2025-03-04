import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': '/mnt/data/chicago.csv',
    'new york city': '/mnt/data/new_york_city.csv',
    'washington': '/mnt/data/washington.csv'
}

def get_valid_input(prompt, valid_options):
    """
    Prompts the user for input until a valid option is entered.
    Converts the input to lowercase before checking.

    Args:
        prompt (str): The prompt to display to the user.
        valid_options (iterable): A collection of valid string options.
    
    Returns:
        str: A valid input chosen by the user.
    """
    while True:
        user_input = input(prompt).lower()
        if user_input in valid_options:
            return user_input
        print("Invalid input. Please choose from: " + ", ".join(valid_options))

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    
    city = get_valid_input(
        "Would you like to see data for Chicago, New York City, or Washington? ",
        list(CITY_DATA.keys())
    )
    
    month = get_valid_input(
        "Which month? January, February, March, April, May, June, or All? ",
        ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    )
    
    day = get_valid_input(
        "Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All? ",
        ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    )
    
    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]

    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].mode()[0]
    print('Most Common Month:', most_common_month)

    most_common_day = df['day_of_week'].mode()[0]
    print('Most Common Day:', most_common_day)

    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', most_common_start_station)

    most_common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', most_common_end_station)

    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Common Trip:', most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nGender Counts:\n', gender_counts)

    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print('\nBirth Year:\n')
        print('Earliest:', earliest_year)
        print('Most Recent:', most_recent_year)
        print('Most Common:', most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_raw_data(df):
    row = 0
    while True:
        display = input('Would you like to see 5 lines of raw data? Enter yes or no: ').lower()
        if display == 'yes':
            print(df.iloc[row:row + 5])
            row += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
