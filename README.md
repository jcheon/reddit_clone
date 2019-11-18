
# Reddit Clone
![Django](https://static.djangoproject.com/img/logos/django-logo-negative.png) 
![Docker](https://www.docker.com/sites/default/files/d8/2019-07/vertical-logo-monochromatic.png | width=40) 
![Foundation](https://www.zvstcloudtech.com/adminpanel/uploadimage/42734.png | width=40)
![Vue](https://ih1.redbubble.net/image.393347411.1344/pp,550x550.jpg | width=40)
## Begin
* Clone repo 
```
git clone https://github.com/jcheon/reddit_clone
```
* Go into the repo
```
cd reddit_clone
```
* Run Docker
```
docker-compose up
```

## Help
* Get into container's shell
```
docker-compose run web /bin/bash
```

* Migrate database
```
python manage.py makemigrations
python manage.py migrate
```


## regular files

* **Dockerfile** - Initial dockerfile to help us setup our environment
* **docker-compose.yml** - Initial starter docker-compose file
* **requirements.txt** - Blank requirements.txt file for us to add python package requirements into

## hidden files

* **.gitignore** - ignores python code & macOS generated files that don't need to be in the repo
