# Setup of postgresql

### Local Installation

##### Requirements

* Postgres App

##### Installing postgres

Download postgres from `https://postgresapp.com/` and install it to your machine.
Click `start` in order to start the server which runs on port 5432.
You will access your user on the terminal.
Create the database using `create database jarvis`


### Setting up postgres configurations in .env

```
LOCAL_DB_URL=postgresql://postgres:123456@localhost:5432/jarvis
```

`postgresql` represents the type of database you are using which is postgresql
`postgres` represents your postgresql User name
`123456` represents your postgresql User password
`localhost:5432` represents your postgresql server port
`jarvis` represents your postgesql database name
