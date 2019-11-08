import json
import logging 
import pickle
from urllib.parse import urlparse
import os 
import io
import boto3
import numpy as np

""" --- Static initialization--- 
We will download the user embeddings file on lambda initialization
 as we need this later as input for the SageMaker endpoint
"""
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

embeddings = None
if 'SAGEMAKER_ENDPOINT_NAME' in os.environ:
  endpoint_name = os.environ['SAGEMAKER_ENDPOINT_NAME']

# Load user embeddings from S3, which we will need to call sagemaker endpoint later
if 'EMBEDDINGS_S3_PATH' in os.environ: 
    logger.debug('Downloading embeddings from path:' + os.environ['EMBEDDINGS_S3_PATH'])
    parsed_url = urlparse(os.environ['EMBEDDINGS_S3_PATH'], allow_fragments=False)
    embeddings_bucket = parsed_url.netloc
    embeddings_path = parsed_url.path.lstrip('/') # the bucket which contains static assets

    logger.debug(
    'Downloading user embeddings  from url=s3://{}/{}'.format(embeddings_bucket,embeddings_path))
    s3 = boto3.client('s3')
    s3.download_file(embeddings_bucket, embeddings_path, '/tmp/embeddings.pickle')

    #load embeddings as numpy array
    with open('/tmp/embeddings.pickle', 'rb') as embeddings_file:
      embeddings = pickle.load(embeddings_file)
    logger.debug( 'Successfully loaded user embeddings')
else:
  raise Exception('missing path to embeddings')

def handler(event, context):
    """
    Main lambda handler function, extracts the user_id from the request, 
    invokes the Sagemaker endpoint and returns the result in the required format
    """
    # first lets get the requested user id else return error 400
    if event['queryStringParameters'] != None and 'user_id' in event['queryStringParameters']:
        user_id = int(event['queryStringParameters']['user_id'])
    else:
        logger.debug('Returning error 400 , missing user_id query string param')
        return {
            "statusCode": 400,
            "body": "Missing user_id queryString param"
        }
    
    # invoke sagemaker endpoint
    result = invoke_endpoint(user_id)
    body = {
       "itemList": result
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    logger.debug("Returning response: {}".format(response))
    return response

def invoke_endpoint(user_id):
  """
  Invokes the sagemaker endpoint using standard boto3 AWS Python SDK
  """
  sagemaker = boto3.client('sagemaker-runtime')
  response = sagemaker.invoke_endpoint(
    EndpointName=endpoint_name,
    Body=_getEmbeddingsForUserAsCSV(user_id),
    ContentType='text/csv',
    Accept='application/jsonlines; verbose=true'
  )
  response = json.loads(response['Body'].read().decode())
  itemList = []
  for item in response['labels']:
    itemList.append({'itemId' : str(int(item)) })
  return itemList

def _getEmbeddingsForUserAsCSV(user_id):
    """
    use the embeddings matrix we have in memory to extract the vector representation for the user required by the sagemaker endpoint
    """
    user= embeddings[user_id-1][:]
    user.shape=(1,user.shape[0])
    buf = io.StringIO()
    np.savetxt(buf, user, delimiter=',')
    return buf.getvalue()
