

gunicorn --workers=2 tawasol:app --bind=127.0.0.1:5009 --log-level=debug --access-logfile=logs/access.log --error-logfile=logs/error.log