# FiiPractic Flask API 2021

This project is an user management API developed within the FiiPractic workshop
Python Backend by Bytex in 2021. The API is built with the help of Python (Flask
framerwork), SQLAlchemy ORM and sqlite3 database (relational database).


## API Reference

Postman documentation: [Link](https://documenter.getpostman.com/view/11692173/VUxKS99Y)

## Features

- CRUD routes for users and companies
- Relational database
- Email verification
- Logging feature, every important action is saved
- RESTful API
- Docker image ready to be build
## Local deployment 

To run this project locally configure environment variables, then run:

```bash
  docker build -t fiipractic-python .
  docker compose up
```

