docker rm --force recon
docker build -t recon .
docker run --name recon --rm -p 1337:1337 -d -v assets:/usr/src/recon/assets recon
docker exec -it recon //bin//sh 