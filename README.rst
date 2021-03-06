redshift_tool - Elegant data load from Pandas to Redshift
=========================================================

| 1.Overview_
| 2.Installation_
| 3.Usages-Guidelines_
| 4.Examples_
| 5.Support_
| 6.References_ 

1.Overview
==========
**redshift_tool** is a python package which is prepared for loading pandas data frame into redshift table. This package is making it easier for bulk uploads, where the procedure for uploading data consists in generating various CSV files, uploading them to an S3 bucket and then calling a copy command on the server, this package helps with all those tasks in encapsulated functions. There are two methods of data copy.

| a). Append:- It simply copies the data or adds the data at the end of existing data in a redshift table.

| b). Upsert:- It is used for updating the old record as per provided upsert Id/Ids and also copy the new records into the table.    

redshift_tool is purely implemented in Python.

2.Installation
==============
| **To install the library, use below command**
|    $ pip install redshift_tool

.. note::

    During the installation of the package please verify that all the required dependencies installed successfully, if not try to install them one by one manually.

3.Usages-Guidelines
===================
Uses Commands 
   >>> import redshift_tool
   >>>  redshift_tool.query(data,method,redshift_auth=None,s3_auth=None,schema=None,table=None,
                            primarykey=None,sortkey=None,distkey=None,upsertkey=None)

a). data:- It will take any pandas Data frame.

   >>> data= df
               
| b). method: There are two methods of writing pandas data frame as defined above either by 'append' or 'upsert'.

   >>> method='append/upsert'
                    
| c). redshift_auth:- To write the data into redshift, it is required to establish the redshift connection. It is the connection's credential parameter. 

   >>> redshift_auth= {'db':'database_name','port':port,'user':'user','pswd':'password','host':'host'}

| d). s3_auth:- AWS S3 is used to enhance the performance of the copy operation. It is used to pass the AWS S3 credentials as well S3 bucket name. S3 Bucket is a place where you can put your files temporary for coping into redshift tables.

   >>> s3_auth = {'accesskey':'aws_access_key','secretkey':'aws_secret_key','bucket':'s3_bucket_name'}
               
| e). schema:- If there is any schema name associated with your database in which table will be created.

   >>> schema='Schema_name'
                
| f). table:- Target table name to write pandas.

 1. If target table is already exist, function will be used to copy/usert data into exiting table. 

 2. A user can proceed with two steps in case of target table is not exist.

  2.1. Use SQL Create staatement to create taget table manualy.

  2.2. This libaray can also create target table on the basis of input pandas dataframe columns and datatypes so before using the command make sure all the column names and datatypes of pandas dataframe set properly.
                
 >>> table='table_name'
                
| g). primarykey:- A primary key is a special relational database table column (or combination of columns) designated to uniquely identify all table records. 

While creating the table by default, if it is required to define any column as primary key, then pass the column name in a tuple in this parameter.

   >>> primarykey=('Primary_Key') or 
   >>> primarykey=('Primary_Key1','Primary_Key2')
    
| h). sortkey:- A sortkey is a field or column that is used to sort the data. It can be a single key as well as multiple keys.

While creating the table by default, if we need to define any column as a sort key, then pass the column name in a tuple in this parameter.

   >>> sortkey=('sort_key') or  
   >>> sortkey=('sort_key1','sort_key2')  
    
| i). distkey(Default - Even):- A distribution key is a column that is used to determine the parallel data processing task with all available redshift slices.

   >>> distkey=('distribution_key')
                  
| j). upsertkey:- During the upsert method of data loading, we need to pass upsert key by which key old record will get updated & new will be added. It will be also added into a tuple.

   >>> upsertkey=('upsertkey') or 
   >>> upsertkey=('upsertkey1','upsertkey2')
 

4.Examples
==========
Append or Copy data without primarykey, sortkey, distributionkey
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Eg. 
      >>> import redshift_tool
      >>> df= pandas.DataFrame()
      >>> redshift_tool.query(data=df,method='append',
          redshift_auth={'db':'database_name','port':port,'user':'user','pswd':'password','host':'host'},
          s3_auth={'accesskey':'aws_access_key','secretkey':'aws_secret_key','bucket':'s3_bucket_name'},
          schema='shcema_name',table='redshift_table_name')

Append or Copy data with primarykey, sortkey, distributionkey
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Eg. 
     >>> import redshift_tool
     >>> df= pandas.DataFrame()
     >>> redshift_tool.query(data=df,method='append',
         redshift_auth={'db':'database_name','port':port,'user':'user','pswd':'password','host':'host'},
         s3_auth={'accesskey':'aws_access_key','secretkey':'aws_secret_key','bucket':'s3_bucket_name'},
         schema='shcema_name',table='redshift_table_name',primarykey=(''primarykey'),
         sortkey=('sortkey'),distkey=('distributionkey'))

 
Upsert data without primarykey, sortkey, distributionkey
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Eg. 
    >>> import redshift_tool
    >>> df= pandas.DataFrame()
    >>> redshift_tool.query(data=df,method='append',
        redshift_auth={'db':'database_name','port':port,'user':'user','pswd':'password','host':'host'},
        s3_auth={'accesskey':'aws_access_key','secretkey':'aws_secret_key','bucket':'s3_bucket_name'},
        schema='shcema_name',table='redshift_table_name',upsertkey=('upsertkey'))

Upsert data with primarykey, sortkey, distributionkey
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Eg. 
    >>> import redshift_tool
    >>> df= pandas.DataFrame()
    >>> redshift_tool.query(data=df,method='append',
        redshift_auth={'db':'database_name','port':port,'user':'user','pswd':'password','host':'host'},
        s3_auth={'accesskey':'aws_access_key','secretkey':'aws_secret_key','bucket':'s3_bucket_name'},
        schema='shcema_name',table='redshift_table_name',primarykey=('primarykey'),
        sortkey=('sortkey'),distkey=('distributionkey'),upsertkey=('upsertkey'))


5.Support
==========
 +--------------------+----------------------------------------+
 |**Operating System**|Linux/OSX/Windows                       |
 +--------------------+----------------------------------------+
 |**Python Version**  |2/2.7/3/3.2/3.3/3.4/3.5/3.6/3.7 etc.    |
 +--------------------+----------------------------------------+ 


6.References
============
| Many thanks to the developers of dependent packages. Please use the below links to get deeper knowledge about required packages:-

| **PANDAS:** https://pypi.org/project/pandas/
| **NUMPY:** https://pypi.org/project/numpy/
| **PSYCOPG2:** https://pypi.org/project/psycopg2/
| **BOTO3:** https://pypi.org/project/boto3/