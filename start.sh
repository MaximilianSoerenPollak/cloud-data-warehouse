#!/bin/sh

echo "Starting up the Redshift cluster..."
python aws_startup.py 
echo "Creating all tables..."
python create_tables.py 
echo "Inserting data into the tables..."
python etl.py 
echo "All done. If you want to delete the Cluster just type 'python aws_shutdown.py'"

