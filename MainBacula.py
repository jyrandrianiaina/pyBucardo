from BaculaAction import BaculaAction
from RemoteDatabaseCreation import RemoteDatabaseCreation
from FileTransfert import FileTransfert

class MainBacula(object):
    def __init__(self):
        self.database_source_host   = "db1"
        self.database_target_host   = "db2"
        self.database_user          = "postgres"
        self.database_port          = "5432"
        self.database_password      = "postgres"
        self.BaculaAction           = BaculaAction()
        self.RemotedatabaseCreation = RemoteDatabaseCreation()
        self.FileTransfert          = FileTransfert()

    def main_principale(self):
        #check if bacula is installed
        bacula_binary = "/usr/local/bin/bucardo"
        BaculaAction().BaculaIsInstalled(bacula_binary)
        #stop bacula
        BaculaAction().BaculaWhatAction(bacula_binary, 'stop')
        database_name = raw_input("Enter Database's name: ")
        #remove database from bacula
        database_source_name = database_name+"_source"
        BaculaAction().BaculaManageDatabase(bacula_binary, 'remove', database_source_name,'','','','','')
        database_target_name = database_name+"_target"
        BaculaAction().BaculaManageDatabase(bacula_binary, 'remove', database_target_name,'','','','','')

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
        BaculaAction().BaculaManageDatabase(bacula_binary,
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
        BaculaAction().BaculaManageDatabase(bacula_binary,
                                            'add',
                                            database_name,
                                            self.database_source_host,
                                            self.database_port,
                                            self.database_user,
                                            self.database_password,
                                            database_target_name
                                            )
        #Adding Herd to the database
        #database_herd_name = database_name+"_herd"
        BaculaAction().baculatablesmanagement(bacula_binary, database_name)
        #Creating sync for the database
        BaculaAction().baculasyncmanagement(bacula_binary, database_name)
        #Start Bucardo
        BaculaAction().BaculaWhatAction(bacula_binary,'start')
        #Show Bacula status
        BaculaAction().BaculaWhatAction(bacula_binary, 'status')

Bacula = MainBacula()
Bacula.main_principale()





