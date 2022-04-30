# This file starts all AWS services that we need. 
# THIS HAS TO RUN FIRST 
""" 
This scrip is going to make a new IAM_role (if not so done yet) will then 
spin up a redshift cluster and also detect and see if it is avialable and up. 

So once this Script runs we can interact with the Redshift cluster and can be sure we 
have a connection to it. 

So this scrips ALWAYS should run first.

"""

# ----- CODE ----
import configparser
import boto3
import pandas as pd
import psycopg2
import json
import botocore
from time import sleep
# ---- Read Config ----
config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))

KEY                   = config.get('KEYS','ACCESS_KEY')
SECRET                = config.get('KEYS','SECRET_KEY')

DWH_CLUSTER_TYPE      = config.get("DWH","DWH_CLUSTER_TYPE")
DWH_NUM_NODES         = config.get("DWH","DWH_NUM_NODES")
DWH_NODE_TYPE         = config.get("DWH","DWH_NODE_TYPE")

DWH_CLUSTER_IDENTIFIER= config.get("CLUSTER","DWH_CLUSTER_IDENTIFIER")
DWH_DB                = config.get("CLUSTER","DB_NAME")
DWH_DB_USER           = config.get("CLUSTER","DB_USER")
DWH_DB_PASSWORD       = config.get("CLUSTER","DB_PASSWORD")
DWH_PORT              = config.get("CLUSTER","DB_PORT")

DWH_IAM_ROLE_NAME     = config.get("CLUSTER", "DWH_ROLE")

# ---- Declaring AWS SDK instances ----

ec2 = boto3.resource('ec2',
                       region_name="us-west-2",
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET
                )

iam = boto3.client("iam",
                    region_name="us-west-2",
                    aws_access_key_id=KEY,
                    aws_secret_access_key=SECRET
                )


redshift = boto3.client('redshift',
                       region_name="us-west-2",
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET
                )

# ---- Functions ----

def set_configs(section, configname, value):
    config.set(section, configname, value)
    with open('dwh.cfg', 'w') as configfile:
        config.write(configfile)
    print(f"Config: {configname} written in {section} ")

# Create the IAM role as well as assign policy
def create_iam_role():
    try:
        dwhRole = iam.create_role(
            Path='/',
            RoleName=DWH_IAM_ROLE_NAME,
            Description = "Allows Redshift clusters to call AWS services on your behalf.",
            AssumeRolePolicyDocument=json.dumps(
                {'Statement': [{'Action': 'sts:AssumeRole',
                   'Effect': 'Allow',
                   'Principal': {'Service': 'redshift.amazonaws.com'}}],
                 'Version': '2012-10-17'})
        )
    except iam.exceptions.EntityAlreadyExistsException as e:
        print("Role already created. Skipping creation.")
        pass
    iam.attach_role_policy(RoleName=DWH_IAM_ROLE_NAME,
                           PolicyArn="arn:aws:iam::aws:policy/amazons3readonlyaccess"
                          )['ResponseMetadata']['HTTPStatusCode']
    rolearn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']
    set_configs("IAM", "ROLE_ARN", rolearn)
    return rolearn


# Create Redshift Cluster and check if one with same name already there.
def create_cluster(rolearn):
    try:
        response = redshift.create_cluster(        
            #HW
            ClusterType=DWH_CLUSTER_TYPE,
            NodeType=DWH_NODE_TYPE,
            NumberOfNodes=int(DWH_NUM_NODES),

            #Identifiers & Credentials
            DBName=DWH_DB,
            ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
            MasterUsername=DWH_DB_USER,
            MasterUserPassword=DWH_DB_PASSWORD,
            
            #Roles (for s3 access)
            IamRoles=[rolearn]  
        )
        return True
    except redshift.exceptions.ClusterAlreadyExistsFault as e:
        print("Already created a cluster with this name.")
        return True
    except Exception as e:
        print(e)
        sleep(5)
        print("Trying again, failed to create cluster.")
        create_cluster(rolearn)

# Function to check what the current status of our cluster is
# Note: This dataframe is bad. it's just pretty to look at but bad to work with (see Key/Value).  
def prettyRedshiftProps(props):
    keysToShow = ["ClusterIdentifier", "NodeType", "ClusterStatus", "MasterUsername", "DBName", "Endpoint", "NumberOfNodes", 'VpcId']
    x = [(k, v) for k,v in props.items() if k in keysToShow]
    return pd.DataFrame(data=x, columns=["Key", "Value"])

# Function that runs and only returns true once our cluster is up.
def check_redshift_cluster(props):
    while True:
        try:
            df = prettyRedshiftProps(props)
            if df.iloc[2]["Value"] == "available":
                return True, df.iloc[5]["Value"]["Address"]
        except Exception as e:
            print("Cluster not Available yet. Trying again.")
            sleep(10)
# Open ports of our ec2 instance to Redshift and S3
def open_port(props):
    try:
        vpc = ec2.Vpc(id=myClusterProps['VpcId'])
        defaultSg = list(vpc.security_groups.all())[0]
        defaultSg.authorize_ingress(
            GroupName=defaultSg.group_name,
            CidrIp='0.0.0.0/0',
            IpProtocol='TCP',
            FromPort=int(DWH_PORT),
            ToPort=int(DWH_PORT)
        )
    except botocore.exceptions.ClientError as e:
        print("This rule has already been created and is in place.")
    except Exception as e:
        print(e)

# Check if we can establish a connection to our DWH.
def check_connection(DWH_ENDPOINT):
    conn_string="postgresql://{}:{}@{}:{}/{}".format(DWH_DB_USER, DWH_DB_PASSWORD, DWH_ENDPOINT, DWH_PORT,DWH_DB)
    try:
        conn = psycopg2.connect(conn_string)
        return conn
    except psycopg2.DatabaseError as e:
        print(e)
        print("Could not connect to DB, trying again.")
        sleep(5)
        check_connection()
       

# Call everytihng in the right order once we execute the file.
if __name__ == '__main__':
    roleArn = create_iam_role()
    while not create_cluster(roleArn):
        pass
    # Get cluster properties and check health
    myClusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
    check_redshift, DWH_ENDPOINT = check_redshift_cluster(myClusterProps)
    set_configs("CLUSTER", "DWH_ENDPOINT", DWH_ENDPOINT)
    open_port(myClusterProps)
    conn = check_connection(DWH_ENDPOINT)
    if conn:
        print("Redshift cluster up and running.")
