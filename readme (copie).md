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
sudo docker exec -ti 08f156938cc2 sh
(08f156938cc2 = ID du container)

git reset --hard

sudo docker-compose -f docker-compose.prod.ssl.yml exec web python manage.py migrate --noinput
sudo docker-compose -f docker-compose.prod.ssl.yml exec web python manage.py collectstatic --no-input --clear
sudo docker-compose -f docker-compose.prod.ssl.yml exec web python manage.py createsuperuser
