import os, datetime
import streamlit as st
from pyparsing import empty
import requests, json, folium
from dotenv import load_dotenv
from streamlit_folium import folium_static

load_dotenv()
st.set_page_config(layout="wide")
apikey = os.getenv("OPENWEATHERMAP_API_KEY")

LEFT_GAP = 0.2
RIGHT_GAP = 0.2

left, con1, right = st.columns([0.1, 1.0, 0.1])
left, select, right = st.columns([0.1, 1.0, 0.1])
left, graph1, right = st.columns([0.1, 1.0, 0.1])
# left, s1, s2 = st.columns([0.1, 0.45, 0.52])

def main() :
    # 사이드바
    st.sidebar.header("REPORTS")

    st.sidebar.markdown("OpenWeather API")
    st.sidebar.markdown("Checking Information")
    st.sidebar.markdown("Report")

    with left : 
        empty()

    with con1 :
        title()
        st.divider()

    with select :
        st.header('Select City')
        selected_city_options = ['Seoul', 'Busan', 'Paris', 'Berlin', 'Firenze', 'Napoli', 'Tokyo', 'Manila', 'Budapest', 'Zurich', 'Beijing', 'Moscow', 'Boston', 'Barcelona', 'Shanghai', 'Sydney', 'Amsterdam', 'Prague']
        selected_city_index = st.selectbox('', selected_city_options)

        col1, col2 = st.columns(2)
        with col1 : 
            city = selected_city_index
            data = get_weather_data(city)
            datas = get_weather_data_day(city)
            Select_city(selected_city_index, city, data)

        with col2 :
            show_map(data)
    
        with graph1 :
            graph()

def title():
    st.title("OpenWeather Information")

def Select_city(selected_city_index, city, data):
    st.subheader('Info')

    st.write('\n')
    st.write(f'Country : {data['sys']['country']}')
    st.write(f'City : {city}')
    st.write(f"Temperature : {data['main']['temp']} ℃")
    st.write(f'Lowest Temperature : {data["main"]["temp_min"]} ℃')
    st.write(f'Highest Temperature : {data["main"]["temp_max"]} ℃')
    st.write(f'Weather : {data["weather"][0]["main"]}')
    st.write(f'Description : {data["weather"][0]["description"]}')
    st.write(f'pressure : {data["main"]["pressure"]} ph')
    st.write(f'humidity : {data["main"]["humidity"]} %')
    st.write(f'Wind Speed : {data["wind"]['speed']}m/s')
    print(data)

def get_weather_data(city) :
    api = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&units=metric'
    result = requests.get(api)
    return json.loads(result.text)

def get_weather_data_day(city) :
    apis = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units=metric'
    forecast_result = requests.get(apis)
    return json.loads(forecast_result.text)

def show_map(data):
    if 'main' in data and 'weather' in data:
        location = data['name']
        temperature = data['main']['temp']
        weather_status = data['weather'][0]['main']

        # Folium을 사용하여 지도에 위치 표시하기
        m = folium.Map(location=[data['coord']['lat'], data['coord']['lon']], zoom_start=10)
        folium.Marker(location=[data['coord']['lat'], data['coord']['lon']], popup=f'{location}: {temperature}℃, {weather_status}').add_to(m)
        folium_static(m)
    else:
        st.write('City not found')

def graph(datas):
    data_to_write = {}
    for forecast in datas['list']:
        data_string = forecast['dt_txt']
        date_object = datetime.datetime.strptime(data_string, '%Y-%m-%d %H:%M:%S')
        day = date_object.strftime('%d')  # day만 출력 

        if day not in data_to_write:
            data_to_write[day] = {'max_temp': -100, 'min_temp': 100}

        min_temp = forecast['main']['temp_min']
        max_temp = forecast['main']['temp_max']

        if min_temp < data_to_write[day]['min_temp']:
            data_to_write[day]['min_temp'] = min_temp
            
        if max_temp > data_to_write[day]['max_temp']:
            data_to_write[day]['max_temp'] = max_temp

    st.write('Temperature forecast for the next 5 days:')
    st.write('Day | Min Temp (°C) | Max Temp (°C)')
    for day, temps in data_to_write.items():
        st.write(f'{day} | {temps["min_temp"]} | {temps["max_temp"]}')

    # data_to_write = []
    # date_check ={} # 값을 추가해줄 딕셔너리
    # max_temp = {}
    # min_temp = {}

    # if "list" in datas :
    #     for forecast in datas['list'] :
    #         data_string = forecast['dt_txt']
    #         date_object = datetime.datetime.strptime(data_string, '%Y-%m-%d %H:%M:%S')
    #         day = date_object.strftime('%d')  # day만 출력 
    #         # print(f'Date: {date_object.date()}, Day: {day}')

    #         # if date_object == day :
    #         #     date_check[day] = forecast['dt_txt'].index
            
    #         #해당 날짜를 구분하여 index의 길이를 측정하여 갯수파악
    #         if day not in date_check:
    #             date_check[day] = [datas['list'].index(forecast)]
    #         else:
    #             date_check[day].append(datas['list'].index(forecast))

    #     for day, index in date_check.items(): # 딕셔너리 day, index의 값을 출력
    #         print(f"Date: {day}, Index: {index}")

    #     date_check1 = list(date_check.items())
    #     length = len(date_check1)
    #     print(date_check1)

    #     for i in range(length):
    #         key, value = date_check1[i]
    #         # print(f"{key}, {value}")

    #     for key in date_check.keys():
    #         values = date_check[key]
    #         for idx, value in enumerate(values, start=1):
    #             print(f"{int(key)}day: {value}")
    #             check_list = datas['list'][value]
    #             check_list1 = check_list['main']['temp_min'] #최저온도
    #             check_list2 = check_list['main']['temp_max'] #최대온도
    #             # print(check_list)
    #             # print('최저 온도 :',check_list1,'°C')
    #             # print('최대 온도 :',check_list2,'°C')
                
    #              # 최고온도와 최저온도를 딕셔너리에 저장
    #             if key not in max_temp:
    #                 max_temp[key] = check_list2
    #             elif check_list2 > max_temp[key]:
    #                 max_temp[key] = check_list2

    #             if key not in min_temp:
    #                 min_temp[key] = check_list1
    #             elif check_list1 < min_temp[key]:
    #                 min_temp[key] = check_list1
                
    #             print(max_temp)
    #             print(min_temp)
    
main()