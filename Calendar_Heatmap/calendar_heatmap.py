#-------------------------------------------------------------------------------------#
#
#    File :             calendar_heatmap.py
#    Author :           Greg Furlich
#    Date Created :     2019-03-12
#
#    Purpose:           Python function library for calendar heatmap plots
#
#    Execution :        import calendar_heatmap as cal
#
#    Sources :          https://stackoverflow.com/questions/32485907/matplotlib-and-numpy-create-a-calendar-heatmap
#                       https://github.com/martijnvermaat/calmap/blob/master/calmap/__init__.py
#
#---# Start of Script #---#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import datetime
# from datetime import datetime

def calendar_heatmap(df,
                    title,
                    cbar_title,
                    orientation='h',
                    cmap='summer',
                    norm = None,
                    fill_color='lightgray',
                    size=2,
                    w=8,
                    h=1.4,
                    label='1111',
                    cbar=True):

    '''
    # Description #
    Add date's numeric label of month ontop of date's square according to row and column information from wekk and dayofweek.

    # Parameters #
    df :            pandas DataFrame with DatetimeIndex indexed by day and corresponding data to plot in only column
    title :         Title of Calendar
    cbar_title :    Lable of Colorbar
    orientation :   Orientation of Calendar.
                    'h' or 'horizontal' for horizontal calendar, and 'v' or 'vertical' for vertical calendar.
                    Default is horizontal.
    cmap :          Colormap of Calendar.
                    Default is 'summer'.
    fill_color :    Fill color of empty dates of a year.
                    Default is 'lightgray'.
    size:           Size to increase dimnesions of the plot by.
                    Default is 2x increase.
    w :             Long side of calendar year box.
                    Default is 8.
    h :             Short side of calendar year box.
                    Default is 1.4.
    label :         Label Options of Calendar.
                    Default is '1111'.
                    Options are usually '2' is long, '1' for short or on, '0' for off.
                    label[0] is for date_label options [2-0],
                    label[1] for day_label options [2-0],
                    label[2] for month_label options [1-0],
                    label[3] for year_label options [1-0].
    cbar :          Turn on/off Colorbar. Default if 'True')

    # Returns #
    f :     calendar map figure
    ax :    axis or list of axes of each year's calendar heatmap of date range

    '''

    # General Variables #
    years = list(df.index.year.unique())

    # Figure Aspect Size #
    w, h = w, h*len(years)
    size = size

    # Set Label Options #
    # Label Options : 2 for long, 1 for short, 0 for off
    date_label = label[0]
    day_label = label[1]
    month_label = label[2]
    year_label = label[3]

    # Generate Calendar Array #
    calendar, emptycalendar, cal_df = calendar_array(df, orientation)

    # get max and min of array #
    vmin = cal_df.data.min()
    vmax = cal_df.data.max()

    # Create Plots with desired orientation #

    # Single Year Case #
    if len(years) == 1 :

        if ((orientation == 'vertical') | (orientation == 'v')) :
            f, ax = plt.subplots( figsize=(size * h,size * w))

        # Horizontal Calendar
        elif ((orientation == 'horizontal') | (orientation == 'h')) :
            f, ax = plt.subplots( figsize=(size * w,size * h))

        # Fill Calendar dates :
        ax.pcolormesh(emptycalendar[0], vmin=0, vmax=1, cmap=ListedColormap([fill_color]))

        # Fill Calendar with data :
        if norm :
            im = ax.pcolormesh(calendar[0], cmap=cmap, vmin=vmin, vmax=vmax, norm=norm, linewidth=1, edgecolors='white')
        else :
            im = ax.pcolormesh(calendar[0], cmap=cmap, vmin=vmin, vmax=vmax, linewidth=1, edgecolors='white')

        # Set Calendar with Sunday on top for horizontal or Jan on top for vertical and set aspect ratio
        ax.set_aspect('equal')
        ax.invert_yaxis()

        # Label Calendar Dates :
        if ( date_label == '2'):
            label_dates(ax, 0, cal_df, orientation, length='all', date_color='w')
        elif ( date_label == '1'):
            label_dates(ax, 0, cal_df, orientation, length='data', date_color='w')

        # Label Calendar days axis :
        if (day_label == '2') :
            label_days(ax, orientation, 'long')
        if (day_label == '1') :
            label_days(ax, orientation, 'short')

        # Label Calendar Months axis :
        if (month_label == '1') :
            label_months(ax, cal_df, orientation)

        if (year_label == '1') :
            label_years(ax, 0, cal_df, orientation)

        # turn off Subplot Frame #
        ax.set_frame_on(False)

        if cbar == True :
            calendar_single_colorbar(f, im, cbar_title, orientation)

    # Multiyear Case #
    else :

        # Vertical Calendar #
        if ((orientation == 'vertical') | (orientation == 'v')) :
            f, ax = plt.subplots(1, len(years), figsize=(size * h,size * w))

        # Horizontal Calendar #
        elif ((orientation == 'horizontal') | (orientation == 'h')) :
            f, ax = plt.subplots(len(years), 1, figsize=(size * w,size * h))

        # Plot All Years of Data #
        for i in range(len(years)):

            # Fill Calendar dates :
            ax[i].pcolormesh(emptycalendar[i], cmap=ListedColormap([fill_color]))

            # Fill Calendar with data :
            im = ax[i].pcolormesh(calendar[i], cmap=cmap, vmin=vmin, vmax=vmax, linewidth=1, edgecolors='white')

            # Set Calendar with Sunday on top for horizontal or Jan on top for vertical and set aspect ratio
            ax[i].set_aspect('equal')
            ax[i].invert_yaxis()

            # Label Calendar Dates :
            if ( date_label == '2'):
                label_dates(ax[i], i, cal_df, orientation, length='all', date_color='w')
            elif ( date_label == '1'):
                label_dates(ax[i], i, cal_df, orientation, length='data', date_color='w')

            # Label Calendar days axis :
            if (day_label == '2') :
                label_days(ax[i], orientation, 'long')
            if (day_label == '1') :
                label_days(ax[i], orientation, 'short')

            # Label Calendar Months axis :
            if (month_label == '1') :
                label_months(ax[i], cal_df, orientation)

            if (year_label == '1') :
                label_years(ax[i], i, cal_df, orientation)

            # turn off Subplot Frame #
            ax[i].set_frame_on(False)

        # Add Colorbar #
        if cbar == True :
            calendar_colorbar(f, im, cbar_title, orientation)

    # Calendar Title :
    f.suptitle(title, y=.9, x=0.5, fontsize=18, horizontalalignment='center', verticalalignment='center')

    # Return Calendar Figure and axes #
    return f, ax

