import scp
import pexpect
import os
import time
import sys
from pexpect import pxssh

class FileTransfert(object):

    def generateschemaintosource(self,
                       database_name,
                       database_source_host,
                       source_host_user,
                       source_host_password):
        ssh_connexion = pxssh.pxssh()

        if not ssh_connexion.login(database_source_host, source_host_user, source_host_password):
            print ("Unable to connect to ssh server")
            exit(-1)
        else:
            database_schema_name = database_name+"_schema.sql"
            print ("Connexion etablished. Postgresql's schema for database "+database_name+" will be generated")
            ssh_connexion.sendline("pg_dump "+database_name+" $TABLES --schema-only | grep -v \'CREATE TRIGGER\' | grep -v \'^--\' | grep -v \'^$\' | grep -v \'^SET\' | grep -v \'OWNER TO\' > "+database_schema_name)
            ssh_connexion.prompt()
            #ssh_connexion.timeout=300
            print("" +ssh_connexion.before)
            ssh_connexion.logout()

    def sendschematotarget(self,
                           database_name,
                           database_source_host,
                           source_host_user,
                           source_host_password,
                           database_target_host):
        ssh_connexion = pxssh.pxssh()
        if not ssh_connexion.login(database_source_host, source_host_user, source_host_password):
            print ("Unable to connect to ssh server")
            exit(-1)
        else:
            database_schema_name = database_name+"_schema.sql"
            target_host_user = source_host_user
            target_host_password = source_host_password
            print ("Connexion with source etablished. Postgresql's schema for database "+database_name+" will be sent to "+database_target_host)
            ssh_connexion.sendline("scp "+database_schema_name+" "+target_host_user+"@"+database_target_host+":~")
            ssh_connexion.prompt()
            print("" +ssh_connexion.before)
            ssh_connexion.logout()

    def loadschemaintotarget(self,
                             database_name,
                             database_target_host,
                             target_host_user,
                             target_host_password):
        ssh_connexion = pxssh.pxssh()

        if not ssh_connexion.login(database_target_host, target_host_user, target_host_password):
            print ("Unable to connect to ssh server")
            exit(-1)
        else:
            database_schema_name = database_name+"_schema.sql"
            print ("Connexion etablished. Postgresql's schema for database "+database_name+" will be loaded to "+database_target_host)
            ssh_connexion.sendline("psql "+database_name+" -f " +database_schema_name)
            ssh_connexion.prompt()
            #ssh_connexion.timeout=300
            print("" +ssh_connexion.before)
            ssh_connexion.logout()


