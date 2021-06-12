import os, json, requests, urllib
import ssl
from flask import Flask, Response, abort, request
from datetime import datetime
import time
import logging
from logging import StreamHandler
from retry import retry

# Define the base logger
logging.getLogger("analyzer").setLevel(logging.DEBUG)
log = logging.getLogger("analyzer")
stream_handler = StreamHandler()
stream_formatter = logging.Formatter('[%(asctime)s] [%(thread)d] [%(module)s : %(lineno)d] [%(levelname)s] %(message)s')
stream_handler.setFormatter(stream_formatter)
log.addHandler(stream_handler)

# Flask config
app = Flask(__name__, static_url_path='')
app.config['PROPAGATE_EXCEPTIONS'] = True

# Define global variables

global tone_analyzer_ep

global identity_token_url

global api_key

global refresh_token

global access_token

global is_refresh

global expire_time

def analyze_tone(input_text):
    log.info("tone_analyzer_ep is: %s ", tone_analyzer_ep)

    # before getting tone, check if token is expired and refresh if so.
    if datetime.utcnow() > expire_time:
        generate_tokens(is_refresh)

    if access_token:
	log.info("access token is there.")
    else:
	log.debug("access_token not existing")
	return None

    headers = {
         'Content-Type': 'text/plain',
     'Authorization': 'Bearer ' + access_token,
    }

    r = requests.post(tone_analyzer_ep, headers=headers, data=input_text)
    log.info("tone_analyzer_ep response code is: %s ", r.status_code)
    if r.status_code != 200:
        log.error("FAILED analyze tone: '%s', msg: '%s'", input_text, r.text)
        return None
    log.info("return %s ", r.json())
    return r.json()

'''
 This is the analyzer API that accepts POST data as describes below:
 POST http://localhost:5000/tone body=\
 {
     "input_text": "this is cool"
 }
'''
@app.route('/tone', methods=['POST'])
def tone():
    log.info("Serving /tone")
    if not request.json or not 'input_text' in request.json:
        log.error("bad body: '%s'", request.data)
        abort(400)

    input_text = request.json['input_text']

    log.info("input text is '%s'", input_text)
    tone_doc = analyze_tone(input_text)

    return (json.dumps(tone_doc['document_tone']['tones']), 200)


'''
POST identity/token method to generate an IAM access token by passing an API key
'''
@retry(Exception, delay=2, tries=5)
def generate_tokens(refresh):

	api_key = os.getenv('TONE_ANALYZER_API_KEY')

	params = None

	global is_refresh

	global access_token

	global refresh_token

	global expire_time

	is_refresh = refresh

	if api_key:
		log.info("api key is there.")
	else :
		log.error("TONE_ANALYZER_API_KEY not set")

	if refresh:
		headers = {
			'Authorization': 'Basic Yng6Yng=',
		}
		params = {
			'grant_type': 'refresh_token',
			'refresh_token': refresh_token,
		}

	else:
		headers = {
			'Content-Type': 'application/x-www-form-urlencoded',
			'Accept': 'application/json',
		}

		params = {
			'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
			'apikey': api_key,
		}

	params = urllib.urlencode(params)

	log.debug("calling identity token method : %s ", params)

	r = requests.post(url=identity_token_url, headers=headers, params=params)

	log.info("Identity tokens response code is: %s ", r.status_code)

	if r.status_code == 200 :

		access_token = r.json()['access_token']

		refresh_token = r.json()['refresh_token']

		token_expiration = r.json()['expiration']


		if access_token:
			log.info("Identity access token generated")

		if refresh_token:
			log.info("Identity refresh token generated")

		log.info("Identity tokens expiration: %s ", token_expiration)

		expire_time = datetime.utcfromtimestamp(float(token_expiration))
		log.info("Identity access token would expire at around: %s ", expire_time)

		log.info("current time : %s ", datetime.utcnow())

	else :

		log.error("json : %s ", r.json())


if __name__ == '__main__':

    PORT = '5000'

    api_url = os.getenv('TONE_ANALYZER_SERVICE_API')

    if not api_url:
        log.error("TONE_ANALYZER_SERVICE_API not set")

    # https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21&sentences=false
    tone_analyzer_ep = "" + api_url + "/v3/tone?version=2017-09-21&sentences=false"

    identity_token_url = "https://iam.cloud.ibm.com/identity/token"

    access_token = ""

try:
    generate_tokens(None)
except Exception as err:
	log.debug('SSL connection failed: %s', str(err))

finally :
	log.info("Starting analyzer tone_analyzer_ep: %s ", tone_analyzer_ep)
	app.run(host='0.0.0.0', port=int(PORT))
