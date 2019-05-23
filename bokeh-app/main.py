import pandas as pd
from os.path import dirname, join
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.sampledata.us_states import data as states

from scripts.histogram import histogram_tab
from scripts.draw_map import map_tab

flights=pd.read_csv(join(dirname(__file__), 'data', 'flights.csv'), index_col=0).dropna()

map_data = pd.read_csv(join(dirname(__file__), 'data', 'flights_map.csv'), header=[0,1], index_col=0)

tab1=histogram_tab(flights)
tab2=map_tab(map_data, states)

tabs = Tabs(tabs=[tab1, tab2]) #add tab2
curdoc().add_root(tabs)