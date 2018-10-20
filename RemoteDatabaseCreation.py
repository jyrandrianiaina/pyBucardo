import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class RemoteDatabaseCreation(object):

    def createdatabase(self,database_name, database_target_host, database_port, database_user, database_password):
        print ("Create database: "+database_name+" into the host "+database_target_host)
        try:
            connexion = psycopg2.connect(
                host = database_target_host,
                port = database_port,
                database = 'postgres',
                user = database_user,
                password = database_password)
            print ("Database postgres is opened  succefully. I will create the database: "+database_name)
            connexion.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            db_cursor = connexion.cursor()
            try:
                #print ("Drop database "+database_name)
                #db_cursor.execute("DROP DATABSE "+database_name)
                db_cursor.execute("CREATE DATABASE "+database_name)
                print ("Success. Database "+database_name+" was created ")
                db_cursor.close()
            except:
                print ("Error while creating database " +database_name)
                exit(-1)
        except:
            print("There was an error. Program will exit.")
            exit(-1)