#!/usr/bin/env python

"""Tools for gathering and manipulating Reddit data.

The module has functions that use the praw package to gather data from Reddit.
It also has functions for manipulating data. Current functions only deal with
submitted post date and time data. You must enter your own client_id,
client_secret, and user_agent information below.

Example:
    This example takes a years worth of data from the /r/EngineeringStudents
    and puts it into an excel sheet.

    reddit_data.scrub_post_time_d2d('engineeringstudents',
                                    1452789417,1484413081, 'unix_time_data')
    reddit_data.unix_time_convert('unix_time_data','date_time_data')
    reddit_data.file_to_excel('date_time_data', 'post_frequency_data.xlsx')

Todo:
    *Defualt argment for subreddit is /r/all
    *File that will have client_id, client_secret, user_agent info. Write
        function where you can input that info and file is created.
    *General functions for data scrubbing that lets you put in an input
        argument that indicates what data you want.
    *Change all the functions for every data point on line to be seperated by
    a comma(',') instead of a space (' ').
    *Functions for excel manipulation, like a frequency calculation shortcut
        script.

"""

import praw
import openpyxl

__author__ = "Austin Pursley"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "austin.t.pursley@gmail.com"
__status__ = "Experiment"

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='')

def scrub_post_time (subreddit, post_num, file_name):
    """"Function to get sumbitted time data for a number of subreddit posts.

    Args:
        subreddit (str): name of subreddit.
        post_num (int): number of subreddit posts to gather time data from.
        file_name (str): name of file to save that time data to.

    Returns:
        None

    """""

    subreddit = reddit.subreddit(subreddit)
    with open(file_name, 'w') as f:
        for submission in subreddit.new(limit=post_num):
            f.write(str(submission.id))
            f.write(' ')
            f.write(str(submission.created_utc))
            f.write('\n')
    f.close()

def scrub_post_time_d2d(subreddit, start_unix_time, end_unix_time, file_name):
    """"Gets submitted post times for posts in subreddit between two times.

    Args:
        subreddit (str): Name of subreddit.
        start_unix_time (int): Function will start to get data from post
            submitted after this time. It must be in the unix time format.
        end_unix_time (int): Function will stop getting data from post
            submitted before this time. It must be in the unix time format.

    Returns:
        None
    """""

    subreddit = reddit.subreddit(subreddit)
    with open(file_name, 'w') as f:
        for submission in subreddit.submissions(start_unix_time, end_unix_time):
            f.write(str(submission.id))
            f.write(' ')
            f.write(str(submission.created_utc))
            f.write('\n')
    f.close()

def unix_time_convert(file_read, file_write):
    """"Converts unix time data into regular time-date data.

    This function reads a file with the reddit id and unix time on each line
    and writes a new file where the time is instead in a common date-time
    format.

    Args:
        file_read (str): name of the file with the reddit post id and unix time.
        file_write (str): name of the file written with converted date-time values.

    Returns:
        None
    """""

    from datetime import datetime
    with open(file_write, 'w') as f1:
        with open(file_read, 'r') as f2:
            for line in f2:
                line_split = line.split()
                f1.write(line_split[0])
                f1.write(' ')
                time_data_sec = float(line_split[1])
                date_time_data = datetime.fromtimestamp(time_data_sec)
                f1.write(str(date_time_data))
                f1.write('\n')
    f1.close()
    f2.close()

def file_to_excel(file_read, xl_file_name):
    """""Reads a text file with data and puts that into an excel sheet.

    Args:
        file_read (str): name of text file with data. Row data is on each line,
        separated by spaces to indicated different columns.
        xl_file_name (str): name of the excel file data is being written to.
    Returns:
        None
    """""

    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    with open(file_read, 'r') as f:
        row_num = 1
        for line in f:
            line_split = line.split()
            column_num = 1
            for item in line_split:
                ws.cell(column=column_num, row=row_num,
                        value=line_split[column_num - 1])
                column_num += 1
            row_num += 1
    wb.save(xl_file_name)
