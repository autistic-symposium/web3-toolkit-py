# Location API 🗺


Location API built with FastAPI. [Deployed in Vercel](https://choices-location-api.vercel.app/).

## Endpoint /location

Input data:

```
{"city": "berlin"}
```

Response:

```
{"lat":52.5186925,"lon":13.3996024,"tzone":1}
```


### Installing

```
virtualenv -p python3.9 venv
source venv/bin/activate
pipenv install
```

### Running


```
python3 main.py
```
