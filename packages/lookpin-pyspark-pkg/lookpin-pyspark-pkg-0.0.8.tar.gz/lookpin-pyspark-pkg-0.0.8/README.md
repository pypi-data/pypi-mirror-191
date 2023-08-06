#install
python -m pip install --upgrade build

#install
python -m pip install --upgrade twine

#root
cd lookpin-pyspark-pkg

#build
python -m build 

#upload 
python -m twine upload dist/*

#user auth
register 1password
ID: level13