def label_dates(ax, i, cal_df, orientation, length, date_color):
    '''
    # Description #
    Add date's numeric label of month ontop of date's square according to row and column information from wekk and dayofweek.

    # Parameters #
    ax :            subplot axis to add year label to
    i :             index of year corresponding to index of axis in axes
    cal_df :        Pandas DataFrame of calendar heatmap data and dates
    orientation :   orientation of the titlebar to match the orientation of the calendar. 'h' or 'horizontal' for horizontal calendar, and 'v' or 'vertical' for vertical calendar
    length :        Verbosity of date labels. 'all' referes to labeling all dates of the year and 'data' refers to label only dates with data.
    date_color :    Set font color of dates.

    # Returns #
    None

    '''

    # Get Range of Years of Data :
    years = list(cal_df.index.year.unique())

    # Display Settings :
    if (length == 'all'):
        year_cal_df = cal_df[(cal_df.index.year ==  years[i])]
    elif (length == 'data'):
        year_cal_df = cal_df[(cal_df.index.year ==  years[i]) & ( np.logical_not(cal_df.data.isnull()))]

    # Calendar Orientation :
    if ((orientation == 'vertical') | (orientation == 'v')) :
        for j in range(len(year_cal_df)):
            ax.text(year_cal_df.dayofweek[j]+ .5, year_cal_df.week[j] + .5, year_cal_df.index.day[j], horizontalalignment='center', verticalalignment='center', color=date_color)

    elif ((orientation == 'horizontal') | (orientation == 'h')) :
        for j in range(len(year_cal_df)):
            ax.text(year_cal_df.week[j] + .5, year_cal_df.dayofweek[j] + .5, year_cal_df.index.day[j], horizontalalignment='center', verticalalignment='center', color=date_color)

