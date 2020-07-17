http://51.75.170.196:1337
http://51.75.170.196
ssh ubuntu@51.75.170.196


PROD :
docker-compose -f docker-compose.prod.yml down && docker-compose -f docker-compose.prod.yml build --no-cache && docker-compose -f docker-compose.prod.yml up

sudo docker-compose -f docker-compose.prod.yml down && sudo docker-compose down -v && sudo docker-compose -f docker-compose.prod.yml down && sudo docker-compose -f docker-compose.prod.yml build --no-cache && sudo docker-compose -f docker-compose.prod.yml up -d

DEV :
sudo docker-compose -f docker-compose.yml down && sudo docker-compose -f docker-compose.yml build --no-cache && sudo docker-compose -f docker-compose.yml up -d


DEV CACHE : 
sudo docker-compose -f docker-compose.yml down && sudo docker-compose -f docker-compose.yml build && sudo docker-compose -f docker-compose.yml up


CREATE SUPER USER :
sudo docker-compose run web python manage.py createsuperuser

BUILD PROD :
docker-compose down -v
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build --force-recreate --renew-anon-volumes
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

sudo docker volume prune
sudo docker system prune -a
sudo docker builder prune

docker-compose -f docker-compose.prod.yml build -d
GO INSIDE DOCKER COMPOSE CONTAINER :
sudo docker ps
sudo docker exec -ti 08f156938cc2 sh
(08f156938cc2 = ID du container)

git reset --hard

sudo docker-compose -f docker-compose.prod.ssl.yml exec web python manage.py migrate --noinput
sudo docker-compose -f docker-compose.prod.ssl.yml exec web python manage.py collectstatic --no-input --clear
sudo docker-compose -f docker-compose.prod.ssl.yml exec web python manage.py
 createsuperuser

-----------------------------------------------------------------
https://github.com/ermissa/django-docker-setup
***********
1ere fois : 

sudo docker-compose -f docker-compose.prod.ssl.yml down
sudo docker system prune -a
git pull origin master
chmod u+x init-letsencrypt.sh 
./init-letsencrypt.sh

(si besoin  : 
sudo docker-compose -f docker-compose.prod.ssl.yml exec web python manage.py migrate --noinput
sudo docker-compose -f docker-compose.prod.ssl.yml exec web python manage.py collectstatic --no-input --clear
sudo docker-compose -f docker-compose.prod.ssl.yml exec web python manage.py
 createsuperuser )

Normalement tout fonctionne sauf l'api, on va refaire le process ci-dessous pour
activer les apis. Aussi faire attention à la variable stagging dans init-letsencrypt
qui permet de faire un fake certificat pour pas se faire limiter en essais.
Passer cette variable à 0 pour un veritable certificat.

*****************
Les autres fois : 
sudo docker-compose -f docker-compose.prod.ssl.yml down
sudo docker system prune -a
git pull origin master
sudo docker-compose -f docker-compose.prod.ssl.yml up -d

normalement cette fois ci-l'api fonctionne. (bien veiller à faire les calls en
http sur l'api

*****************

Dans le cas où plus rien ne fonctionne il faut tester cette stratégie :
https://www.datanovia.com/en/fr/lessons/comment-heberger-plusieurs-sites-web-https-sur-un-seul-serveur/
(multiple domains docker compose nginx)


**************
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)

