#!/usr/bin/env python
# encoding: utf-8
import os
# reload(sys)
# sys.setdefaultencoding('utf-8')
import json
import boto3
import base64
from botocore.exceptions import ClientError
import base64

def get_aws_key():
	myconfig = os.environ.get("AWS_ACCESS_KEY_ID")
	return myconfig

def get_aws_region():
	myconfig = os.environ.get("AWS_REGION")
	return myconfig

def get_aws_secret():
	myconfig = os.environ.get("AWS_SECRET_ACCESS_KEY")
	return myconfig

def get_aws_secrets(secret_name="sandbox-cluster"):
	secret_name = secret_name
	AWS_ACCESS_KEY_ID = get_aws_key()
	AWS_SECRET_ACCESS_KEY = get_aws_secret()
	AWS_REGION = get_aws_region()

	# Create a Secrets Manager client
	session = boto3.session.Session()
	client = session.client(
		service_name='secretsmanager',
		region_name=AWS_REGION,
		aws_access_key_id=AWS_ACCESS_KEY_ID,
	    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
	)
	secret = ""
	# In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
	# See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
	# We rethrow the exception by default.
	
	try:
		get_secret_value_response = client.get_secret_value(
			SecretId=secret_name
		)
	except ClientError as e:
		if e.response['Error']['Code'] == 'DecryptionFailureException':
			# Secrets Manager can't decrypt the protected secret text using the provided KMS key.
			# Deal with the exception here, and/or rethrow at your discretion.
			raise e
		elif e.response['Error']['Code'] == 'InternalServiceErrorException':
			# An error occurred on the server side.
			# Deal with the exception here, and/or rethrow at your discretion.
			raise e
		elif e.response['Error']['Code'] == 'InvalidParameterException':
			# You provided an invalid value for a parameter.
			# Deal with the exception here, and/or rethrow at your discretion.
			raise e
		elif e.response['Error']['Code'] == 'InvalidRequestException':
			# You provided a parameter value that is not valid for the current state of the resource.
			# Deal with the exception here, and/or rethrow at your discretion.
			raise e
		elif e.response['Error']['Code'] == 'ResourceNotFoundException':
			# We can't find the resource that you asked for.
			# Deal with the exception here, and/or rethrow at your discretion.
			raise e
		return None
	else:
		# Decrypts secret using the associated KMS key.
		# Depending on whether the secret is a string or binary, one of these fields will be populated.
		if 'SecretString' in get_secret_value_response:
			secret = get_secret_value_response['SecretString']
		else:
			secret = base64.b64decode(get_secret_value_response['SecretBinary'])
	
	secret = json.loads(secret)
	return secret
