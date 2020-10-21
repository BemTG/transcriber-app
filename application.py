from flask import Flask, render_template, request
import boto3
from werkzeug.utils import secure_filename
import time as time
from cryptography.fernet import Fernet
import os 
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import key

crypter= Fernet(key.key)

acc_keyid=b'gAAAAABfj2y2SbMoxazBxPZqke59GQCbjkCjLUoxWX3yFbGkCOlTAZfTcThH-qmUA3WPa7_jPGUaHUQvwPIwA28LBa9Y4KugMjrVNtPwWwPldPy-6fAUuUM='
sec_keyid=b'gAAAAABfj21W1V35AOcVTP9QBBw5IDLS67OKZ1d-yyx4sj_6XGevY49wc3ew9t7MzxjxUjO9PemZ5uVE8U6hnj-0TFcpLL-fJM-8ch1VlkuyRkaSt9i03aTUFQa8-ZlBFq3G3t0zvCxV'



aws_access_key_id= crypter.decrypt(acc_keyid)
aws_access_key_id=aws_access_key_id.decode("utf-8")

aws_secret_access_key= crypter.decrypt(sec_keyid)
aws_secret_access_key=aws_secret_access_key.decode("utf-8")





application= app = Flask(__name__)





# aws_access_key_id='12323'
# aws_secret_access_key= ''


s3 = boto3.resource('s3',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key= aws_secret_access_key,
                    # aws_session_token=keys.AWS_SESSION_TOKEN
                     )

dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name='us-east-1')





# BUCKET_NAME='transcriberbucket1'
BUCKET_NAME='transcriberbucket1'

@app.route('/')  
def home():

    return render_template("file_upload_to_s3.html")

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        mp3 = request.files['file']
        email=request.form['email']
        # time=time.ctime()

# #         # USED FOR CREATING THE TABLE INITIALLY
#         table = dynamodb.create_table(
#     TableName='newtable',
#     KeySchema=[
#         {
#             'AttributeName': 'email',
#             'KeyType': 'HASH'
#         }
         
#     ],
#     AttributeDefinitions=[
#              {
#             'AttributeName': 'time',
#             'AttributeType': 'S',

#             'AttributeName': 'time-number',
#             'AttributeType': 'S',

#             'AttributeName': 'email',
#             'AttributeType': 'S',

#         } 
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 1,
#         'WriteCapacityUnits': 1,
#     }

# )
        table = dynamodb.Table('newtable')
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName='newtable')

        # IPopulating the table created with users input
        table = dynamodb.Table('newtable')
        
        table.put_item(
                Item={
        
        'email': email,
        'date': time.ctime(),
        'time-number': str(time.time()),
        
            }
        )



        # msg2 = "Transcription should "


        if mp3:

                filename = secure_filename(mp3.filename)
                mp3.save(filename)
                s3.meta.client.upload_file(filename, BUCKET_NAME, 'audioFile/%s' % (filename))
                # s3.upload_file(
                #     Bucket = BUCKET_NAME,
                #     Filename=filename,
                #     Key = filename
                # )
                msg= 'Upload Done! Your file is being proccessed and will be emailed to you shortly'


    return render_template("file_upload_to_s3.html",msg =msg)





if __name__ == "__main__":
    
    app.run(debug=True)
