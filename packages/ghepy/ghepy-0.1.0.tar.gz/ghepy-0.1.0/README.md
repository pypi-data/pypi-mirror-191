<div align="center"> <img src="https://github.com/mehran-hmdpr/GHEpy/blob/main/GHEpy.png" width="300" height="300" >

<div align="left">

# GHEpy
**GHEpy** (Greenhouse energy-python) is a python tool for evaluation of heating demand in greenhouses when data are not provided elsewhere. 

## Table of contents
* [Description](#description)
     * [Problem definition](#problem-definition)
     * [Problem solution](#problem-solution)

* [Dependencies and installation](#dependencies-and-installation)

* [Examples and Tutorials](#examples-and-tutorials)

* [Authors and contributors](#authors-and-contributors)

* [License](#license)

## Description
**GHEpy** is a Python-based model implemented for greenhouses according to the energy balance equations. This calculation is intended as a guide for estimation purposes.



#### Problem definition
To estimate the heating demand of a greenhouse **GHEpy** needs parameters like location, dimantions, and inside minimum temperature. The required dimentions for the model are shown below:


          
#### Problem solution
  
The energy balance of a greenhouse can be calculated by:

$Q̇_g (t)= Q̇_{con}(t)+ Q̇_l(t)+ Q̇_{trans}(t)+Q̇_{vent}(t)-Q̇_s(t)$

Where:
  - $Q ̇_g (t)$ is the required heating energy to maintain greenhouse conditions.
  - $Q̇_{con}(t)$ is energy transfer by conduction and convection mechanisms.
  - $Q̇_l(t)$ is the energy exchange due to long-wave and short-wave radiations.
  - $Q̇_{trans}(t)$ is the energy flow rate caused by crop transpiration.
  - $Q̇_{vent}(t)$ is the heat flow rate due to mass transfer for ventilation
  - $Q̇_s(t)$ is the solar irradiation energy transfer. 


  
## Dependencies and installation
**GHEpy** requires `numpy`, `plotly`, `CoolProp`, `folium`, `vincent`. The code is tested for Python 3, while compatibility of Python 2 is not guaranteed anymore. It can be installed using `pip` or directly from the source code.

### Installing via PIP
To install the package just type:
```bash
> pip install GHEpy
```
To uninstall the package:
```bash
> pip uninstall GHEpy
```
## Examples and Tutorials

**GHEpy** has three main functions that can help you with calculating heating demand of a greenhouse to use any of them you need to have climate data. To acquire data, you just need to take a token from [renewable ninja platform](https://www.renewables.ninja/documentation/api).
- First function is `energymodel` which gives you energy demand of the greenhouse in 8760 hours of a year. To use this function just type:
  ```bash
    >
    from ghepy import model
    token = "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" # Token code that you should get from renewable ninja database
    lat = 52.225121 # latitude
    lon = 36.681990 # longitude
    T_i = 18 # minimum inside temperature
    h = 3 # dimension
    L = 100 # dimension
    d = 100 # dimension

    heating_demand = model.greenhouse.energymodel(token, lat, lon, T_i, h, L, d, G= 2, U = 4)

    ```
- The second funciton is `visualization` which gives you a figure of temperatures and energy demands during a year. An example of the result of this function can be seen here:
  ```bash
    >
      from ghepy import model
      token = "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" # Token code that you should get from renewable ninja database
      lat = 52.225121 # latitude
      lon = 36.681990 # longitude
      T_i = 18 # minimum inside temperature
      h = 3 # dimension
      L = 100 # dimension
      d = 100 # dimension

      fig = model.greenhouse.visualization(token, lat, lon, T_i, h, L, d, G= 2, U = 4)
      fig.show()

    ```
  The result would be something like this:
  
  
  <div align="center"> <img src="https://github.com/mehran-hmdpr/GHEpy/blob/main/Visualization%20(2).png" width="600" height="400" >
  <div align="left">
  
 - The last function is `CDFmap` which shows the location of greenhouse and cumulative distribution of greenhouse heating demand. This can help you realize how long your greenhouse needs heating or cooing during a year.
   ```bash
    >
      from ghepy import model
      token = "aa643a1899ea2156807425008360759c4853484d" # Token code that you should get from renewable ninja database
      lat = 52.225121 # latitude
      lon = 36.681990 # longitude
      T_i = 18 # minimum inside temperature
      h = 3 # dimension
      L = 100 # dimension
      d = 100 # dimension

      map = model.greenhouse.CDFmap(token, lat, lon, T_i, h, L, d, G= 2, U = 4)
      map

    ```
    The result would be something like this:
    <div align="center"> <img src="https://github.com/mehran-hmdpr/GHEpy/blob/main/CDF.png" width="900" height="506" >
    <div align="left">
    


## Authors and contributors
**GHEpy** is developed and mantained by
* [Mehran Ahmadpour](mailto:mehran.hmdpr@gmail.com)

under the supervision of Prof. Ramin Roshandel.

Contact us by email for further information or questions about **GHEpy**, or suggest pull requests. Contributions improving either the code or the documentation are welcome!
You can find out more about my projects by visiting my [website](https://mehranahmadpour.mozellosite.com/).
## License

See the [LICENSE](https://github.com/mehran-hmdpr/orcpy/blob/main/LICENSE) file for license rights and limitations (MIT).

   
