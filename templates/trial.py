import json
from newfile import aws_access_key_id, aws_secret_access_key, password


print(aws_access_key_id)




def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
