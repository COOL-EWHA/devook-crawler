# -*- coding: utf-8 -*-
import json
import os.path

from azure.ai.textanalytics                     import TextAnalyticsClient
from azure.core.credentials                     import AzureKeyCredential

from key_phrase_with_crawler.get_test_document  import get_test_document

endpoint    = "https://koreacentral.api.cognitive.microsoft.com/"
secret_file = os.path.join('.', 'secrets.json')
with open(secret_file) as f:
    secrets = json.loads(f.read())


# Authenticate the client using your key and endpoint
def authenticate_client():
    ta_credential           = AzureKeyCredential(secrets["azure_secret_key"])
    text_analytics_client   = TextAnalyticsClient(
        endpoint    = endpoint,
        credential  = ta_credential)
    return text_analytics_client


client = authenticate_client()


# Test key phrase extraction with crawler
def key_phrase_extraction_example(client):
    try:
        documents   = get_test_document()
        response    = client.extract_key_phrases(documents=documents, language="ko")

        for data in response:
            print(data)

    except Exception as err:
        print("Encountered exception. {}".format(err))


key_phrase_extraction_example(client)
