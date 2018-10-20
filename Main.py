from BucardoAction import BucardoAction
from RemoteDatabaseCreation import RemoteDatabaseCreation
from FileTransfert import FileTransfert
import sys

class Main(object):
    def __init__(self):
        self.database_source_host   = ""
        self.database_target_host   = ""
        self.database_user          = "postgres"
        self.database_port          = "5432"
        self.database_password      = "postgres"
        self.BucardoAction           = BucardoAction()
        self.RemotedatabaseCreation = RemoteDatabaseCreation()
        self.FileTransfert          = FileTransfert()

    def main_principale(self):
        #check if bacula is installed
        cmdargs = str(sys.argv)
        if (str(sys.argv[1]) == ""):
            print ("Error. You must specify a source host")
            exit(-1)
        if (str(sys.argv[2]) == ""):
            print ("Error. You must specify a target host")
            exit(-1)
        if (str(sys.argv[3]) == ""):
            print ("Error. You must specify a database name")
            exit(-1)
        self.database_source_host = str(sys.argv[1])
        self.database_target_host = str(sys.argv[2])
        database_name = str(sys.argv[3])

        print ("Command will be: \npython Main.py " +self.database_source_host+ " " +self.database_target_host+ " "+database_name);
        #exit(-1)
        #database_name = raw_input("Enter Database's name: ")
        bucardo_binary = "/usr/local/bin/bucardo"
        BucardoAction().BaculaIsInstalled(bucardo_binary)
        #stop bacula
        BucardoAction().BaculaWhatAction(bucardo_binary, 'stop')

        #remove database from bacula
        database_source_name = database_name+"_source"
        BucardoAction().BaculaManageDatabase(bucardo_binary, 'remove', database_source_name,'','','','','')
        database_target_name = database_name+"_target"
        BucardoAction().BaculaManageDatabase(bucardo_binary, 'remove', database_target_name,'','','','','')

        #create database in the target
        RemoteDatabaseCreation().createdatabase(database_name,
                                                self.database_target_host,
                                                self.database_port,
                                                self.database_user,
                                                self.database_password)

        ##get into target host
        FileTransfert().generateschemaintosource(database_name,
                                                 self.database_source_host,
                                                 self.database_user,
                                                 self.database_password)
        #Send schema to the target database
        FileTransfert().sendschematotarget(database_name,
                                           self.database_source_host,
                                           self.database_user,
                                           self.database_password,
                                           self.database_target_host)
        #Load schema into target database
        FileTransfert().loadschemaintotarget(database_name,
                                             self.database_target_host,
                                             self.database_user,
                                             self.database_password)
        #Create and add database source into bucardo
        #database_bucardo = database_name+"_source"
        BucardoAction().BaculaManageDatabase(bucardo_binary,
                                            'add',
                                            database_name,
                                            self.database_source_host,
                                            self.database_port,
                                            self.database_user,
                                            self.database_password,
                                            database_source_name
                                            )
        #Create and add database target into bucardo
        #database_bucardo = database_name+"_target"
        BucardoAction().BaculaManageDatabase(bucardo_binary,
                                            'add',
                                            database_name,
                                            self.database_target_host,
                                            self.database_port,
                                            self.database_user,
                                            self.database_password,
                                            database_target_name
                                            )
        #Adding Herd to the database
        #database_herd_name = database_name+"_herd"
        BucardoAction().baculatablesmanagement(bucardo_binary, database_name)
        #Creating sync for the database
        BucardoAction().baculasyncmanagement(bucardo_binary, database_name)
        #Start Bucardo
        BucardoAction().BaculaWhatAction(bucardo_binary,'start')
        #Show Bacula status
        BucardoAction().BaculaWhatAction(bucardo_binary, 'status')

    def usage(self):
        print ("Usage: python Main.py [source] [target] [database_name]")

Bucardo = Main()
Bucardo.usage()
Bucardo.main_principale()





