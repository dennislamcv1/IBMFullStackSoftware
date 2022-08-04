# sudo python3 -m pip install --upgrade --force pip
# pip3 install --upgrade ibm-watson
# pip3 install ibm-cloud-sdk-core
# pylint: disable=unused-import,line-too-long,bare-except,import-error,invalid-name,missing-final-newline

"""This is a translator module"""

import ibm_watson

from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def englishtofrench(word):
    """This class does english to french translation"""

    url_lt='https://api.us-south.language-translator.watson.cloud.ibm.com/instances/dfb4e059-a2b5-470b-9ac4-f4628099cf0a'
    apikey_lt='5W4TiN2vz1utmA3YgN0-m9qv7TgzznYioDwTXPc4g_-7'
    version_lt='2018-05-01'
    authenticator = IAMAuthenticator(apikey_lt)
    language_translator = LanguageTranslatorV3(version=version_lt,authenticator=authenticator)
    language_translator.set_service_url(url_lt)
    lt = language_translator
    translation = lt.translate(text=word, model_id="en-fr").get_result()
    
    if word == " ":
        print("Please enter a word")
    else:
        pass

    return translation['translations'][0]['translation']

def englishtogerman(word):
    """This class does english to german translation"""

    url_lt='https://api.us-south.language-translator.watson.cloud.ibm.com/instances/dfb4e059-a2b5-470b-9ac4-f4628099cf0a'
    apikey_lt='5W4TiN2vz1utmA3YgN0-m9qv7TgzznYioDwTXPc4g_-7'
    version_lt='2018-05-01'
    authenticator = IAMAuthenticator(apikey_lt)
    language_translator = LanguageTranslatorV3(version=version_lt,authenticator=authenticator)
    language_translator.set_service_url(url_lt)
    lt = language_translator
    translation = lt.translate(text=word, model_id="en-de").get_result()
    return translation['translations'][0]['translation']