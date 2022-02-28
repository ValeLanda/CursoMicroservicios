#!/bin/bash

# Crear un registry local: docker run -d -p "192.168.0.155:5000:5000" --restart=always --name registry registry:2
# verificar que la IP sea del equipo local, NO USAR NUNCA localhost, 127.0.0.1, etc.
# poner un nombre de acuerdo al aplicativo

imagename="apibase"
version=$(date +%Y%m%d%H%M%S)
registry="192.168.0.155:5000"

docker build --pull --rm -f "Dockerfile" -t $imagename:$version "."
docker tag $imagename:$version $registry/$imagename:$version
docker push $registry/$imagename:$version
sed -e "s|REPLACE_IMAGE_WITH_TAG|$registry/$imagename:$version|g" ./deployment.yaml | kubectl apply -f -
