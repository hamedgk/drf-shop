#### initial setup:
below command automatically creates db based on .env file, installs requirements and run containers.
exposing .env file is a bad practice. but I have nothing to lose here.
```bash
docker-compose up
```

#### navigate to python server container:
```bash
docker-compose exec web sh
```
after you got into container shell execute these:
#### create db schema:
```bash
python manage.py migrate
```

#### create superuser:
```bash
python manage.py createsuperuser --username admin --email hamed.gk@yahoo.com
```
only superusers role can edit, create, delete products 

#### if you needed to access to database:
```bash
docker-compose exec -it db psql -U hamedgk -d shop -w hahafafa
```
#### testing:
the postman collection is available in project directory
