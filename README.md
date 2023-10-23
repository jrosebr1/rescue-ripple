# rescue_ripple

## Launch commands
Start Redis:

```
$ redis-server
```

Create Django superuser (if not done already):

```
$ python manage.py createsuperuser
```

Launch Celery workers:

```
$ celery -A rescue_ripple worker -l INFO
```

Launch Flower:

```
$ celery -A rescue_ripple flower
```

---

## Adding social media posts to database

Ingest HumAID tweets:

```
$ python manage.py load_social_media_posts --tsv ~/Desktop/HumAID/events_set1/canada_wildfires_2016/canada_wildfires_2016_train.tsv
```

## Classifying social media posts

Classify HumAID data using prompt-based methods:

```
$ python manage.py classify_with_prompt --tsv ~/Desktop/HumAID/events_set1/canada_wildfires_2016/canada_wildfires_2016_train.tsv --experiment prompt-classification-gpt-3.5-turbo --model gpt-3.5-turbo
```