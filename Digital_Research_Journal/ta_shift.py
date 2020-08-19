
#-------------------------------------------------------------------------------------#
#
#    File :                 ta_shifts.py
#    Author :               Greg Furlich
#    Date Created :         2019-06-10
#
#    Purpose: To track submissions to my Digital Research Journal and what Categories were worked on.
#
#    Execution :   python3 ta_shift.py
#
#
#---# Start of Script #---#
import argparse
import os
import calendar_heatmap as cal
import itertools
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import urllib
# from urllib.request import urlopen
import re
from matplotlib.colors import ListedColormap, to_rgba

## Get Delta Shifts Information ##
def ta_shifts(runner):

    print('\n')
    print('### TA Shifts Counts ###')
    print('\n')

    Runner = runner

    gf_run_line = []
    darktime = []
    dayofweek = []
    start_why = []
    end_why = []
    start_date_mst = []
    end_date_mst = []
    start_date_utc = []
    end_date_utc = []
    br_runners = []
    br_logs = []
    lr_runners = []
    lr_logs = []
    md_runners = []
    md_logs = []
    sd_runners = []
    sd_logs = []
    field_shift = []
    field_logs = []
    dates = []

    def site_info(site_info):
        site_logs = ''
        site_runners = ''
        for info in site_info:
            # Log Files
            if '.log' in info:
                site_logs += info
            # Runners #
            else :
                site_runners += info

        if site_runners == '':
            site_runners = 'No Runners'

        if site_logs == '':
            site_logs = 'No Logs'

        return site_runners, site_logs

    # find all Runs with my name #
    years = range(2010,2021)
    for year in years :
        run_page = urllib.urlopen('http://www.telescopearray.org/tawiki/index.php/{0}_Run_Signups'.format(year)).read()
        # run_page = urlopen('http://www.telescopearray.org/tawiki/index.php/{0}_Run_Signups'.format(year)).read()
        run_page_lines = re.split('\n',run_page)

        for line in run_page_lines:
            if Runner in line:
                # print(line)

                # Santize Scrapped Data #
                gf_line = re.split('</td>',line)
                gf_line = [ re.sub('<br />', '\n',column) for column in gf_line]
                gf_line = [ re.sub('<[^>]*>', ' ',column) for column in gf_line]

                # Empty Run
                # (['  '], [' 0.00', '  Tuesday ', '  ', '  y2019m02d20.brm.log \n y2019m02d20.brtax4.log ', '  y2019m02d20.lr.log ', '  y2019m02d20.md.log \n y2019m02d20.tale.log \n y2019m02d20.mdtax4.log ', '  Jesse Warner \n y2019m02d20.sd.log ', ' TAx4 SD deployment\n Robert Cady \n Jihee Kim \n Greg Furlich \n y2019m02d20.maint.log '])

                # Find Run Info Line #
                # print(len(gf_line))
                if (len(gf_line) == 8):

                    gf_run_line.append(gf_line)
                    # print(gf_line)

                    # Get Run Dark Time #
                    darktime.append( re.sub(' ', '', gf_line[0]))

                    # Get Day of Week #
                    dayofweek.append(re.sub(' ', '', gf_line[1]))

                    # Get Run Start and End Date #
                    date = re.split('to',gf_line[2])
                    # print(len(date))

                    # Non run Nights #
                    if (len(date) == 1):
                        start_why.append('No FD Run')
                        end_why.append('No FD Run')
                        start_date_mst.append('No FD Run')
                        end_date_mst.append('No FD Run')
                        start_date_utc.append('No FD Run')
                        end_date_utc.append('No FD Run')

                    # Run Nights #
                    else:
                        start_why.append(re.findall(r'\((.*?)\)', date[0]))
                        end_why.append(re.findall(r'\((.*?)\)', date[-1]))
                        start_mst = re.split('M', date[0])
                        start_mst = start_mst[0].lstrip(' ').rstrip(' ')
                        start_date_mst.append(start_mst)
                        foo = re.split('\n',date[1])
                        end_mst = re.split('M', foo[0])
                        end_mst = end_mst[0].lstrip(' ').rstrip(' ')
                        end_date_mst.append(end_mst)
                        start_utc = re.split('U', foo[1])
                        start_utc = start_utc[0].lstrip(' ').rstrip(' ')
                        start_date_utc.append(start_utc)
                        end_utc = re.split('U', date[2])
                        end_utc = end_utc[0].lstrip(' ').rstrip(' ')
                        end_date_utc.append(end_utc)

                    # BR Info #
                    br_info = re.split('\n',gf_line[3])
                    br_foo_runners, br_foo_logs = site_info(br_info)
                    br_logs.append(br_foo_logs)
                    br_runners.append(br_foo_runners)

                    # LR Info #
                    lr_info = re.split('\n',gf_line[4])
                    lr_foo_runners, lr_foo_logs = site_info(lr_info)
                    lr_logs.append(lr_foo_logs)
                    lr_runners.append(lr_foo_runners)

                    # MD Info #
                    md_info = re.split('\n',gf_line[5])
                    md_foo_runners, md_foo_logs = site_info(md_info)
                    md_logs.append(md_foo_logs)
                    md_runners.append(md_foo_runners)

                    # SD Info #
                    sd_info = re.split('\n',gf_line[6])
                    sd_foo_runners, sd_foo_logs = site_info(sd_info)
                    sd_logs.append(sd_foo_logs)
                    sd_runners.append(sd_foo_runners)

                    # Field Info #
                    field_info = re.split('\n',gf_line[7])
                    field_foo_runners, field_foo_logs = site_info(field_info)
                    field_logs.append(field_foo_logs)
                    field_shift.append(field_foo_runners)

                    # Get Date from Log #
                    foo_date = field_foo_logs.split('.')
                    # print(foo_date)
                    if foo_date[0] != 'No Logs' : y, m, d = re.findall(r'\d+',foo_date[0])
                    else:
                        foo_date = sd_foo_logs.split('.')
                        y, m, d = re.findall(r'\d+',foo_date[0])

                    # print(y,m,d)
                    foo_date = '{0}-{1}-{2}'.format(y,m,d)
                    # print(date)
                    dates.append(foo_date)

    # Create Pandas DataFrame of Shift Info #
    shifts = {
        'Dark Time': darktime,
        'Weekday': dayofweek,
        'Start Reason': start_why,
        'End Reason': end_why,
        'MST Start': start_date_mst,
        'MST End': end_date_mst,
        'UTC_Start': start_date_utc,
        'UTC End': end_date_utc,
        'BR Operators': br_runners,
        'BR Logs': br_logs,
        'LR Operators': lr_runners,
        'LR Logs': lr_logs,
        'MD Operators': md_runners,
        'MD Logs': md_logs,
        'SD Monitor': sd_runners,
        'SD Logs': sd_logs,
        'Field Work': field_shift,
        'Field Logs': field_logs}

    shifts_df = pd.DataFrame(shifts, index=pd.to_datetime(dates))
    # print(shifts_df.index)
    # print(shifts_df.columns)
    # print(shifts_df['MST End'].head())

    # Create Information about when I ran #

    # MD Shifts #
    md_df = pd.DataFrame(shifts_df['Dark Time'][shifts_df['MD Operators'].str.contains(Runner)], index= shifts_df.index[shifts_df['MD Operators'].str.contains(Runner)])
    md_df['Dark Time'] = pd.to_numeric(md_df['Dark Time'])
    print('MD FD Shifts: {0} Total'.format(len(md_df)))
    print(md_df.groupby(md_df.index.year).count())

    # cal.calendar_heatmap(md_df, title='Middle Drum FD Shifts', cbar_title='Run Length', label='0211', cmap='Reds', cbar=False)
    # plt.savefig(parent + 'assets/calendars/MD_calendar.png'.format(cats), bbox_inches='tight')

    # SD Shifts #
    sd_df = pd.DataFrame(shifts_df['SD Monitor'][shifts_df['SD Monitor'].str.contains(Runner)], index= shifts_df.index[shifts_df['SD Monitor'].str.contains(Runner)])
    sd_df['SD Monitor'] = 1
    print('SD Monitor Shifts: {0} Total'.format(len(sd_df)))
    print(sd_df.groupby(sd_df.index.year).count())

    # cal.calendar_heatmap(sd_df, title='SD Monitor Shifts', cbar_title='', label='0211', cmap=ListedColormap([to_rgba('Green', 0.75)]), cbar=False)
    # plt.savefig(parent + 'assets/calendars/SD_calendar.png'.format(cats), bbox_inches='tight')

    # Field Shifts #
    field_df = pd.DataFrame(shifts_df['Field Work'][shifts_df['Field Work'].str.contains(Runner)], index= shifts_df.index[shifts_df['Field Work'].str.contains(Runner)])
    field_df['Field Work'] = 1
    print('Field Shifts: {0} Total'.format(len(field_df)))
    print(field_df.groupby(field_df.index.year).count())

    # cal.calendar_heatmap(field_df, title='Field Shifts', cbar_title='', label='0211', cmap=ListedColormap([to_rgba('Blue', 0.75)]), cbar=False)
    # plt.savefig(parent + 'assets/calendars/Field_calendar.png'.format(cats), bbox_inches='tight')

#---# Main Function #---#
if __name__ == '__main__':

    # Parse script arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--runner', help='Runner', type=str)
    args = parser.parse_args()

    # Execute TAx4 FD North Processing of Part #
    try:
        ta_shifts(args.runner)
    except Exception as err:
        print('Error encountered: {0}'.format(err))

#---# End of Script #---#
