# demo_pkg
A reference for making python packages and uploading them on PyPI

## Follow the above directory structure and enter the commands:

### For Windows:
```batch
py -m pip install --upgrade build
py -m build
```

### For Unix/MacOS:
```shell
python3 -m pip install --upgrade build
python3 -m build
```

## How to upload package on PyPI?

### For Windows:
```batch
py -m pip install --upgrade twine
py -m twine upload --repository testpypi dist/*
```

### For Unix/MacOS:
```shell
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```