import httplib2, argparse, os, sys, json
from oauth2client import tools, file, client
from googleapiclient import discovery
from googleapiclient.errors import HttpError

#Project and model configuration
project_id = '717050671184'
model_id = 'rdatarmx'

#activity labels
labels = {
	'1': 'walking', '2': 'walking upstairs', 
	'3': 'walking downstairs', '4': 'sitting', 
	'5': 'standing', '6': 'laying'
}

def main():
	""" Simple logic: train and make prediction """
	try:
		make_prediction()
	except HttpError as e: 
		if e.resp.status == 404: #model does not exist
			print("Model does not exist yet.")
			train_model()
			make_prediction()
		else: #real error
			print(e)


def make_prediction():
	api = get_prediction_api()
	
	print("Fetching model.")

	model = api.trainedmodels().get(project=project_id, id=model_id).execute()

	if model.get('trainingStatus') != 'DONE':
		print("Model is (still) training. \nPlease wait and run me again!") #no polling
		exit()

	print("Model is ready.")
	
	
	#Optionally analyze model stats (big json!)
	"""analysis = api.trainedmodels().analyze(project=project_id, id=model_id).execute()
	print(analysis)
	exit()"""
	import pprint

	#read new record from local file
	with open('record.csv') as f:
		result = [row for row in f]
	#record = f.readline().split(',') #csv

	#obtain new prediction
	for i in range(0,20):
		testdata=result[i].rstrip().split(',')
		prediction = api.trainedmodels().predict(project=project_id, id=model_id, body={
		'input': {
			'csvInstance': testdata
		       },
		}).execute()
                #retrieve classified label and reliability measures for each class
		label = prediction.get('outputLabel')
		#stats = prediction.get('outputMulti')
		#show results
		#print(' Test dataset is "%s"...prediction value is "%s"' % (testdata, label))
		print(' "%s"' % label)
		#pprint.pprint(prediction)
                
	

def train_model():
	api = get_prediction_api()

	print("Creating new Model.")

	api.trainedmodels().insert(project=project_id, body={
		'id': model_id,
		'storageDataLocation': 'machine-learning-dataset/dataset.csv',
		'modelType': 'CLASSIFICATION'
	}).execute()


def get_prediction_api():
	scope = [
		'https://www.googleapis.com/auth/prediction',
		'https://www.googleapis.com/auth/devstorage.read_only'
	]
	return get_api('prediction', scope)


def get_api(api, scope):
	""" Build API client based on oAuth2 authentication """
	STORAGE = file.Storage('oAuth2.json') #local storage of oAuth tokens
	credentials = STORAGE.get()
	if credentials is None or credentials.invalid: #check if new oAuth flow is needed
		CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
		FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS, scope=scope)
		PARSER = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, parents=[tools.argparser])
		FLAGS = PARSER.parse_args(sys.argv[1:])
		credentials = tools.run_flow(FLOW, STORAGE, FLAGS)
		
  #wrap http with credentials
	http = credentials.authorize(httplib2.Http())
	return discovery.build(api, "v1.6", http=http)


if __name__ == '__main__':
    main()
