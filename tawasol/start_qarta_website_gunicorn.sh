

gunicorn --workers=2 --bind=0.0.0.0:5009 --log-level=debug tawasol:app --access-logfile=logs/access.log --error-logfile=logs/error.log