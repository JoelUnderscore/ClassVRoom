python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > testdb.json
python manage.py loaddata testdb.json
