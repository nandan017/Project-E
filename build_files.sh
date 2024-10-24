echo "Building files"
python3.12 -m pip install -r requirements.txt
python3.12 manage.py collectstatic --noinput --clear 
echo "Files built"