def label_days(ax, orientation, length):
    '''
    # Description #
    Add a day labels next to each year heatmap

    # Parameters #
    ax :            subplot axis to add year label to
    orientation :   orientation of the calendar. 'h' or 'horizontal' for horizontal calendar, and 'v' or 'vertical' for vertical calendar
    length :        Verbosity of day label

    # Returns #
    None

    '''

    # Short Display Length #
    if ((length == 's' ) | (length == 'short')) : labels=['M', 'T', 'W', 'R', 'F', 'S', 'S']

    # Long Display Length #
    elif ((length == 'l' ) | (length == 'long')) : labels=['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']

    # Vertical Calendar Day Labels #
    if ((orientation == 'vertical') | (orientation == 'v')) :
        ax.set(xticks=np.arange(7)+.5)

        # Short display labels orientation, since single letter, keep upright #
        if ((length == 's' ) | (length == 'short')) : ax.set_xticklabels(labels)

        # Long Display lables orientaion #
        elif ((length == 'l' ) | (length == 'long')) : ax.set_xticklabels(labels, rotation=90)

        ax.xaxis.tick_top()
        ax.tick_params(axis='both', which='both', length=0)

    # Horizontal Calendar Day Labels #
    elif ((orientation == 'horizontal') | (orientation == 'h')) :
        ax.set(yticks=np.arange(7)+.5, yticklabels=labels)
        ax.yaxis.tick_right()
        ax.tick_params(axis='both', which='both', length=0)

