import psycopg2, pandas as pd, numpy as np, boto3
import io,sys
def query(data,method,redshift_auth=None,s3_auth=None,schema=None,table=None,primarykey=None,sortkey=None,distkey=None,upsertkey=None):
    con = psycopg2.connect("dbname='"+str(redshift_auth['db'])+"' port='"+str(redshift_auth['port'])+"' user='"+str(redshift_auth['user'])+"' password='"+str(redshift_auth['pswd'])+"' host='"+str(redshift_auth['host'])+"'")
    cur = con.cursor()
    cur.execute("select count(*) as slices from stv_slices")
    availableslices = int(cur.fetchall()[0][0])
    cur.execute("select exists (select table_name from information_schema.tables where table_schema='"+str(schema)+"' and table_name='"+str(table)+"')")
    table_ifexits = str(cur.fetchall()[0][0])
    con.commit()
    cur.close()
    con.close()
    print("\x1B[3mInfo: Your redshift cluser have "+str(availableslices)+" slices and "+str(len(data.index))+" records in supplied pandas dataframe.\x1B[23m")
    if table_ifexits == 'True':
        print("Table already exists into provided schema, Proceeding to next step.")
    else:
        print("Table is not available into provided schema, Started creating table.")
        create_stmnt = pd.io.sql.get_schema(data,str(schema)+str(".")+str(table),keys=primarykey).replace('\n','').replace('\"','').replace('CREATE TABLE','CREATE TABLE IF NOT EXISTS').lower()
        if primarykey==None:
            create_stmnt = create_stmnt
        else:
            create_stmnt = create_stmnt.replace('  constraint '+str(schema)+str('.')+str(table)+str('_pk'),'')

        if distkey==None:
            create_stmnt = create_stmnt+' diststyle even'
        else:
            create_stmnt = create_stmnt+' distkey('+str(distkey).lower()+')'
            
        if sortkey==None:
            create_stmnt = create_stmnt
        else:
            create_stmnt = create_stmnt+(' sortkey('+str(sortkey).lower()+')').replace('((','(').replace('))',')').replace("'","")


            
        con = psycopg2.connect("dbname='"+str(redshift_auth['db'])+"' port='"+str(redshift_auth['port'])+"' user='"+str(redshift_auth['user'])+"' password='"+str(redshift_auth['pswd'])+"' host='"+str(redshift_auth['host'])+"'")
        cur = con.cursor()
        cur.execute(create_stmnt)
        con.commit()
        cur.close()
        con.close()
        print("\x1B[3mTable created sucessfully.\x1B[23m")
    
    print("Started uploading pandas dataframe to S3 bucket(.csv)")
    if len(data.index) <= 3000:
        s3 = boto3.client('s3', aws_access_key_id=str(s3_auth['accesskey']),aws_secret_access_key=str(s3_auth['secretkey']))
        if int(sys.version[0]) > 2:
            csv_buffer = io.StringIO()
        else:
            csv_buffer = io.BytesIO()
        data.to_csv(csv_buffer, index=False)
        s3.put_object(Bucket=str(s3_auth['bucket']), Key='tmp_pkg_pandas2redshift.csv',Body=csv_buffer.getvalue())
    elif len(data.index) > 3000:
        s3 = boto3.client('s3', aws_access_key_id=str(s3_auth['accesskey']),aws_secret_access_key=str(s3_auth['secretkey']))
        splitlist = np.array_split(data, int(availableslices))
        for i in range(0,len(splitlist)):
            if int(sys.version[0]) > 2:
                csv_buffer = io.StringIO()
            else:
                csv_buffer = io.BytesIO()            
            splitlist[i].to_csv(csv_buffer, index=False)
            s3.put_object(Bucket=str(s3_auth['bucket']), Key='tmp_pkg_pandas2redshift_'+str(i)+'.csv',Body=csv_buffer.getvalue())
    print("\x1B[3mDataframe uploaded sucessfully.\x1B[23m")
    
    print("Started copying uploaded S3 files into redshift table with applied method.")
    if method.lower()=='append':
        con = psycopg2.connect("dbname='"+str(redshift_auth['db'])+"' port='"+str(redshift_auth['port'])+"' user='"+str(redshift_auth['user'])+"' password='"+str(redshift_auth['pswd'])+"' host='"+str(redshift_auth['host'])+"'")
        cur = con.cursor()
        cur.execute("COPY "+str(schema)+str('.')+str(table)+" from 's3://"+str(s3_auth['bucket'])+"/tmp_pkg_pandas2redshift' "+"credentials 'aws_access_key_id="+str(s3_auth['accesskey'])+";aws_secret_access_key="+str(s3_auth['secretkey'])+"' DELIMITER ',' IGNOREHEADER 1 csv")
        con.commit()
        cur.close()
        con.close()
    elif method.lower()=='upsert':
        create = "create temp table "+str("stage")+str(table)+str(" (like ")+str(table)+")"
        copy = "COPY "+str("stage")+str(table)+" from 's3://"+str(s3_auth['bucket'])+"/tmp_pkg_pandas2redshift' "+"credentials 'aws_access_key_id="+str(s3_auth['accesskey'])+";aws_secret_access_key="+str(s3_auth['secretkey'])+"' DELIMITER ',' IGNOREHEADER 1 csv"
        s = ""
        if isinstance(upsertkey,tuple):
            for i in upsertkey:
                s+=str(schema)+str(".")+str(table)+str(".")+str(i)+"="+str('stage')+str(table)+str(".")+str(i)+" and "
        else:
            s+=str(schema)+str(".")+str(table)+str(".")+str(upsertkey)+"="+str('stage')+str(table)+str(".")+str(upsertkey)+" and "
        delete = "delete from "+str(schema)+str(".")+str(table)+" using "+str('stage')+str(table)+" where "+str(s).replace('', '')[:-5]
        insert = "insert into "+str(schema)+str(".")+str(table)+" select * from "+str('stage')+str(table)
        drop = "drop table "+str('stage')+str(table)
        
        con = psycopg2.connect("dbname='"+str(redshift_auth['db'])+"' port='"+str(redshift_auth['port'])+"' user='"+str(redshift_auth['user'])+"' password='"+str(redshift_auth['pswd'])+"' host='"+str(redshift_auth['host'])+"'")
        cur = con.cursor()
        print("-> Creating stagging table.")
        cur.execute(create)
        print("-> Copying data into stagging table.")
        cur.execute(copy)
        cur.execute("begin transaction")
        print("-> Deleting row from main table which needs to be upadted.")
        cur.execute(delete)
        print("-> Copying updated data from staging to main table.")
        cur.execute(insert)
        cur.execute("end transaction;")
        print("-> Dropping stagging table.")
        cur.execute(drop)
        con.commit()
        cur.close()
        con.close()
    print("\x1B[3mCopied data into redshift sucessfully.\x1B[23m")
    
    print("Started deleting temprory files from S3 bucket.")
    s3 = boto3.client('s3', aws_access_key_id=str(s3_auth['accesskey']),aws_secret_access_key=str(s3_auth['secretkey']))
    objects_to_delete = s3.list_objects(Bucket=s3_auth['bucket'], Prefix="tmp_pkg_pandas2redshift")
    delete_keys = {'Objects' : []}
    delete_keys['Objects'] = [{'Key' : k} for k in [obj['Key'] for obj in objects_to_delete.get('Contents', [])]]
    s3.delete_objects(Bucket=s3_auth['bucket'], Delete=delete_keys)
    print("\x1B[3mDeleted temprory files from S3 bucket.\x1B[23m")







