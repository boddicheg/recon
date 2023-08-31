docker stop recon
docker rm --force recon
docker rmi recon recon-web
docker build -t recon --build-arg CACHEBUST=$(date) .
docker-compose up