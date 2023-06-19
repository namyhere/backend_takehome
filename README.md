# Backend Engineering Take-Home Challenge
### Introduction
In this challenge, you will be tasked with creating a simple ETL pipeline that can be triggered via an API call. You will be provided with a set of CSV files that you will need to process, derive some features from, and then upload into a database table.

### Requirements
- Python 3.7+
- Docker
- PostgreSQL

### ETL Process
Below are the steps that I've followed inorder to complete this challenge
1. Extract
    <br> The Extract stage is used to extract data from data sources. The extract.py file in our case is only reading from various csv files depending on the directory specified and return the dataframe.
2. Transform
    <br> The Transform stage is where I've performed feature derivation. From the provided CSV files, I need to derive the following features:
    - Total experiments a user ran.
      <br> users.csv and experiments.csv would be merged on user_id. Then count all experiment_ids by grouping on user_id.
    - Average experiments amount per user.
      <br> users.csv and experiments.csv would be merged on user_id. Then count all experiment_ids by grouping on user_id. Taking total experiments into picture, every user's average experiment count = count(experiment_id)/total_experiments
    - User's most commonly experimented compound.
      <br> experiments.csv is first divided on experiment_compound_ids. This would be merged to compounds.csv on compound_id. Then count all compound_ids per user and sort it in decreasing order. Filter down the topmost compound per user. 
3. Load
    <br> The Load stage is used to load the data that has been transformed to the data warehouse or database. I've used psycopg2 to help me connect python with PostgreSQL. Not just that, I also used argparse to help me create command arguments in python therefore, I can input csv files directory, database name, host name, username, password, and port of PostgreSQL flexibly.

## Installation

1. Clone the repository.
2. Download and setup Docker according to your OS.
3. Open a terminal and run below commands.
4. We first need postgresql and pgadmin images for our docker container.
    ```
    docker pull postgres
    docker pull dpage/pgadmin4
    ```
5. After creating PostgreSQL and PgAdmin4 images, we have to create network. Because we have separated container for PostgreSQL and PgAdmin4. Therefore, we need to connect them using docker network. To do this we need to write this command in your command line:
    ```
    docker network create [network_name]
    ```
    In our case the network name is `backend_project_network`
6. We also need to create volume to save our data in docker therefore, every time we run and stop our container, the data will always there. To do this we use this command line:
    ```
    docker volume create [volume_name]
    ```
    In our case the volume name is `backend_project`
7. Now that we have prerequisites installed, we can create the container with all the images connected. We need a `docker-compose.yaml` file which is present in the repository.
    ```
    docker-compose up
    ```
8. After successfully setting up your docker container, we can access (localhost:8080) and setup our databases in postgres using pgAdmin4.
9. Login to pgAdmin4 website using credentials specified in `docker-compose.yaml` for image dpage/pgadmin4. 
![ScreenShot](/screenshots/screenshot1.png)<br>
10. Register a new server with postgres details.
![ScreenShot](/screenshots/screenshot2.png)<br>
11. Specify a new server name and postgres credentials details according to the `docker-compose.yaml` file.
![ScreenShot](/screenshots/screenshot3.png)<br>
12. Not only for PostgreSQL and PgAdmin4 we also need to build Image for our Docker
    python. In this case we create `dockerfile` :
    ```
    docker build -t python-etl .
    ```
13. After you build the image you can run it with this command:
    ```
    docker run -it --network=backend_project_network\
    python-etl\
    -d \data\
    -db exampledb\
    -hs pgdatabase\
    -u postgres\
    -pass backendproject\
    -p 5432
    ```
14. Then ETL process will completed.
15. If ETL runs successfully, there would be 3 tables with all results stored under database specified in `docker-compose.yaml` file.
