# CERS
*CERS* (**C**urrency **E**xchange **R**ates **S**craper) is a collection of scripts to scrape currency exchange rates and store them in a *MongoDB* database.
*Note: unless otherwise noted, all below commands are assumed to be executed from the directory this readme file is in.*

## Configuration
The following environment variables are expected to be set:
- `CHROMEDRIVER_URL`: The address of a running Selenium Chrome Driver.
- `MONGO_DB_URL`: The URL to access the MongoDB server that should store the scraped information.

Note, that this gets taken care of automatically if you use the `docker-compose.yml` file in this repository. See section *Run the scripts using Docker Compose* below for details.

## Preparation
Generate relevant indices in your MongoDB, if you haven't done so already. You can use
```sh
python -m scripts.create_mongo_indices
```

## Available scripts
All available scripts are living in the `./scripts` folder. Usage instructions can be viewed using the `--help` flag. Use, for example,
```sh
python -m scripts.scrape_imf --help
```
to find out what the script `scrape_imf` does and what options it supports.

## Tests
Automated tests are available in the `./tests` directory. You can run a test file like any script. For example
```sh
python -m tests.scripts.test_scrape_imf
```

## Run the scripts using Docker Compose
Simply prepend `docker-compose run --rm app` to the desired command and Docker will take care of all dependencies. The MongoDB data will be stored in a new directory `./data`.
For example, to run the script `scrape_imf`, simply do
```sh
docker-compose run --rm app python -m scripts.scrape_imf
```
