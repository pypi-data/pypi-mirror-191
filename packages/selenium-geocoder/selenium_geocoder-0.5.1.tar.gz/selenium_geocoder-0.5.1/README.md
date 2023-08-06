# selenium-geocoder
Modularizing selenium code for getting coordinates from address of a place.

# Exmaple:
```python
from selenium_geocoder import Globe, Browsers

# code for selecting browser to automate on:
globe = Globe(browser=Browsers.FIREFOX)
"""
Supported browsers:
- Mozilla Firefox
- Google Chrome
- Microsoft Edge
"""

# code to get coordinates of a single locaiton: (returns a tuple)
x,y = globe.get_coordinate(name='University of Mumbai')

# code to get coordinates of a batch of locations: (returns a list)
coordinates = globe.get_coordinates(name=['Grand Hyatt Mumbai','Tajlands Mumbai', 'Trident Mumbai'])
```