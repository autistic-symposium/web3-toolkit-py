# Location API 🗺


Location API deployed in Vercel and built with FastAPI.

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
