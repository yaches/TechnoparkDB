createdb -U postgres dbapi 
psql -U postgres -d dbapi -f schema.sql
# cd dbAPI/
# gunicorn -b :5000 dbAPI.wsgi