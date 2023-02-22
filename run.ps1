docker build -t pentester .
docker run --name pentester --rm -p 8079:8079 -d pentester
docker exec -it pentester //bin//sh