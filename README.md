# Wrapper for car parks live data in Constance
All necessary info will be explained in this README. For further info about each class,
have a look in the documented source files.

## Install
 - `pip install parkhausAPI`
 - clone and run `pip install .` in the root folder

### Dependencies of the packgage
These will be installed when installing via pip
```
bs4
numpy
requests
lxml
```
## Use
```python
# import and initialize
from parkhausAPI import API
api = API()

# list all places / returns a dict
places = api.getPlaces()
print(places)
# return:
{
    "Altstadt": 107845,
    "Lago" : 107856,
    "Marktstätte" : 107867,
    "Fischmarkt" : 107878,
    "Döbele" : 107889,
    "Augustiner" : 107900,
    "Karstadt": 107900,
    "Benediktinerplatz" : 107911,
    "Seerhein-Center" : 107922,
    "Bodenseeforum" : 107933
}

# get information about a specific car park
api.getInfo("Altstadt")
# code works as well, it returns the same as "Altstadt"
api.getInfo(107845)

# both return a Parkhaus Object
# -> See following section
```

### getPlaces()
**What** <br>
Get all car park names and their corresponding codes/ids/int  <br>
**Return** <br>
dict, places

### getInfo(name: str)
**What** <br>
calls getInfo on wrapper:
starts the process of getting the soup, parsing it
and creating the parkhaus object <br>
**Parameters** <br>
name : str
    name of the car park <br>
| maybe:
name : int
    code of the car park <br>
| maybe:
spots : bool
    parse spots? <br>
| maybe:
content : bool
    parse content? <br>

**Return** <br>
Parkhaus object with all infos

## Parkhaus Object
The Parkhaus class has the following attributes:
```
entry : str
    how and/or where to enter the car park
entry : str
    how and/or where to enter the car park
openingHours : str
    opening hours of the car park
hightLimit : str
    empty if none / is a string in the format: x,yz m with x,y,z number
address : str
    street, housenr and postal code
operator : str
    address and name of the car house operator
spots : int
    total number of available spots
freeSpots : int
    free spots
occupiedSpots : int
    occupied spots
tendency : str
    tendency of free spots development: gleichbleibend, steigend or sinkend
image : str
    an absolute image url of (the entry of) the car park    
```
If no corresponding value can be found, the attribute will be empty.

## License
MIT License

Copyright (c) 2020 Tilman Kerl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
