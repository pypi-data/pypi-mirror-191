import vincent
import folium
import CoolProp.CoolProp as CP
import numpy as np
import pandas as pd
from math import pi
from glob import glob
import plotly.graph_objs as go
import json
import requests
from math import cos

class greenhouse:
  def request(token, lat, lon):
    api_base = 'https://www.renewables.ninja/api/'
    s = requests.session()
    s.headers = {'Authorization': 'Token ' + token}
    url = api_base + 'data/pv'

    irradiance = np.zeros((8760))
    tilt = 0
    azim = 180
    args = {
        'lat': lat,
        'lon': lon,
        'date_from': '2019-01-01',
        'date_to': '2019-12-31',
        'dataset': 'merra2',
        'capacity': 1.0,
        'system_loss': 0.1,
        'tracking': 0,
        'tilt': tilt,
        'azim': azim,
        'raw' : True,
        'format': 'json'
    }

    r = s.get(url, params=args)
    parsed_response = json.loads(r.text)
    data = pd.read_json(json.dumps(parsed_response['data']), orient='index')
    metadata = parsed_response['metadata']
    s = np.array(data)
    irradiance[:] = s[:,1] + s[:,2]
    temperature = s[:,3]
    return(temperature, irradiance)

  def energy_model(temperature, irradiance, T_i, h, L, d, G= 2, U = 4, teta = pi/6):
    # U = 4 #[W/m^2K]
    # T_i = 18 #[C]
    # h = 4 #[m]
    # G = 2 #[m]
    # teta = pi/6
    beta = 0.71 #[%]
    N = 2.1*(10**-4) #[s^-1]
    Cp= CP.PropsSI('C','T',323,'P',101325,"Water") #[J/kg.k]
    rho = CP.PropsSI("D","T",323,"P",101325,"water") #[kg/m3]
    heat_demand = np.zeros((8760,2))
    E_r = np.zeros(8760)
    irradiance_total = np.zeros(8760)

    for i in range(8760):
      irradiance_total[i] = (L*h*irradiance[i]+d*h*irradiance[i]+L*(d/cos(teta))*irradiance[i])*beta
      E_r[i] = (((2*L*h)+(2*d*h)+(L*d/cos(teta))) * U + 1800*(h+G/2)*L*d*N)*(T_i - temperature[i])
      heat_demand[i,0] = (E_r[i] - irradiance_total[i])/10**6 #[MW]
      heat_demand[i,1] = i

    return(heat_demand)
  
  def figure(heat_demand,temperature):
    bound = int(np.maximum(abs(np.min(heat_demand[:,0])), np.max(heat_demand[:,0])))
    fig = go.Figure(data=go.Heatmap(
                        z=[temperature]*((bound+1)*2+1),
                        y = np.arange(-(bound+1),bound+2,1)))
    fig.add_trace(go.Scatter(
        x=heat_demand[:,1],
        y=heat_demand[:,0],
        name = "Energy demand [MW]",
        marker=dict(size=4,color= heat_demand[:,0],
                    colorscale="Edge",cmid=0,cmin = 0.005, cmax= 0.005,
                    line=dict(width=0.05,color='DarkSlateGrey')),
        mode="markers"))

    fig.update_layout(title={'text': '°C',
        'y':0.91,'x':0.94,'xanchor': 'center','yanchor': 'top',})

    fig.update_xaxes(title_text="Hour")
    fig.update_yaxes(title_text="Energy Demand[MW]",tickmode='linear')
    fig.update_layout(font=dict(size=20))

    fig.update_layout(width=1200,height=800)
    fig.update_xaxes(range=[0,8760])
    
    return(fig)

  def CDF_map(heat_demand, lat, lon):
    count, bins_count = np.histogram(heat_demand[:,0], bins=30)
    pdf = count / sum(count) 
    cdf = np.cumsum(pdf)


    scatter_points = {"x": bins_count[1:],"y": cdf*100,}
    scatter_chart = vincent.Scatter(scatter_points, iter_idx="x", width=600, height=300)
    scatter_chart.axis_titles(x='Energy demand [MW]', y='Cumulative distribution [%]')
    scatter_chart.colors(brew='Spectral')


    scatter_json = scatter_chart.to_json()
    scatter_dict = json.loads(scatter_json)




    m = folium.Map([lat, lon], zoom_start= 15)
    folium.raster_layers.TileLayer(
    tiles="http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
    attr="google",
    name="google maps",
    max_zoom=15,
    subdomains=["mt0", "mt1", "mt2", "mt3"],
    overlay=True,
    control=True,).add_to(m)

    popup = folium.Popup()
    folium.Vega(scatter_chart, height=350, width=650).add_to(popup)
    folium.Marker([lat, lon], popup=popup,
                  tooltip = f'Your Greenhouse',
                  icon = folium.Icon(color='green', icon='leaf',
                                     prefix='fa')
    ).add_to(m)


    return(m)
  












  def energymodel(token, lat, lon, T_i, h, L, d, G= 2, U = 4, teta = pi/6):
    temperature, irradiance = greenhouse.request(token, lat, lon)
    heat_demand = greenhouse.energy_model(temperature, irradiance, T_i, h, L, d, G= 2, U = 4, teta = pi/6)
    return(heat_demand)
  
  def visualization(token, lat, lon, T_i, h, L, d, G= 2, U = 4, teta = pi/6):
    temperature, irradiance = greenhouse.request(token, lat, lon)
    heat_demand = greenhouse.energy_model(temperature, irradiance, T_i, h, L, d, G= 2, U = 4, teta = pi/6)
    fig = greenhouse.figure(heat_demand,temperature)
    return(fig)
  
  def CDFmap(token, lat, lon, T_i, h, L, d, G= 2, U = 4, teta = pi/6):
    temperature, irradiance = greenhouse.request(token, lat, lon)
    heat_demand = greenhouse.energy_model(temperature, irradiance, T_i, h, L, d, G= 2, U = 4, teta = pi/6)
    m = greenhouse.CDF_map(heat_demand, lat, lon)
    return(m)
