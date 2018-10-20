import os
import os.path

class BucardoAction(object):

    def BaculaIsInstalled(self, bacula_bin):
        if (os.path.isfile(bacula_bin)):
            print ("Bacula is installed on this computer")
        else:
            print ("Bacula is not installed. Program will exit")
            exit(-1)

    def BaculaWhatAction(self,bacula_binary, bacula_action):
        if (bacula_action == "status"):
            print ("Bacula Status: ")
            os.system(bacula_binary +" "+bacula_action)
        else:
            print ("Bacula action: " +bacula_action)
            os.system(bacula_binary +" "+bacula_action)

    def BaculaManageDatabase(self,
                             bacula_binary,
                             database_action,
                             database_name,
                             database_host,
                             database_port,
                             database_user,
                             database_password,
                             database_bucardo):
        if (database_action == "add"):
            print ("Add a new database "+database_name+ " into Bucardo")
            os.system(bacula_binary +" "+ database_action +
                      " db " + database_bucardo+
                      " dbhost="+database_host+
                      " dbport="+database_port+
                      " dbname="+database_name+
                      " dbuser=" +database_user+
                      " dbpass=" +database_password
                      )
        if (database_action == "remove"):
            print ("Delete Database "+database_name+" in Bucardo")
            os.system(bacula_binary +" "+ database_action + " db " + database_name)
            #os.system(bacula_binary +" "+ database_action + " db " + database_name)

    def baculatablesmanagement(self,bacula_binary, database_name):
        print ("Adding all tables to bucardo into the database: "+database_name)
        database_herd = database_name+"_herd"
        database_name_source = database_name+"_source"
        os.system(bacula_binary + " add all tables db="+database_name_source+ " herd=" +database_herd)

    def baculasyncmanagement(self, bacula_binary, database_name):
        database_name_source = database_name+"_source"
        database_name_target = database_name+"_target"
        database_sync = database_name+"_sync"
        database_herd = database_name+"_herd"

        print ("Create and add new sync to the database "+database_name+" into Bucardo")

        os.system(bacula_binary+" add sync "+database_sync+
                  " relgroup= "+database_herd+" dbs="+database_name_source+":source,"
                  ""+database_name_target+":target onetimecopy=2")


