def label_months(ax, cal_df, orientation):
    '''
    # Description #
    Add a month labels next to each year heatmap

    # Parameters #
    ax :            subplot axis to add year label to
    cal_df :        Pandas DataFrame of calendar heatmap data and dates
    orientation :   orientation of the calendar. 'h' or 'horizontal' for horizontal calendar, and 'v' or 'vertical' for vertical calendar

    # Returns #
    None

    '''

    # Month Labels #
    month_labels = np.array(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    # Generate Month Tick Placement #
    months = np.array([d.month for d in cal_df.index])
    uniq_months = sorted(set(months))
    ticks = [cal_df.week[months == m].mean() for m in uniq_months]

    # Vertical Calendar Month Labels #
    if ((orientation == 'vertical') | (orientation == 'v')) :
        ax.set_yticklabels(month_labels)
        ax.set(yticks=ticks)
        ax.tick_params(axis='both', which='both', length=0)

    # Horizontal Calendar Month Labels #
    elif ((orientation == 'horizontal') | (orientation == 'h')) :
        ax.set(xticks=ticks)
        ax.set_xticklabels(month_labels)

def label_years(ax, i, cal_df, orientation):
    '''
    # Description #
    Add a year label next to each year heatmap

    # Parameters #
    f :             figure
    ax :            subplot axis to add year label to
    i :             index of year corresponding to index of axis in axes
    cal_df :        Pandas DataFrame of calendar heatmap data and dates
    orientation :   orientation of the calendar. 'h' or 'horizontal' for horizontal calendar, and 'v' or 'vertical' for vertical calendar

    # Returns #
    None

    '''

    # Get Range of Years of Data #
    years = list(cal_df.index.year.unique())

    # Get Year #
    year = str(years[i])

    # Vertical Calendar Year Label #
    if ((orientation == 'vertical') | (orientation == 'v')) :
        ax.set_title(year, rotation='vertical',x=-0.3,y=0.5)

    # Horizontal Calendar Year Label #
    elif ((orientation == 'horizontal') | (orientation == 'h')) :
        ax.set_title(year)

def calendar_colorbar(f, im, cbar_title, orientation):
    '''
    # Description #
    Add a colorbar to the calendar map for reference of the calendar heatmap magnitude

    # Parameters #
    f :             figure
    im :            pcolormesh plot to create a colorbar from
    cbar_title :    Color Bar Label
    cbar_labels :   optional cbaer labels on long side of axis
    orientation :   orientation of the titlebar to match the orientation of the calendar. 'h' or 'horizontal' for horizontal calendar, and 'v' or 'vertical' for vertical calendar

    # Returns #
    None

    '''

    # Horizontal Calendar Colorbar #
    if ((orientation == 'horizontal') | (orientation == 'h')) :

        # Place on right of calendar #
        cbar_xo, cbar_yo = .85, .25
        cbar_w, cbar_h = .015, .5
        plt.subplots_adjust(right=0.8)
        cbar_ax = f.add_axes([cbar_xo, cbar_yo, cbar_w, cbar_h])
        cbar = f.colorbar(im, cax=cbar_ax)

        # Add Colorbar Label to right of Colorbar #
        cbar_ax.text( 3.5, .5, cbar_title, horizontalalignment='center', verticalalignment='center', rotation=270)

    # Vertical Calendar Colorbar #
    elif ((orientation == 'vertical') | (orientation == 'v')) :

        # Place on bottom of calendar #
        cbar_xo, cbar_yo = .25, 0.1
        cbar_w, cbar_h = .5, .015
        cbar_ax = f.add_axes([cbar_xo, cbar_yo, cbar_w, cbar_h])
        cbar = f.colorbar(im, cax=cbar_ax, orientation='horizontal')

        # Add Colorbar Label below Colorbar #
        cbar_ax.text( .5, -1.5, cbar_title, horizontalalignment='center', verticalalignment='center')

def calendar_single_colorbar(f, im, cbar_title, orientation):
    '''
    # Description #
    Add a colorbar to the calendar map in the case of only one year of data. Added as there seems to be a bug in using calendar_colorbar() with one year.

    # Parameters #
    f :             figure
    im :            pcolormesh plot to create a colorbar from
    cbar_title :    Color Bar Label
    orientation :   orientation of the titlebar to match the orientation of the calendar

    # Returns #
    None

    '''

    # Horizontal Calendar Colorbar #
    if ((orientation == 'horizontal') | (orientation == 'h')) :

        # Place on right of calendar #
        cbar_xo, cbar_yo = .85, .25
        cbar_w, cbar_h = .015, .5
        plt.subplots_adjust(right=0.8)
        cbar_ax = f.add_axes([cbar_xo, cbar_yo, cbar_w, cbar_h])
        cbar = f.colorbar(im, cax=cbar_ax)

        # Add Colorbar Label to right of Colorbar #
        cbar_ax.text( 12.5, 4, cbar_title, horizontalalignment='center', verticalalignment='center', rotation=270)

    # Vertical Calendar Colorbar #
    elif ((orientation == 'vertical') | (orientation == 'v')) :

        # Place on bottom of calendar #
        cbar_xo, cbar_yo = .25, 0.1
        cbar_w, cbar_h = .5, .015
        cbar_ax = f.add_axes([cbar_xo, cbar_yo, cbar_w, cbar_h])
        cbar = f.colorbar(im, cax=cbar_ax, orientation='horizontal')

        # Add Colorbar Label below Colorbar #
        cbar_ax.text( .5, -1.5, cbar_title, horizontalalignment='center', verticalalignment='center')

def calendar_array(df, orientation):
    '''
    # Description #
    Convert a Pandas DataFrame with DatetimeIndex into list of numpy arrays representing a heatmap of a calendar year.

    # Parameters #
    df :            pandas DataFrame with DatetimeIndex indexed by day and corresponding data to plot in only column
    orientation :   desired orientation of calander to reflect in calendar array

    # Returns #
    filled_calendar :   list of numpy arrays for each year of the calendar. Each array has the data to be ploted assined by row and column corresponding to orientation of week and day of week
    empty_calendar :    list of numpy arrays for each year of the calendar. Each array element is filled with 1 to signify that is a date of the year in that calendar for ploting each date of the year even if it has no data
    cal_df :            Pandas DataFrame which copies input df and calculates dayofweek and week from datetime index for row and col info for arrays

    '''

    # General Variables :
    days_in_week = 7

    # Get Range of Years #
    years = list(df.index.year.unique())

    # Create DataFrame of all dates over the range of data years
    cal_df = df.reindex(pd.date_range(start=str(min(years)), end=str(max(years) + 1), freq='D')[:-1])
    cal_df = pd.DataFrame({'data': cal_df.iloc[:,0],
                        'fill': 1,
                        'dayofweek': cal_df.index.dayofweek,
                        'week': cal_df.index.week})

    # Reset First Week if alignment with last year's last week :
    cal_df.loc[(cal_df.index.month == 1) & (cal_df.week > 50), 'week'] = 0

    # Reset Last Week if alignment with next year's first week :
    cal_df.loc[(cal_df.index.month == 12) & (cal_df.week < 10), 'week'] = cal_df.week.max() + 1

    # Reset Last Week if alignment with next year's first week :
#     cal_df.loc[(cal_df.index.year == 12) & (cal_df.week.min() == 1), 'week'] = cal_df.week - 1

    # Since a year might have varying shape, a list of the year's calendar will be appended
    filled_calendar = []
    empty_calendar = []

    # Create Calendar Array from dataframe #
    for year in years :

        year_cal_df = cal_df[cal_df.index.year == year]

    # Vertical Calandar
        if ((orientation == 'vertical') | (orientation == 'v')) :

            nrows, ncols = year_cal_df.week.max() + 1, days_in_week
            year_calendar = np.nan * np.zeros((nrows, ncols))
            empty_year_calendar = np.nan * np.zeros((nrows, ncols))

            data = year_cal_df.data
            fill = year_cal_df.fill
            rows = year_cal_df.week
            cols = year_cal_df.dayofweek

            for (data,fill, row,col) in zip(data,fill,rows,cols) :
                year_calendar[row,col] = data
                empty_year_calendar[row,col] = fill

            # Append to calendar list
            filled_calendar.append(year_calendar)
            empty_calendar.append(empty_year_calendar)

        # Horizontal Calander
        elif ((orientation == 'horizontal') | (orientation == 'h')) :

            nrows, ncols =  days_in_week, year_cal_df.week.max() + 1
            year_calendar = np.nan * np.zeros((nrows, ncols))
            empty_year_calendar = np.nan * np.zeros((nrows, ncols))

            data = year_cal_df.data
            fill = year_cal_df.fill
            rows = year_cal_df.dayofweek
            cols = year_cal_df.week

            for (data,fill,row,col) in zip(data,fill,rows,cols) :
                year_calendar[row,col] = data
                empty_year_calendar[row,col] = fill

            # Append to calendar list
            filled_calendar.append(year_calendar)
            empty_calendar.append(empty_year_calendar)

    return filled_calendar, empty_calendar, cal_df

def generate_example_data(start_time, end_time, rand_min = 0, rand_max = 10 ):
    '''
    # Description #
    Generate example pandas DataFrame of random values for each day from start_date to end_date with a DatetimeIndex to use with the calendar_heatmap()

    # Parameters #
    start_time : datetime.datetime value of initial date to start data generation
    end_time : datetime.datetime value of final date of data generation
    random_range : Range of Values for random ints

    # Returns #
    df : pandas DataFrame of DatetimeIndex randomly generated data

    # Example Usage #
    start_date = dt.strptime('2017-10-01', '%Y-%m-%d')
    end_date = dt.strptime('2019-06-30', '%Y-%m-%d')
    df = generate_example_data(start_date, end_date)

    '''

    # Calculate data range #
    ndays = (end_time-start_time).days

    # Generate Random Data #
    data = np.random.randint(rand_min, rand_max, ndays)

    # Generate data dates #
    dates = [start_time + datetime.timedelta(days=i) for i in range(ndays)]

    # Create Pandas DataFrame from randomly generated data #
    df = pd.DataFrame({'data':data}, index=dates)

    return df
