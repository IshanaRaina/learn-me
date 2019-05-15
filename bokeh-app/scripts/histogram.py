import pandas as pd
import numpy as np
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Panel
from bokeh.models.widgets import CheckboxGroup, Select
from bokeh.palettes import Category10_5

def histogram_tab(flights):

    #####################Preparing the dataset####################
    def make_dataset(carrier_list):
        reporting_df = pd.DataFrame(columns=['count', 'left', 'right', 'f_count', 'f_interval', 'name', 'color'])

        #For each of the 5 carriers, perform the following processing steps
        for i, carrier_name in enumerate(carrier_list):
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
            #Lastly, append to main dataframe at the end of each iteration
            reporting_df=reporting_df.append(arr_df)

        reporting_df=reporting_df.sort_values(['name', 'left'])
        return ColumnDataSource(reporting_df)

    #####################Visualizing with Bokeh####################
    def make_plot(src):
        #Create the figure
        plot = figure(plot_width=800, plot_height=800, title='Histogram of Arrival Delays by Carrier', \
            x_axis_label = 'Arrival Delay (min)', y_axis_label='Count')
        #Add quad glyph with ColumnDataSource
        plot.quad(source=src, bottom=0, top='count', left='left', right='right', \
            fill_color='color', line_color='black', legend = 'name', hover_fill_color='color')
        #Initialize a hovertool and add it to the plot
        hover=HoverTool(tooltips=[('Carrier', '@name'), ('Flight Count', '@f_count'), ('Delay', '@f_interval')], mode='vline')
        plot.add_tools (hover)
        return plot
    
    #####################Dynamic updation of data####################
    def update(attr, old, new):
        updated_carriers = [carrier_selection.labels[i] for i in carrier_selection.active]
        new_src = make_dataset(updated_carriers) #function returns ColumnDataSource(updated df)
        src.data.update(new_src.data) #we don't need to call make_plot again, we just need to update the data

    #Checkbox Group initialization and manipulation
    available_carriers = list(set(flights['name']))
    available_carriers.sort()
    carrier_selection = CheckboxGroup(labels=available_carriers, active=[0,1])
    carrier_selection.on_change('active', update)

    #Initial data source to display
    initial_carriers = [carrier_selection.labels[i] for i in carrier_selection.active]
    src = make_dataset(initial_carriers)
    plot = make_plot(src)

    layout = row(carrier_selection, plot)
    tab = Panel(child=layout, title='Histogram')
    return tab