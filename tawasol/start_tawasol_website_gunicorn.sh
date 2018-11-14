

gunicorn --workers=2 --bind=127.0.0.1:5009 --log-level=debug tawasol:app --access-logfile=logs/access.log --error-logfile=logs/error.log