import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_list = ["january","february","march","april","may","june","all"]
day_list = ["saturday" , "sunday" , "monday" , "tuesday" , "wednesday" , "thursday" , "friday" , "all" ]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city_bool, month_bool, day_bool = False, False, False

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        if not city_bool:
            city = input("choose one of the three cities to explore chicago, new york city or washington \n")
            city = city.lower()
            if city not in CITY_DATA:
                print("please re_enter you city correctly")
                continue
            else:
                city_bool = True
        print("/n")

        # get user input for month (all, january, february, ... , june)
        if not month_bool:
            month = input("choose month to explore from january to june, all to explore all 6 months ")
            month = month.lower()
            if month not in month_list:
                print("please re_enter the month correctly")
                continue
            else:
                month_bool = True
        print("/n")

        # get user input for day of week (all, monday, tuesday, ... sunday)
        if not day_bool:
            day = input("choose day to explore , all to explore all days ")
            day = day.lower()
            if day not in day_list:
                print("please re_enter the day correctly")
                continue
            else:
                break

    print('-' * 40)
    print("/n")
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
    start_time = time.time()
    df = pd.read_csv(CITY_DATA.get(city), parse_dates=["Start Time", "End Time"])
    df["Start Month"], df["Start Day"], df["Start Hour"] = (
        df["Start Time"].dt.month_name(),
        df["Start Time"].dt.day_name(),
        df["Start Time"].dt.hour,
    )

    if month != "all":
        df = df[df["Start Month"] == month]
    if day != "all":
        df = df[df["Start Day"] == day]
    print("filtered")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    if month == "all":
        # most_popular_month = df["Start Month"].dropna()
        '''if most_popular_month.empty:
            print("no popular month found")
        else:'''
        most_popular_month = df["Start Month"].mode()[0]
        print("most popular month is : {}".format(most_popular_month))
    else:
        print("select all to get the most popular month")
    # display the most common day of week
    if day == "all":
        '''most_common_day = df["Start Day"].dropna()
        if most_common_day.empty:
            print("no common day found")
        else:'''
        most_common_day = df["Start Day"].mode()[0]
        print("most common day is : {}".format(most_common_day))
    else:
        print("select all to get the most common day ")

    # display the most common start hour
    most_popular_hour = df["Start Hour"].dropna()
    if most_popular_hour.empty:
        print("please refilter your data")
    else:
        most_popular_hour = most_popular_hour.mode()[0]
        print("most popular start hour is : {} hrs".format(most_popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # most_commonly_start_station = df["Start Station"]
    '''if most_commonly_start_station.empty :
        print("no most commonly used start station found , refilter your data")
    else:'''
    most_commonly_start_station = df["Start Station"].mode()[0]
    print("most popular start station is : {}".format(most_commonly_start_station))

    # display most commonly used end station
    '''most_commonly_end_station = df["End Station"].dropna
    if most_commonly_end_station.empty :
        print("no most commonly used end station found , refilter your data")
    else:'''
    most_commonly_end_station = df["End Station"].mode()[0]
    print("most popular end station is : {}".format(most_commonly_end_station))

    # display most frequent combination of start station and end station trip
    '''most_common_combination = df[["Start Station","End Station"]].dropna()
    if most_common_combination.empty:
        print("no data , please refilter the data again")
    else:'''
    most_common_combination = df[["Start Station", "End Station"]].groupby(
        ["Start Station", "End Station"]).size().sort_values(ascending=False)
    trip_count = most_common_combination.iloc[0]
    stations = most_common_combination[most_common_combination == trip_count].index[0]
    start_staion, end_station = stations
    print("most frequent start station is : ", start_staion, " and end station is : ", end_station,
          "which were part of ", trip_count, "trips")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df["Trip Duration"].dropna()
    if travel_time.empty:
        print("no data found , refilter your data")
    else:
        total_travel_time = travel_time.sum() / 60
        print("total travel time in minets is : {}".format(total_travel_time))

        # display mean travel time
        mean_travel_time = travel_time.mean() / 60
        print("mean travel time in minets is : {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_type = df["User Type"].dropna()
    if user_type.empty:
        print("no data , refilter your data  ")
    else:
        user_type = user_type.value_counts()
        print("user type counts : {}".format(user_type))

        # Display counts of gender
        if "Gender" in df:
            ''' user_gender = df["Gender"].dropna
            if user_gender.empty :
            print("no data , refilter your data")
            else:'''
            user_gender = df["Gender"].value_counts()
            print("counts of gender is : {}".format(user_gender))

            # Display earliest, most recent, and most common year of birth
        if "Birth Year" in df:
            birth_year = df["Birth Year"].dropna()
            if birth_year.empty:
                print("no data , refilter your data")
            else:
                earlier = birth_year.min()
                print("earliest birth year is : {}".format(int(earlier)))
                recent = birth_year.max()
                print("most recent birth year is : {}".format(int(recent)))
                common_year = birth_year.mode()[0]
                print("the most common year of birth is : {}".format(int(common_year)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_raw_data(df):
    choice = input("would ypu like to see raw data ? {yes,no} :")

    count = 0
    if choice.lower() == "yes":
        for row in df.iterrows():
            print(row)
            count += 1
            if count != 0 and count % 5 == 0:
                choice = input("would ypu like to see raw data ? {yes,no} :")
                if choice.lower() != "yes":
                    break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
