import requests
from bs4 import BeautifulSoup
import tkinter as tk
import json
from PIL import Image, ImageTk

api_key = '908e28f05e40363efea5141211dc18e2'
#Function to scrape the current temperature from Google search results
def get_current_temp(city):
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial'

    response = requests.get(api_url)
    data = response.json()
    temperature = data["main"]["temp"]

    weather = data['weather'][0]['main']
    icon = data['weather'][0]['icon']
    return temperature, weather, icon

    try:

        label.config(text=f'The current temperature in {city} is {temperature}° Farenheit, or {int((temperature-32)/1.8)}° Celcius. \nWeather: {weather}.')
    except:
        label.config(text =f'')
        label.config(text=f'You have entered an incorrect city.')
    #response.raise_for_status()

    #temperature = response.json().get('main', {}).get('temp')
    
    # soup = BeautifulSoup(response, 'lxml')
    # print(soup)
    # temperature = soup.find_all("div", attrs= {'id': "wob_tm"})
    #temperature_el = soup.find('span#wob_tm')

    # if temperature_el:
    #     temperature = temperature_el.texts
    # else:
    #     temperature = 'Data not found'

def get_weather():
    window.geometry('800x220')
    city = entry.get()
    try:
        temperature, weather, icon = get_current_temp(city)
    except:
        label.config(text=f'You have entered an incorrect city.')
        icon_label.image = None
        window.geometry('800x160')
    label.config(text=f'The current temperature in {city} is {temperature}° Farenheit, or {int((temperature-32)/1.8)}° Celcius. \nWeather: {weather}.')
    update_weather_icon(icon)
    label.update_idletasks()
    window.update_idletasks()
    width = label.winfo_width()+100
    window.geometry(f"{width}x{window.winfo_height()}")
    

def update_weather_icon(icon_code):
    icon_url = f'http://openweathermap.org/img/wn/{icon_code}.png'
    response = requests.get(icon_url, stream= True)
    image = Image.open(response.raw)
    image = image.resize((50,50))
    weather_icon = ImageTk.PhotoImage(image)
    icon_label.config(image = weather_icon)
    icon_label.image = weather_icon

def temp_text(event):
    entry.delete(0, tk.END)

window = tk.Tk()
window.title("Weather Data")
window.geometry('300x100')
window.minsize(300,120)
window.configure(bg = "white")

entry = tk.Entry(window, font = ("Poppins", 10), width=25)
entry.insert(0, "Type a city or location here...")
entry.bind("<Button-1>", temp_text)
entry.pack(pady=10)

button = tk.Button(window, text = 'Get Weather', command = get_weather, height= 1, width = 15, font = ("Poppins", 10), bg = 'light blue')
button.pack(pady = 10)

weather_frame = tk.Frame(window, bg = 'white')
weather_frame.pack(pady=10)

label = tk.Label(weather_frame, font = ("Poppins", 13), bg = "white")
label.pack()

icon_label = tk.Label(weather_frame, bg= "white")
icon_label.pack(side=tk.TOP, padx=10)

window.resizable(True, True)

window.mainloop()