# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.figure as figure

search_name = input('Please enter a search name: ')

NameDirectory = Path(".\data")

# get a working list of each file
NamesFileList = [x for x in NameDirectory.iterdir() if x.is_dir() == False]

def CheckName(NameFile,name='Jack'):
    '''
    Parameters
    ----------
    NameFile : path object
        path object of ssa data file.
    name : string, optional
        name string to search for. The default is 'Jack'.

    Returns
    -------
    year : int
        year that was searched.
    count_male : int
        count of occurences found for males.
    count_female : int
        count of occurences found for females.

    '''
    # calculate the year
    year = NameFile.stem[3:]
    # read the csv data
    temp_df = pd.read_csv(NameFile,names=['Name','Sex','Count'])
    
    #Check for the name in the datafile
    if name in temp_df.Name.values:
        sub_df = temp_df.loc[temp_df.Name == name]
        # check to see if name is both M & F
        if sub_df.shape[0] == 1:
            #just one
            if sub_df.iloc[0,1] == 'M': 
                # is male
                count_male = sub_df.iloc[0,2]
                count_female = 0
            else: #is female
                count_male = 0
                count_female = sub_df.iloc[0,2]
        else:
            # both sexes actually easier!
            count_male = sub_df.loc[sub_df.Sex == 'M'].iloc[0,2]
            count_female = sub_df.loc[sub_df.Sex == 'F'].iloc[0,2]
    else:
        # name not in year
        count_male = 0
        count_female = 0
    return (year,count_male,count_female) 

# create the dictionary
NameData = {'Year':[],
            'Count_male':[],
            'Count_female':[]}

#now run through files and check for names
for file in NamesFileList:
    (year, count_male, count_female) = CheckName(file,search_name)
    NameData['Year'].append(year)
    NameData['Count_male'].append(count_male)
    NameData['Count_female'].append(count_female)

df = pd.DataFrame(NameData)

# plotting
fig, (ax2, ax3) = plt.subplots(2,1)
ax2.bar(df.Year,df.Count_female,color='salmon')
ax3.bar(df.Year,df.Count_male)
# set the title
ax2.set_title(search_name + ' occurence by year')
# set the tick marks
ax2.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax2.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax2.tick_params(labelsize=8)
ax2.grid()
ax3.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax3.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax3.tick_params(labelsize=8)
ax3.grid()
# set legends
ax2.legend(['Female'])
ax3.legend(['Male'])
# set the size
fig.set_size_inches(7,5)
fig.set_dpi(125)
# save the figure
figpath = Path.cwd() / Path(search_name + '.png')
fig.savefig(figpath)

# print a summary
print('Search name: {}'.format(search_name))
print('Female stats:')
print('Total women with name:\t{}'.format(df.Count_female.sum()))
print('Count at peak:\t{}'.format(df.Count_female.max()))
print('Peak year:\t{}'.format(df.Year.iloc[df.Count_female.idxmax()]))
print('-----')
print('Male stats:')
print('Total women with name:\t{}'.format(df.Count_male.sum()))
print('Count at peak:\t{}'.format(df.Count_male.max()))
print('Peak year:\t{}'.format(df.Year.iloc[df.Count_male.idxmax()]))
