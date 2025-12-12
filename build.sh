pip install -r requirements.txt
python manage.py collectstatic --noinput --clear

mkdir -p media
mkdir -p media/profile_photos
mkdir -p media/images
