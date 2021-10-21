# IndySCC API

This is a simple API wrapping a SQLite DB for programming
competition answers.

Each team will be provided with a unique API token
to access the database.  API calls can be made
using any HTTPS client.

This documentation provides example calls using bash
shell scripts.

## API Endpoints

Set some useful variables:
```
url=http://localhost:8080
TOKEN='my secret token'
```

---

Test your API token (`/team` endpoint):
```
curl -X GET \
     -H "accept: application/json" \
     -H "Authorization: token $TOKEN" \
     $url/team; echo
```
Should return your team's name as a json-encoded string.

---

Submit an answer (POST to `/answers/{problem}` endpoint):
```
curl -X POST \
     -H "accept: application/json" \
     -H "Authorization: token $TOKEN" \
     -d "1 Exaflop" \
     $url/answers/HPCG; echo
```

Example response: `{}`

No errors means the answer was accepted.

Example response:
```
{ 'errors':
    [ "Response text is missing 'Date:' line.",
      "Response text was too long."
    ]
}
```

This list of errors means the answer was not accepted.
There are two things that need to be fixed.

---

Check submitted answers (GET from `/answers` endpoint):
```
curl -X GET \
     -H "accept: application/json" \
     -H "Authorization: token $TOKEN" \
     $url/answers; echo
```

Example response:
{"HPL": 0, "HPCG": 1, "Gromacs": 0, "JohnTheRipper": 0, "Mystery": 0}

---

Get a list of submitted answers for
a particular problem (GET from `/answers/{problem}` endpoint):
```
curl -X GET \
     -H "accept: application/json" \
     -H "Authorization: token $TOKEN" \
     $url/answers/Gromacs; echo
```

Example response:
```
[ { "team":"Sun Yat-Sen",
    "problem":"HPCG",
    "created_at":"2021-10-20T17:55:13.010243"
  }
]
```

### Further API Documentation

The API endpoints are documented in $url/docs,
where $url is the server's base URL.  Note that the
test functions don't work there because the web interface
neglects to send header values to the API.


## Install and Run the Server

Although teams do not need to install and run the server,
it can be helpful to test that everything is working properly.

Use the following steps to install and run locally:
```
pip install -r requirements.txt
INDY_CONFIG=example_config.json uvicorn --port 8080 server:app
```


