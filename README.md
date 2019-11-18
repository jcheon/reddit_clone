
# Reddit Clone

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

## Techs used
* [Django](https://www.djangoproject.com/)
* [Docker](https://www.docker.com)
* [Foundation](https://foundation.zurb.com/)
* [Vue](https://vuejs.org/)
