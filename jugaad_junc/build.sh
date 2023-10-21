echo "Building the project..."
python3.11.5 -m pip install -r requirements.txt

echo "Make migrations.."
python3.11.5 manage.py makemigrations --noinput
python3.11.5 manage.py migrate --noinput

echo "Collect static...."
python3.11.5 manage.py collectstatic --noinput --clear

