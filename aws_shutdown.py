
from aws_startup import DWH_CLUSTER_IDENTIFIER, DWH_IAM_ROLE_NAME, redshift, iam
from time import sleep
# ----- CODE ----

# Delete the Redshift cluster we created.
def delete_redshift():
    try:
        redshift.delete_cluster( ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,  SkipFinalClusterSnapshot=True)
        myClusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
        sleep(2)
        delete_redshift()
    except redshift.exceptions.InvalidClusterStateFault as e:
        print(e)
        sleep(2)
        print("Cluster currently deleting.")
        delete_redshift()
    except redshift.exceptions.ClusterNotFoundFault as e:
        print(e)
        print("Cluster was successfully deleted.")


# Delete the IAM role we created
def delete_iam():
    try:
        iam.detach_role_policy(RoleName=DWH_IAM_ROLE_NAME, PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
        iam.delete_role(RoleName=DWH_IAM_ROLE_NAME)
        sleep(5)
        delete_iam()
    except iam.exceptions.NoSuchEntityException as e:
        print(e)
        print("IAM role successfully deleted")


# Run all the functions if the script is called.
if __name__ == '__main__':
    try:
        delete_redshift()
    except redshift.exceptions.ClusterNotFoundFault as e:
        pass
    try:
        delete_iam()
    except iam.exceptions.NoSuchEntityException as e:
        pass
    print("All resources deleted.")
