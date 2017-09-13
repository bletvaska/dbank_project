# dbank

Bank web application for Django - course project.

## Instalation

### If you are running Linux

then create virtual environment and install all the required packages with following commands:

```bash
cd dbank_project
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```


### If your are running Windows

then you are on your own ;) Or you can install [Chocolately](https://chocolatey.org/) (package manager for _Windows_)
and run following commands:

```shell
choco install cmder python3
```


### Running Tests

_py.test_ is used for testing instead of _unittest_. To run tests:

```shell
./manage.py
```

### Running Coverage