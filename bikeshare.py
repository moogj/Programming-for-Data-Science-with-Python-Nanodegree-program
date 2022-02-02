import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Choose a city where you want to see data from (Chicago, New York City or Washington) : ')
    city = city.casefold()
    while city not in CITY_DATA:
        city = input('Invalid response. Please try again.')
        city = city.casefold()

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('Please type in the month name or "all" to select all months : ')
    month = month.casefold()
    while month not in months:
        month = input('Invalid response. Please try again.')
        month = month.casefold()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('Please type in a day or "all" to select all days : ')
    day = day.casefold()
    while day not in days:
        day = input('Invalid response. Please try again.')
        day = day.casefold()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime type
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding integer
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        # month output as integer
        month = months.index(month) + 1
        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    # Extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month
    # Find the most common month of the year from 1 to 12
    popular_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('Most common month:', months[popular_month-1])

    # TO DO: display the most common day of week
    # Extract day_of_week from the Start Time column to create a day_of_week column
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    # Find the most common day of the week
    popular_day = df['day_of_week'].mode()[0]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print('Most common day:', days[popular_day])

    # TO DO: display the most common start hour
    # Extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # Find the most common hour
    popular_hour = df['hour'].mode()[0]
    print('Most common start hour:', popular_hour)

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most commonly used start station: ', df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('Most commonly used end station: ', df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    print('\nMost frequent combination of start station and end station trips:\n\n',df.groupby(['Start Station', 'End Station']).size().nlargest(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time:', df['Trip Duration'].sum())

    # TO DO: display mean travel time
    print('Mean travel time:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types,'\n')

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender,'\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of birth:', df['Birth Year'].min())
        print('Most recent year of birth:', df['Birth Year'].max())
        print('Most common year of birth:', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        #Display a prompt where the user can decide if the user would like to see more data
        enter = ['yes','no']
        user_input = input('Would you like to see more data? Enter: Yes or No.\n')

        while user_input.lower() not in enter:
            user_input = input('Please enter Yes or No:\n')
            user_input = user_input.lower()
        n = 0
        while True :
            if user_input.lower() == 'yes':

                print(df.iloc[n : n + 5])
                n += 5
                user_input = input('\nWould you like to see more data? Enter: Yes or No.\n')
                while user_input.lower() not in enter:
                    user_input = input('Please enter Yes or No:\n')
                    user_input = user_input.lower()
            else:
                break

        restart = input('\nWould you like to restart? Enter: Yes or No.\n')
        #Check if the user enters a valid entry
        while restart.lower() not in enter:
            restart = input('Please enter Yes or No:\n')
            restart = restart.lower()
        if restart.lower() != 'yes':
            print('Hope to see you again.')
            break


if __name__ == "__main__":
	main()
