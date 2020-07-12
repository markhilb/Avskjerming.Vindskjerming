## Prerequisites
* Python 3.8
* Pillow
```
$ pip install Pillow
```

* Pylatex
```
$ pip install pylatex
```

* Latex compiler
https://miktex.org/download


## Run program
```
$ py main.py
```

## Create windows installer:
* Install cx_Freeze:
```
$ pip intall cx_Freeze
```
Create installer:
```
$ python setup.py bdist_msi
```
* Installer is located in src/dist/


## Convert to exe:
#### Windows
* Install pyinstaller: 
```
$ pip install pyinstaller
```
* Convert to exe:
```
$ pyinstaller --onefile -w main.py
```
* Delete build folder, and spec file (optional, but you don't need them)
* Enjoy :)
