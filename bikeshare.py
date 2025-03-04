import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': '/mnt/data/chicago.csv',
    'new york city': '/mnt/data/new_york_city.csv',
    'washington': '/mnt/data/washington.csv'
}

def timeit(func):
    """
    Decorator that prints the runtime of the decorated function.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)
        return result
    return wrapper

def get_filters():
    print("Hello! Let's explore some US bikeshare data!")
    
    # Input loops remain the same for simplicity
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington? ").lower()
        if city in CITY_DATA:
            break
        print("Invalid input. Please enter either Chicago, New York City, or Washington.")

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Which month? January, February, March, April, May, June, or All? ").lower()
        if month in months:
            break
        print("Invalid input. Please enter a valid month or 'all'.")

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All? ").lower()
        if day in days:
            break
        print("Invalid input. Please enter a valid day or 'all'.")

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

@timeit
def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    
    most_common_month = df['month'].mode()[0]
    print('Most Common Month:', most_common_month)

    most_common_day = df['day_of_week'].mode()[0]
    print('Most Common Day:', most_common_day)

    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', most_common_hour)

@timeit
def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', most_common_start_station)

    most_common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', most_common_end_station)

    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Common Trip:', most_common_trip)

@timeit
def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)

@timeit
def user_stats(df):
    print('\nCalculating User Stats...\n')
    
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
