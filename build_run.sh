docker build -t datamining .
docker run -it --rm --publish 80:80 --name datamining datamining