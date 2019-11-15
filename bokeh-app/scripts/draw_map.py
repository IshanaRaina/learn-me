import pandas as pd
import numpy as np
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Panel
from bokeh.models.widgets import CheckboxGroup, Select
from bokeh.palettes import Category20_16

def map_tab(map_data, states):
    
    #####################Preparing the dataset####################
    def make_dataset(carrier_list):
        # Dictionary mapping carriers to colors
        color_dict = {carrier: color for carrier, color in zip(available_carriers, airline_colors)}
        
        # Lists of data for plotting --> dict --> ColumnDataSource
        flight_x = []
        flight_y = []
        colors = []
        carriers = []
        mean_delays = []
        origin_x_loc = []
        origin_y_loc = []
        dest_x_loc = []
        dest_y_loc = []
        origins = []
        dests = []
        mean_distances = []

        # For each of the carriers, perform the following processing steps
        for carrier in carrier_list:
            subset_df = map_data[map_data['carrier']['Unnamed: 3_level_1'] == carrier]
            # Iterate through each flight (origin to destination) of the carrier
            for _, row in subset_df.iterrows():
                colors.append(color_dict[carrier])
                carriers.append(carrier)
                origins.append(row['origin']['Unnamed: 1_level_1'])
                dests.append(row['dest']['Unnamed: 2_level_1'])
                
                # Origin x (longitude) and y (latitude) location
                origin_x_loc.append(row['start_long']['Unnamed: 20_level_1'])
                origin_y_loc.append(row['start_lati']['Unnamed: 21_level_1'])
                
                # Destination x (longitude) and y (latitude) location
                dest_x_loc.append(row['end_long']['Unnamed: 22_level_1'])
                dest_y_loc.append(row['end_lati']['Unnamed: 23_level_1'])
                
                # Flight x (longitude) locations
                flight_x.append([row['start_long']['Unnamed: 20_level_1'], row['end_long']['Unnamed: 22_level_1']])
                
                # Flight y (latitude) locations
                flight_y.append([row['start_lati']['Unnamed: 21_level_1'], row['end_lati']['Unnamed: 23_level_1']])
                
                # Stats about the particular route
                mean_delays.append(row['arr_delay']['mean'])
                mean_distances.append(row['distance']['mean'])

        new_src = ColumnDataSource(data = {'carrier': carriers, 'flight_x': flight_x, 'flight_y': flight_y, 'origin_x_loc': origin_x_loc, \
            'origin_y_loc': origin_y_loc, 'dest_x_loc': dest_x_loc, 'dest_y_loc': dest_y_loc, 'color': colors, \
            'mean_delay': mean_delays, 'origin': origins, 'dest': dests, 'mean_distance': mean_distances})
        return new_src

    #####################Visualizing with Bokeh####################    
    def make_plot(src, xs, ys):
        plot = figure(plot_width=1100, plot_height=700, title='Flights Departing NYC in 2013')
        plot.xaxis.visible = False
        plot.yaxis.visible = False
        plot.grid.visible = False

        # States are drawn as patches
        patches_glyph = plot.patches(xs, ys, fill_alpha=0.2, fill_color='lightgray', line_width=2, line_alpha=0.8)

        # Flights are drawn as lines
        lines_glyph = plot.multi_line('flight_x', 'flight_y', color='color', line_width=2, line_alpha=0.8,\
            hover_line_alpha=1.0, hover_line_color='color', legend='carrier', source=src)

        # Origins (all in NYC) are drawn as squares
        squares_glyph = plot.square('origin_x_loc', 'origin_y_loc', color='color', size=10, source=src)

        #Destinations are drawn as circles
        circles_glyph = plot.circle('dest_x_loc', 'dest_y_loc', color='color', size=10, source=src)

        # Add glyphs to plot using the renderers attribute
        plot.renderers.append(patches_glyph)
        plot.renderers.append(lines_glyph)
        plot.renderers.append(squares_glyph)
        plot.renderers.append(circles_glyph)

        hover_line = HoverTool(tooltips = [('Airline','@carrier'), ('Average Delay (min)','@mean_delay{0.0}')], line_policy='next', \
            renderers = [lines_glyph])

        hover_circle = HoverTool(tooltips = [('Origin', '@origin'), ('Destination', '@dest'), ('Average Distance (miles)', '@mean_distance')], \
            renderers = [circles_glyph])

        # Postiion the legend so it doesn't overlap the plot
        plot.legend.location = (10,50) #Bottom left?

        plot.add_tools(hover_line)
        plot.add_tools(hover_circle)
        return plot

    #####################Dynamic updation of data####################
    def update(attr, old, new):
        updated_carriers = [carrier_selection.labels[i] for i in carrier_selection.active]
        new_src = make_dataset(updated_carriers) # function returns ColumnDataSource(updated df)
        src.data.update(new_src.data) # we don't need to call make_plot again, we just need to update the data

    ####################Initialization####################
    available_carriers = list(set(map_data['carrier']['Unnamed: 3_level_1'])) # simply due to first 2 rows being a header
    available_carriers.sort()

    airline_colors = Category20_16
    airline_colors.sort()
    
    # Remove Alaska and Hawaii from states
    # This modules exposes geometry data for Unites States. It exposes a dictionary 'data' which is
    # indexed by the two letter state code (e.g., 'CA', 'TX') and has the following dictionary as the 
    # associated value:
    # data['CA']['name']
    # data['CA']['region']
    # data['CA']['lats']
    # data['CA']['lons']
    if 'HI' in states: del states['HI']
    if 'AK' in states: del states['AK']

    # Put longitudes and latitudes in lists
    xs = [states[state]['lons'] for state in states]
    ys = [states[state]['lats']  for state in states]
    
    carrier_selection = CheckboxGroup(labels=available_carriers, active=[0,1])
    carrier_selection.on_change('active', update)

    # Initial data source to display
    initial_carriers = [carrier_selection.labels[i] for i in carrier_selection.active]
    src = make_dataset(initial_carriers)
    plot = make_plot(src, xs, ys)

    layout = row(carrier_selection, plot)
    tab = Panel(child=layout, title='Flight Map')
    return tab
