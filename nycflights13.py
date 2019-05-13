import pandas as pd
import numpy as np
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category10_5

flights=pd.read_csv(".\flights.csv", index_col=0)
print(flights.info(), "\n\n")

#####################Preparing the dataset####################
carrier_nums = flights.groupby('carrier')['year'].count().sort_values(ascending = False)
print(carrier_nums, "\n\n")

#Subset to 5 most common carriers
flights = flights[flights['carrier'].isin(carrier_nums.index[:5])]

#Subset to only [-2, +2] hour delays
flights = flights[(flights['arr_delay'] >= -120) & (flights['arr_delay'] <= 120)]

#Tailor new dataframe to reporting needs
by_carrier = pd.DataFrame(columns=['count', 'left', 'right', 'f_count', 'f_interval', 'name', 'color'])

#For each of the 5 carriers, perform the following processing steps
for i, carrier_name in enumerate(flights['name'].unique()):
    #work on data subsets pertaining to each carrier
    subset_df = flights[flights['name']==carrier_name]
    #Using np.histogram to determine data and edges
    arr_hist, edges = np.histogram(subset_df['arr_delay'], bins=int(240/5), range = [-120, +120])
    #Add data to dataframe
    arr_df = pd.DataFrame({'count':arr_hist, 'left':edges[:-1], 'right':edges[1:]})
    arr_df['f_count'] = ['%d flights' % count for count in arr_df['count']]
    arr_df['f_interval'] = ['%d to %d minutes' %(left, right) for left, right in zip(arr_df['left'], arr_df['right'])]
    arr_df['name']=carrier_name
    arr_df['color']=Category10_5[i]
    #Lastly, append to main dataframe
    by_carrier=by_carrier.append(arr_df)

by_carrier=by_carrier.sort_values(['name', 'left'])
print(by_carrier.head(), "\n\n")
print(by_carrier.tail(), "\n\n")

#####################Visualizing with Bokeh####################
src = ColumnDataSource(by_carrier)
#Create the figure
plot = figure(plot_width=800, plot_height=800, title='Histogram of Arrival Delays by Carrier', \
    x_axis_label = 'Arrival Delay (min)', y_axis_label='Count')
#Add quad glyph with ColumnDataSource
plot.quad(source=src, bottom=0, top='count', left='left', right='right', \
    fill_color='color', line_color='black', legend = 'name', hover_fill_color='color')
#Initialize a hovertool and add it to the plot
hover=HoverTool(tooltips=[('Carrier', '@name'), ('Flight Count', '@f_count'), ('Delay', '@f_interval')], mode='vline')
plot.add_tools (hover)
output_file('learning bokeh.html')
show(plot)