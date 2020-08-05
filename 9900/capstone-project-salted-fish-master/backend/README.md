## This is project backend base directory

### Tested Environment:

Ubuntu 18.04 x64

### Suggestions

Run the backend service in a linux screen session will be easy for management.

Run the backend service in a python virtual environment is recommended since there are fixed package version requirements which is not latest version.

When editing config files, ensure they are saved in valid YAML format with UTF-8 encoding, with no BOM.

## Installation Guide

### For our own testing and demo:

1. Install python3.6+, pip3, configure by your preference

2. Install virtualenv by `python3 -m pip install virtualenv`

3. Create a clean virtual environment by `virtualenv --no-site-packages env`

4. Start virtual environment by `source env/bin/activate`

5. (In virtual environment) Install pypi libraries by: pip3 install -r requirements.txt

6. (In virtual environment) Run app.py by `python3 app.py` to start backend service

### For first time using the project:

1. Install python3.6+, mysql/mariadb, pip3, configure by your preference

2. Install virtualenv by `python3 -m pip install virtualenv`

3. Create a clean virtual environment by `virtualenv --no-site-packages env`

4. Start virtual environment by `source env/bin/activate`

5. (In virtual environment) Install pypi libraries by: pip3 install -r requirements.txt

6. Edit db.config for a valid mysql database for the service

7. Edit server.config to setup your own admin account

8. (In virtual environment) Run pre_init.py by `python3 pre_init.py` to generate required tables

6. (In virtual environment) Run app.py by `python3 app.py` to start backend service
