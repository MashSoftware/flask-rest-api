# Flask REST API Template

This template repository contains a [Flask](https://flask.palletsprojects.com) app based RESTful API. The app is structured based on best practices and experience gained through previous implementations. By using a template repository you can [generate a new repository](https://github.com/MashSoftware/flask-rest-api/generate) with the same directory structure and files to get a new project started quicker.

## Prerequisites

### Required

- Python 3.6.x or higher
- PostgreSQL 10.x or higher

### Optional

- ???

## Getting started

### Create venv and install requirements

```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt ; pip3 install -r requirements_dev.txt
```

### Run app

```shell
flask run
```

## Testing

Run the test suite

```shell
python -m pytest --cov=app --cov-report=term-missing --cov-branch
```
