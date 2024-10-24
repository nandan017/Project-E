echo "Building files"
pip install -r requirements.txt
python manage.py collectstatic --noinput --clear 
echo "Files built"