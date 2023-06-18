from extract import extract_data
from transform import transform_data
import psycopg2
import argparse

def load_data(directory, database, host, user, password, port):

    connection = psycopg2.connect(database=database,
                        host=host,
                        user=user,
                        password=password,
                        port=port)

    cursor = connection.cursor()

    print("loading data...")
    usersdf = extract_data(directory, 'users.csv')
    expdf = extract_data(directory, 'user_experiments.csv')
    compoundsdf = extract_data(directory, 'compounds.csv')

    print("transforming data...")
    q1, q2, q3 = transform_data(usersdf, expdf, compoundsdf)

    #create tables
    query_create_table1 = f"CREATE TABLE IF NOT EXISTS q1(\
    USER_ID SERIAL PRIMARY KEY,\
    NAME VARCHAR(50) NOT NULL,\
    COUNT INT);"
    query_create_table2 = f"CREATE TABLE IF NOT EXISTS q2(\
    USER_ID SERIAL PRIMARY KEY,\
    NAME VARCHAR(50) NOT NULL,\
    AVERAGE FLOAT);"
    query_create_table3 = f"CREATE TABLE IF NOT EXISTS q3(\
    USER_ID SERIAL PRIMARY KEY,\
    COMPOUND_ID INT,\
    COMPOUND_NAME VARCHAR(50) NOT NULL,\
    COMPOUND_STRUCTURE VARCHAR(50) NOT NULL,\
    COUNT INT);"

    cursor.execute(query_create_table1)
    cursor.execute(query_create_table2)
    cursor.execute(query_create_table3)

    #start loading data
    print('loading data...')
    for index, row in q1.iterrows():
        query_insert_value = f"INSERT INTO q1 (USER_ID, NAME, COUNT) VALUES ('{row[0]}', \
            '{row[1]}', {row[2]})" 
        cursor.execute(query_insert_value)
    for index, row in q2.iterrows():
        query_insert_value = f"INSERT INTO q2 (USER_ID, NAME, AVERAGE) VALUES ('{row[0]}', \
            '{row[1]}', {row[2]})" 
        cursor.execute(query_insert_value)
    for index, row in q3.iterrows():
        query_insert_value = f"INSERT INTO q3 (USER_ID, COMPOUND_ID, COMPOUND_NAME, COMPOUND_STRUCTURE, COUNT) VALUES ('{row[0]}', \
            {row[1]}, '{row[2]}', '{row[3]}', {row[4]})" 
        cursor.execute(query_insert_value)
    connection.commit()

    cursor.close()
    connection.close()

    print("etl success...\n")

    return "all processes completed"

if __name__ == "__main__":

    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    parser.add_argument("-d", "--directory", help = "file path of your dataset")
    parser.add_argument("-db", "--database", help = "database name")
    parser.add_argument("-hs", "--host", help = "your postgresql host")
    parser.add_argument("-u", "--user", help = "postgresql username")
    parser.add_argument("-pass", "--password", help = "postgresql password")
    parser.add_argument("-p", "--port", help = "postgresql port")

    # Read arguments from command line
    args = parser.parse_args()

    load_data(args.directory, args.database, args.host, args.user, args.password, args.port)