#-------------------------------------------------------------------------------------#
#
#    File :                 post_stats.py
#    Author :               Greg Furlich
#    Date Created :         2019-02-28
#
#    Purpose: To track submissions to my Digital Research Journal and what Categories were worked on.
#
#    Execution :   python3 post_stats.py
#
#
#---# Start of Script #---#

import os
import calendar_heatmap as cal
import itertools
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import urllib
import re
from matplotlib.colors import ListedColormap, to_rgba

parent = '/GDF/gf_research_journal/'
git_log =  parent + 'assets/git.log'
cat_file = parent + '_site/categories/index.html'
stats_file = parent + 'stats.html'

## Git Stats ##
print('### Digital Journal Git Submissions Info ###')
print('\n')
# Dump Git Log #
os.system('git log > {0}'.format(git_log))

# Parse Git Log #
f = open(git_log, 'r')
# nlines = len(f.readlines())
lines=[]
for line in f.readlines():
    lines.append(line)
# print(lines)

commit_id = lines[0::6]
commit_author = lines[1::6]
commit_dates = lines[2::6]
commit_m = lines[4::6]

commit_id = [i.strip('\n').strip('commit ') for i in commit_id ]
commit_author = [i.strip('\n').strip('Author: ') for i in commit_author ]
commit_dates = [i.strip('\n').strip('Date:    ').split('-')[0] for i in commit_dates ]
commit_m = [i.strip('\n').strip('     ') for i in commit_m ]

# create dataframe of data
# print(commit_dates)
git_df = pd.DataFrame({'commit_times':pd.to_datetime(commit_dates)}, index=pd.to_datetime(commit_dates).date)
git_df.index = pd.to_datetime(git_df.index)
# print(git_df)

