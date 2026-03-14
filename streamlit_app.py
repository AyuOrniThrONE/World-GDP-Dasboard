import streamlit as st
import pandas as pd
import math
from pathlib import Path

st.set_page_config(
    page_title='GDP Dashboard',
    page_icon = ':earth_asia:'
) 

@st.cache_data
def get_gdp_data():
    '''Grab GDP Data from CSV File'''

    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2024

    gdp_df = raw_gdp_df.melt(
        ['REF_AREA'],
        [str(x) for x in range(MIN_YEAR,MAX_YEAR+1)],
        'Year',
        'GDP',
    )
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

    return gdp_df

gdp_df = get_gdp_data()


# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_asia: World GDP Dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2024 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
'''

# Add some spacing
''
''

min_value = gdp_df['Year'].min()
max_value = gdp_df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value = min_value,
    max_value=max_value,
    value = [min_value,max_value]
)

countries = gdp_df['REF_AREA'].unique()

if not len(countries):
    st.warning("Select atleast one country")
selected_countries = st.multiselect(
    'Which countries would you like to view?',countries,['DEU','FRA','IND','BRA','GBR','JPN']
)
''
''
''

filtered_gdp_df = gdp_df[
    (gdp_df['REF_AREA'].isin(selected_countries))
]