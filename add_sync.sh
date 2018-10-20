#!/bin/sh
echo "Arret de bucardo........"
bucardo stop
echo  "Veuillez entrer le nom de la base de donnees:"
read dbname
dbname_source=$dbname"_source"
dbname_destination=$dbname"_destination"
dbname_herd=$dbname"_herd"
dbname_sync="db_"$dbname"_sync"
bucardo remove db $dbname_source
bucardo remove db $dbname_destination
echo "-----------------------------------"
echo "Les parametres sont:"
echo "Source: " $dbname_source
echo "Destination: "$dbname_destination
echo "Herd: "$dbname_herd
echo "Sync: "$dbname_sync
echo "#####################################"
echo "Creation de la base de donnees source: $dbname_source"
bucardo add db $dbname_source dbhost=db1 dbport=5432 dbname=$dbname dbuser=postgres dbpass=postgres
echo "Creation de la base de donnees destination: $dbname_destination"
ssh postgres@db2 "createdb $dbname"
schema_name=$dbname"_schema.sql"
echo "Creation du schema pour la base $dbname : schema = $schema_name";
ssh postgres@db1 "pg_dump $dbname $TABLES --schema-only | grep -v 'CREATE TRIGGER' | grep -v '^--' | grep -v '^$' | grep -v '^SET' | grep -v 'OWNER TO' > $schema_namels"
echo "Telechargement du schema $schema_name"
scp postgres@db1:/var/lib/postgresql/$schema_name .
echo "Envoi du schema $schema_name vers db2"
scp $schema_name postgres@db2:/var/lib/postgresql/
echo "Imporation du schema $schema_name dans db2"
ssh postgres@db2 "psql $dbname -f $schema_name"
echo "Imporation termine"
bucardo add db $dbname_destination dbhost=db2 dbport=5432 dbname=$dbname dbuser=postgres dbpass=Root@2015ET
echo "Ajout de tous les tables"
bucardo add all tables db=$dbname_source herd=$dbname_herd
echo "Creation de la synchronisation"
bucardo add sync $dbname_sync relgroup=$dbname_herd dbs=$dbname_source:source,$dbname_destination:target onetimecopy=2
echo "Demarrage de bucardo..."
bucardo start
bucardo status $dbname_sync
echo "###############Fin####################"