def mean_time(time):
    sum = 0
    for i in range(len(time)):
        sum += time[i].hour + time[i].minute / 60 + time[i].second / 3600
    mean = sum / len(time)
    mean_hour = int(mean // 1)
    mean_min = int((mean - mean_hour ) * 60 // 1)
    mean_sec = int((mean - mean_hour - mean_min/60 ) * 3600 // 1)

    # return '{0} {1}:{2}:{3}'.format(mean, mean_hour, mean_min, mean_sec)
    return '{1}:{2}:{3}'.format(mean, mean_hour, mean_min, mean_sec)

# Aggregate data info
# print(git_df['commit_times'].dt.time.groupby(git_df['commit_times'].dt.date).agg(['max', 'min']))
# print(git_df['commit_times'].dt.time.groupby(git_df['commit_times'].dt.date).apply(mean_time))
# print(git_df.groupby(git_df['commit_times'].dt.date)['commit_times'].map( lambda x: x.dt.hour))
# print(git_df['commit_times'].dt.date.value_counts())

# Get Counts for each date
counts = pd.DataFrame({'counts':git_df['commit_times'].dt.date.value_counts()}, index=git_df.index.unique())
counts = counts.sort_index(ascending=True)
print(counts.head())

# all_days = pd.date_range('1/15/2014', periods=700, freq='D')
# days = np.random.choice(all_days, 500)
# events = pd.Series(np.random.randn(len(days)), index=days)

cal.calendar_heatmap(counts, title='Research Journal Git Commits', cbar_title='Commits a day', label='0211', cmap='Greens', cbar=False)
plt.savefig(parent + 'assets/git_contributions.png', bbox_inches='tight', dpi=300)

## Categories Stats ##
print('\n')
print('### Digital Journal Top 5 Categories Counts ###')
print('\n')

# read in Categories HTML file #
cat_page = urllib.urlopen(cat_file).read()
# print(cat_page)

# Split by line #
cat_page_lines = re.split('\n',cat_page)

# Find All Categories #
cats = re.findall(r'<h4>(.*?)</h4>', cat_page, re.DOTALL)
cats = [ re.findall(r'<li>(.*?)</li>', cat, re.DOTALL) for cat in cats]
cats = [ cat for cat in cats if cat != []]
cats = [ re.findall(r'>(.*?)</a', cat[0], re.DOTALL)[0] for cat in cats ]
n_cats = len(cats)
# print(cats)

## Find All Categories Entries ##
dates = []
titles = []
hrefs = []
categories = []

for cat in cats :
    cat_entries = re.findall(r'<div id=\"{0}\">(.*?)</div>'.format(cat), cat_page, re.DOTALL)[0]

    # print(cat)
    # print(cat_entries)

    cat_hrefs = re.findall(r'href=\"(.*?)\">', cat_entries, re.DOTALL)
    cat_titles = re.findall(r'.html\">(.*?)</a>', cat_entries, re.DOTALL)
    cat_ymd = re.findall(r'/(\d{4})/(\d{2})/(\d{2})/', cat_entries, re.DOTALL)
    cat_ymd = [ '{0}-{1}-{2}'.format(ymd[0],ymd[1],ymd[2]) for ymd in cat_ymd]

    for (href,title,date) in zip(cat_hrefs,cat_titles,cat_ymd):
        # print(cat,href,title,date)
        # print(cat)
        dates.append(date)
        hrefs.append(href)
        titles.append(title)
        categories.append(cat)

# print(len(categories), len(titles), len(dates), len(hrefs))

# for (cat,href,title,date) in zip(categories, hrefs, titles, dates):
    # print(cat,href, title,date)

## Create a Dataframe ##
cat_df = pd.DataFrame({'Entry Category':categories,'Entry Title':titles, 'Category HyperRefs':hrefs}, index=pd.to_datetime(dates))
cat_df = cat_df.sort_index(ascending=True)
# print cat_df.head()
print(cat_df.groupby('Entry Title').size().head())
print(cat_df.groupby('Entry Category').size().nlargest(5))

## Find the top 5 categories ##
top_cats = cat_df.groupby('Entry Category').size().nlargest(5)
top_cats = list(top_cats.index)

## Create top 5 Heatmaps ##

# clear dir #
# os.system('rm ' + parent + 'assets/calendars/*.png')

colors = ['firebrick','steelblue','seagreen','coral','indigo']
# colors = ['#0B146E','#6D2434','#5EDA9E','#533965','#FFA803']
colors = [ to_rgba(color, 0.75) for color in colors ]
for (cats, color) in zip(top_cats, colors) :
    cal_df = pd.DataFrame(cat_df['Entry Category'][cat_df['Entry Category'] == cats ])
    cal_df['Entry Category'] = cal_df['Entry Category'].map({'{0}'.format(cats): 10})
    # print cal_df

    cal.calendar_heatmap(cal_df, title='{0} Journal Entries'.format(cats), cbar_title='', label='0211', cmap=ListedColormap([color]), cbar=False)
    plt.savefig(parent + 'assets/calendars/{0}calendar.png'.format(cats), bbox_inches='tight', dpi=300)

# Get Delta Shifts Information ##
print('\n')
print('### TA Shifts Counts ###')
print('\n')

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
years = range(2014,2021)
for year in years :
    run_page = urllib.urlopen('http://www.telescopearray.org/tawiki/index.php/{0}_Run_Signups'.format(year)).read()
    run_page_lines = re.split('\n',run_page)

    for line in run_page_lines:
        if 'Greg Furlich' in line:
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
md_df = pd.DataFrame(shifts_df['Dark Time'][shifts_df['MD Operators'].str.contains('Greg Furlich')], index= shifts_df.index[shifts_df['MD Operators'].str.contains('Greg Furlich')])
md_df['Dark Time'] = pd.to_numeric(md_df['Dark Time'])
print('MD FD Shifts: {0} Total'.format(len(md_df)))
print(md_df.groupby(md_df.index.year).count())

cal.calendar_heatmap(md_df, title='Middle Drum FD Shifts', cbar_title='Run Length', label='0211', cmap='Reds', cbar=False)
plt.savefig(parent + 'assets/calendars/MD_calendar.png'.format(cats), bbox_inches='tight', dpi=300)

# SD Shifts #
sd_df = pd.DataFrame(shifts_df['SD Monitor'][shifts_df['SD Monitor'].str.contains('Greg Furlich')], index= shifts_df.index[shifts_df['SD Monitor'].str.contains('Greg Furlich')])
sd_df['SD Monitor'] = 1
print('SD Monitor Shifts: {0} Total'.format(len(sd_df)))
print(sd_df.groupby(sd_df.index.year).count())

cal.calendar_heatmap(sd_df, title='SD Monitor Shifts', cbar_title='', label='0211', cmap=ListedColormap([to_rgba('Green', 0.75)]), cbar=False)
plt.savefig(parent + 'assets/calendars/SD_calendar.png'.format(cats), bbox_inches='tight', dpi=300)

# Field Shifts #
field_df = pd.DataFrame(shifts_df['Field Work'][shifts_df['Field Work'].str.contains('Greg Furlich')], index= shifts_df.index[shifts_df['Field Work'].str.contains('Greg Furlich')])
field_df['Field Work'] = 1
print('Field Shifts: {0} Total'.format(len(field_df)))
print(field_df.groupby(field_df.index.year).count())

cal.calendar_heatmap(field_df, title='Field Shifts', cbar_title='', label='0211', cmap=ListedColormap([to_rgba('Blue', 0.75)]), cbar=False)
plt.savefig(parent + 'assets/calendars/Field_calendar.png'.format(cats), bbox_inches='tight', dpi=300)

## Update stats.html  ##

stats_orig = '''---
layout: default
permalink: /stats/
title: Journal Stats
---

<h2>Digital Journal Contributions</h2>
<center><img src="/assets/git_contributions.png" width="800" align="middle"></center>'''
stats_orig = re.split('\n',stats_orig)
# print stats_orig

intro_lines ='\n<h2>Digital Journal Top 5 Categories</h2>\n'
intro_lines = re.split('\n',intro_lines)

add_lines = []
for cat in top_cats :
    # print(cat)
    line = '\n<center><img src="/assets/calendars/{0}calendar.png" width="800" align="middle"></center>\n'.format(cat)
    # add_lines.append(re.split('\n',line))
    add_lines.append(line)

# Shift Calendars #
add_lines.append('<h2>Telescope Array Shifts Contributions</h2>')
add_lines.append('\n<center><img src="/assets/calendars/MD_calendar.png" width="800" align="middle"></center>\n')
add_lines.append('\n<center><img src="/assets/calendars/SD_calendar.png" width="800" align="middle"></center>\n')
add_lines.append('\n<center><img src="/assets/calendars/Field_calendar.png" width="800" align="middle"></center>\n')

# add_lines = re.split('\n',add_lines)
all_lines = stats_orig + intro_lines[:] + add_lines
# print(intro_lines)
# print(list(add_lines))

# Write to file :
f = open(stats_file, "w+")
for line in range(len(all_lines)):
    # print(all_lines[line]+"\n")
    f.write(all_lines[line]+"\n")
