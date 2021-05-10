#made by @eliot.p on Friday 27. November 2020

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import datetime
import csv
from matplotlib.ticker import FormatStrFormatter

rcParams['mathtext.fontset'] = 'cm'
rcParams['font.family'] = 'STIXGeneral'

ax1 = plt.subplot(1, 1, 1)

high_score = score = time = xValues =  dates = []

with open('Media/score.csv', 'r') as file:
    reader = csv.reader(file, delimiter = ';')
    for row in reader:
        if len(row) == 0:
            continue
        else:
            date = str(row[0])
            date = date.replace('-', '/')
            dates.append(date)

n = len(dates)-1

if len(dates)>5:
    score, time = np.loadtxt('Media/score.csv', skiprows=4, usecols=(1, 2), unpack=True, delimiter= ';')
    
else:
    score, time = np.loadtxt('Media/score.csv', skiprows=1, usecols=(1, 2), unpack=True, delimiter= ';')

high_score = max(score)
xValues = np.arange(len(score))
average = np.mean(score)
median = np.median(score)

#Plotting values
ax1.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
ax1.plot(xValues, score, color = 'darkslategrey', label = 'Scores')
ax1.axhline(y = average, linestyle = 'dashdot', label = 'Mean', color = 'teal')
ax1.axhline(y = high_score, linestyle = 'dashdot', label = 'High Score', color = 'indigo', alpha = 0.7)
ax1.axhline(y = median, linestyle = ':', label = 'Median', color = 'peru', alpha = 1)
plt.xticks(ha = 'right', color = 'k', alpha = 0.9)
plt.yticks(color = 'k', alpha = 0.9)


#Setting labels
plt.locator_params(nbins=6)
ax1.set_xlabel('Game Nr.', fontsize=12, fontweight = 'bold')
ax1.xaxis.set_label_coords(1.05, -0.06)
ax1.set_ylabel('Score in WPM', rotation = 0, fontsize = 12, fontweight = 'bold')
ax1.yaxis.set_label_coords(0, 1.035)
ax1.fill_between(xValues, score, average, color = 'teal', alpha = 0.3)

#Setting grid and legend
ax1.grid(True)
grid_x_ticks = np.arange(0, xValues[len(xValues)-1] + 2, 1)
grid_y_ticks = np.arange(round(min(score) - 10, -1), high_score + 10, 2)
ax1.set_xticks(grid_x_ticks , minor=True)
ax1.set_yticks(grid_y_ticks , minor=True)
ax1.grid(which='minor', alpha=0.2, linestyle='--')
ax1.legend(loc='upper right', ncol=1, prop={'size': 9})

#Showing and saving
plt.savefig('score.png', bbox_inches='tight')