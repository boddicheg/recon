docker rm --force recon
docker build -t recon .
docker exec -it recon //bin//sh 