# Fastapi Integrate Lean Fintech API

## Overview

About
This project using fastapi for the backend, bootstrap and jinja template engine as a frontend. it aims to integrate fintech platform that retrieved banking information and transactions to build a robust fintech apps.

## Requirement

See requirements.txt for updates.

```sh
requests==2.27.1
fastapi==0.72.0
uvicorn==0.17.0
python-dotenv==0.19.2
aiofiles==0.8.0
python-multipart==0.0.5
jinja2==3.0.3
Markdown==3.3.6
```

## Installation & Usage

```bash
$ git clone git@github.com:shinokada/fastapi-web-starter.git
$ cd fastapi-web-starter
# install packages
$ pip install -r requirements.txt
# start the server
$ uvicorn app.main:app --reload --port 8080
```

## Features

- Menu
- Unsplash
- Accordion
- Markdown pages

## Test

All tests are under `tests` directory.

```bash
# Change the directory
$ cd fastapi-integrate-leanapi
# Run tests
$ pytest -v
```
