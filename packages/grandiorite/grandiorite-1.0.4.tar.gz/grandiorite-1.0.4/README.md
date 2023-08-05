### Setup

`pip install -r requirements.txt`

### Run

`python main.py`

### Building and Uploading

``` python
python3 setup.py sdist bdist_wheel
python3 -m twine upload -dist/*
[username: __token__, password: <API TOKEN FROM PYPI.ORG ACCOUNT SETTINGS>]
```

