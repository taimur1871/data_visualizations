# python3
import pandas as pd

js = {
  "points": [
    {
      "curveNumber": 0,
      "pointNumber": 1449,
      "pointIndex": 1449,
      "lon": -97.891926,
      "lat": 35.405452,
      "customdata": [
        "EVEREST 1107 3SMH-24"
      ]
    },
    {
      "curveNumber": 0,
      "pointNumber": 1450,
      "pointIndex": 1450,
      "lon": -97.891926,
      "lat": 35.405452,
      "customdata": [
        "EVEREST 1107 3SMH-24"
      ]
    },
    {
      "curveNumber": 0,
      "pointNumber": 1451,
      "pointIndex": 1451,
      "lon": -97.891926,
      "lat": 35.405452,
      "customdata": [
        "EVEREST 1107 3SMH-24"
      ]
    },
    {
      "curveNumber": 0,
      "pointNumber": 1470,
      "pointIndex": 1470,
      "lon": -97.888439,
      "lat": 35.40544,
      "customdata": [
        "EVEREST 1107 6LMH-24"
      ]
    }
  ],
  "range": {
    "mapbox": [
      [
        -97.90895665917525,
        35.41342673518663
      ],
      [
        -97.8718778017534,
        35.39495746908659
      ]
    ]
  }
}

#for i in js['points']:
#    print(i['lon'])

df = pd.DataFrame(js['points'])
