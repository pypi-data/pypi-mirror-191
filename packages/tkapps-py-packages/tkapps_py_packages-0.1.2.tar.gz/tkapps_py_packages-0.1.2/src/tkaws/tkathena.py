import os
import boto3

class Tkathena():
    def __init__(self, region=None):
        """
        :param region: The region for AWS Athena
        """
        self.service_name = 'athena'
        if region is None:
            region = os.getenv("DYNAMODB_REGION")
        if region is None:
            region = os.getenv("REGION")
        if region is None:
            raise ValueError("REGION is missing in both ENV Variable and constructor params.")
        self.region = region
        self.env = os.getenv("ENV")
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.http_timeout = 60

    def get_client(self):
        """
        To be used internally for the purpose of creating the boto3 client of athena.
        This method creates the boto3 client for AWS, The client can later be accessed using 'self.client'
        :return: Self object
        """
        if self.access_key is None or self.secret_key is None:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region)
        else:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region,
                                       aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def get_resource(self):
        """
        To be used internally for the purpose of creating the boto3 resource of athena.
        This method creates the boto3 resource for AWS, The resource can later be accessed using 'self.resource'
        :return: Self object
        """
        if self.access_key is None or self.secret_key is None:
            self.resource = boto3.resource(service_name=self.service_name, region_name=self.region)
        else:
            self.resource = boto3.resource(service_name=self.service_name, region_name=self.region,
                                           aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def run_query(self, database, query):
        output_location = os.getenv("ATHENA_OUTPUT_S3_PATH")
        self.get_client()
        response = self.client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': database
            },
            ResultConfiguration={
                'OutputLocation': output_location
            }
        )
        print("response :", response)
        return response['QueryExecutionId']

    def get_query_status_details(self, execution_id):
        self.get_client()
        response = self.client.get_query_execution(
            QueryExecutionId=execution_id
        )
        return response['QueryExecution']

    def get_output_s3_path(self, file_name):
        output_location = os.getenv("ATHENA_OUTPUT_S3_PATH")
        return str(output_location).strip('/') + '/' + file_name

    def get_athena_db_name(self, tenant_name, athena_env):
        if athena_env.startswith("prod"):
            db_name = "tdp_{}_models".format(tenant_name)
        else:
            db_name = "{}_tdp_{}_models".format(athena_env, tenant_name)
        return db_name

    # Get DB name for processed layer tables
    def get_athena_processed_db_name(self, tenant_name, athena_env):
        if athena_env.startswith("prod"):
            db_name = "tdp_{}_processed".format(tenant_name)
        else:
            db_name = "{}_tdp_{}_processed".format(athena_env, tenant_name)
        return db_name

    def run_query_with_path(self, output_location, database, query):
        self.get_client()
        response = self.client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': database
            },
            ResultConfiguration={
                'OutputLocation': output_location
            }
        )
        return response['QueryExecutionId']

    def get_output_location(self, output_path, database, query, report_name):
        try:
            execution_id = self.get_query_state(output_path, database, query)
            if execution_id:
                output_loc = output_path + "/" + str(execution_id) + ".csv"
                final_path = output_path + "/" + str(report_name) + '.csv'
                output_key = output_loc.split("//")[1]
                final_key = final_path.split("//")[1]
                s3_support.rename_s3_object(output_key, final_key)
                return True
        except Exception as err:
            print(err)

    def get_query_state(self, output_path, database, query):
        max_execution = 30
        self.get_client()
        execution_id = self.run_query_with_path(output_path, database, query)
        state = 'RUNNING'
        while max_execution > 0 and state in ['RUNNING', 'QUEUED']:
            max_execution = max_execution - 1
            response = self.client.get_query_execution(QueryExecutionId=execution_id)
            if 'QueryExecution' in response and \
                    'Status' in response['QueryExecution'] and \
                    'State' in response['QueryExecution']['Status']:
                state = response['QueryExecution']['Status']['State']
                print(response['QueryExecution']['Status'])
                if state == 'FAILED':
                    return False
                elif state == 'SUCCEEDED':
                    return execution_id
        return False






