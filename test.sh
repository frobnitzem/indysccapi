# Run the server with:
# INDY_CONFIG=example_config.json uvicorn --port 8080 server:app &

url=http://localhost:8080

curl -X GET \
     -H 'accept: application/json' \
     -H 'Authorization: token TAMU' \
     $url/team; echo

curl -X GET \
     -H 'accept: application/json' \
     -H 'Authorization: token SYS' \
     $url/answers/Gromacs; echo

curl -X POST \
     -H 'accept: application/json' \
     -H 'Authorization: token SYS' \
     -d '1 Exaflop' \
     $url/answers/HPCG; echo

curl -X GET \
     -H 'accept: application/json' \
     -H 'Authorization: token SYS' \
     $url/answers; echo

curl -X GET \
     -H 'accept: application/json' \
     -H 'Authorization: token SYS' \
     $url/answers/HPCG; echo

curl -X GET \
     -H 'accept: application/json' \
     -H 'Authorization: token TAMU' \
     $url/answers; echo

curl -X GET -H 'accept: application/json' -H 'Authorization: token admin' $url/admin/answers/Texas%20A%26M/HPCG
