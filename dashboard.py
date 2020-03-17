import streamlit as st
import plotly
import plotly.express as px
import datetime,pytz
import plotly.graph_objects as go
import pandas as pd

@st.cache(persist=True, suppress_st_warning=True)
def load_pred(farm):
    df = pd.read_csv('./results/'+farm+'.csv')
    return df

@st.cache(persist=True, suppress_st_warning=True)
def load_farm():
    df = pd.read_csv('https://services.aremi.data61.io/aemo/v6/csv/wind')
    df.set_index('DUID',inplace=True)
    return df

def str_2_utc(time):
    '''
    Convert the ISO format to time format in UTC
    Input time should be string 
    Output is a string in the format of %Y-%m-%d %H:%M:%S
    '''
    utc_dt = datetime.datetime.fromisoformat(time[:19])
    return utc_dt.strftime('%Y-%m-%d %H:%M:%S')

def utc_2_local(time,tz):
    '''
    Convert UTC time to local time in timezone tz
    Input time should be string in the format of %Y-%m-%d %H:%M:%S
    Input tz should be string (e.g.,) 'Australia/Brisbane'
    Output is a string in the format of %Y-%m-%d %H:%M:%S
    '''
    tz = pytz.timezone (tz)
    time = datetime.datetime.strptime (time, "%Y-%m-%d %H:%M:%S")
    local_dt = pytz.utc.localize(time).astimezone(tz)
    return local_dt.strftime('%Y-%m-%d %H:%M:%S')

@st.cache(persist=True, suppress_st_warning=True, allow_output_mutation=True)
def display_map(farms):
    tz = 'Australia/Adelaide'
    lastest_time = farms.dropna().iloc[:,3][0]
    lastest_time=utc_2_local(str_2_utc(lastest_time),tz)
    
    farm_list = ['BLUFF1', 'CATHROCK', 'CLEMGPWF', 'HALLWF2', 
                 'HDWF2', 'LKBONNY2',  'MTMILLAR', 'NBHWF1', 
                 'SNOWNTH1', 'SNOWSTH1', 'STARHLWF', 'WATERLWF', 'WPWF']
    
    
    farms.fillna(0,inplace=True)
    
    px.set_mapbox_access_token(
    "pk.eyJ1IjoiaGVuZ3dhbmczMjIiLCJhIjoiY2s3djRsNGZ5MDQwcjNlcGp4ajB5bDNwMCJ9.8V_SlFxCm3r29sTE9kmS8g")
    fig = px.scatter_mapbox(farms.loc[farm_list,:], lat="Lat", lon="Lon", zoom=4.5, text= 'Station Name',
                            size='Current Output (MW)', color="Current Output (MW)",
                            color_continuous_scale=plotly.colors.sequential.haline,
                            center={'lat':-35.5,'lon':137},
                            title='An Overview of Wind Power in SA, Last Update: '+lastest_time,
                            )
    return fig

@st.cache(persist=True, suppress_st_warning=True)
def display_plot(df,farm,dt_delta):
    today_str = '2020-02-01 00:00:00' #placeholder
    # Select a range to draw
    today = datetime.datetime.strptime(today_str, "%Y-%m-%d %H:%M:%S")
    start_str = (today - datetime.timedelta(days=dt_delta)).strftime('%Y-%m-%d %H:%M:%S')
    select_dt = df[(df.time < today_str) & (df.time > start_str)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=select_dt.time, y=select_dt['power'], name="Actual",
                             line_color='dimgray'))
    
    fig.add_trace(go.Scatter(x=select_dt.time, y=select_dt['pred'], name="Prediction",
                             line_color='orange'))
    
    fig.update_layout(title_text='Wind Power Predition at '+farm,
                      xaxis_rangeslider_visible=True)
    
    return fig
                 

    

def main():
    st.header('Welcome to a demo of wind power prediction')
    
    # Display prediction results
    farm = 'HDWF2'
    dt_delta = 30
    df = load_pred(farm)
    
    range_choice = st.sidebar.selectbox('Select range', 
            ['Last week','Last month','Last six months','Last year'])
    farm_choice = st.sidebar.selectbox('Select farm', ['HDWF2'])
    if farm_choice == farm:
        if range_choice == 'Last week':
            dt_delta = 7
        elif range_choice == 'Last month':
            dt_delta = 30
        elif range_choice == 'Last six months':
            dt_delta = 180
        elif range_choice == 'Last year':
            dt_delta = 365
        
        st.plotly_chart(display_plot(df,farm,dt_delta))
    
    # Display map view of all farms
    farms = load_farm()
    st.plotly_chart(display_map(farms))
    
    
if __name__ == '__main__':
    main()