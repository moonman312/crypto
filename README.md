# Crypto
A simple pipeline for pulling in historical data about several cryptocurrencies and identifying any interesting patterns or features

## To Use  
### Setup Environment  
`pip install virtualenv`  
`virtualenv --python=<path/to/python3> <path/to/new/virtualenv/>`  
`source <path/to/new/virtualenv>/bin/activate`  
`pip install -r requirements.txt`  
  
  
## PostgreSQL and PostGIS installation in Mac OS 
Install Postgres with Homebrew  
`brew install postgres`  
Install PostGIS with Homebrew  
`brew install postgis`  
Start PostgreSQL server  
`pg_ctl -D /usr/local/var/postgres start`  
Create Database
`initdb /usr/local/var/postgres`
Create a new database
`createdb crypto`
Enable PostGIS
`psql crypto`

### Run program  
`python crypto.py`  
You will be prompted to enter a symbol until you provide a valid one. You can run this command multiple times and select different cryptocurrencies. 
