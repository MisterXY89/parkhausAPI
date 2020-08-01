# Wrapper for car parks live data in Constance

## Install
`pip install parkhausAPI`

### Dependencies:
```
bs4
numpy
requests
lxml
```
## Use
```python

from parkhausAPI import API
api = API()

# list all places
api.getPlaces()

# get information about a specific car park
api.getInfo("Altstadt") # code works as well
# returns a Parkhaus Object:

```

## Parkhaus Object
The following attributes are parsed:
```
entry         : where the entry to the car park is
openingHours  : opening hours of the car park
hightLimit    : empty if none
address       :
operator      :
spots         : total number of available spots
freeSpots     : free spots
occupiedSpots : occupied spots
tendency      : tendency - gleichbleibend, steigend or sinkend
image         : an image of (the entry of) the car park
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
