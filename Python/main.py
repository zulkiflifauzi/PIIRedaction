import requests
from flask import Flask
from flask import request, json, jsonify
import json
app = Flask(__name__)
import spacy
from spacy_recognizer import CustomSpacyRecognizer
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
import pandas as pd
from annotated_text import annotated_text
from json import JSONEncoder
import json
import warnings
import os
from flask_cors import CORS, cross_origin
from hugchat import hugchat
from hugchat.login import Login
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings('ignore')
# from flair_recognizer import FlairRecognizer


# Helper methods
def analyzer_engine():
    """Return AnalyzerEngine."""

    spacy_recognizer = CustomSpacyRecognizer()

    configuration = {
        "nlp_engine_name": "spacy",
        "models": [
            {"lang_code": "en", "model_name": "en_spacy_pii_distilbert"}],
    }

    # Create NLP engine based on configuration
    provider = NlpEngineProvider(nlp_configuration=configuration)
    nlp_engine = provider.create_engine()

    registry = RecognizerRegistry()
    # add rule-based recognizers
    registry.load_predefined_recognizers(nlp_engine=nlp_engine)
    registry.add_recognizer(spacy_recognizer)
    # remove the nlp engine we passed, to use custom label mappings
    registry.remove_recognizer("SpacyRecognizer")

    analyzer = AnalyzerEngine(nlp_engine=nlp_engine,
                              registry=registry, supported_languages=["en"])

    # uncomment for flair-based NLP recognizer
    # flair_recognizer = FlairRecognizer()
    # registry.load_predefined_recognizers()
    # registry.add_recognizer(flair_recognizer)
    # analyzer = AnalyzerEngine(registry=registry, supported_languages=["en"])
    return analyzer

def anonymizer_engine():
    """Return AnonymizerEngine."""
    return AnonymizerEngine()


def get_supported_entities():
    """Return supported entities from the Analyzer Engine."""
    return analyzer_engine().get_supported_entities()


def analyze(**kwargs):
    """Analyze input using Analyzer engine and input arguments (kwargs)."""
    if "entities" not in kwargs or "All" in kwargs["entities"]:
        kwargs["entities"] = None
    return analyzer_engine().analyze(**kwargs)


def anonymize(text, analyze_results):
    """Anonymize identified input using Presidio Abonymizer."""
    if not text:
        return
    res = anonymizer_engine().anonymize(text, analyze_results)
    return res.text


def annotate(text, st_analyze_results, st_entities):
    tokens = []
    # sort by start index
    results = sorted(st_analyze_results, key=lambda x: x.start)
    for i, res in enumerate(results):
        if i == 0:
            tokens.append(text[:res.start])

        # append entity text and entity type
        tokens.append((text[res.start: res.end], res.entity_type))

        # if another entity coming i.e. we're not at the last results element, add text up to next entity
        if i != len(results) - 1:
            tokens.append(text[res.end:results[i+1].start])
        # if no more entities coming, add all remaining text
        else:
            tokens.append(text[res.end:])
    return tokens

class ToDictListEncoder(JSONEncoder):
    """Encode dict to json."""

    def default(self, o):
        """Encode to JSON using to_dict."""
        if o:
            return o.to_dict()
        return []
    
@app.route('/', methods=["POST"])
@cross_origin(origin='*')
def main():  
    requestData = json.loads(request.data) 
    input = requestData['Input']
    supported_entities = requestData['Entities']
    analyze_results = analyze(
		text=input,
		entities=supported_entities,
		language="en",
		score_threshold=0.35,
		return_decision_process=True,
	)
    res_dicts = [r.to_dict() for r in analyze_results]
    for d in res_dicts:
        d['Value'] = input[d['start']:d['end']]
    return json.dumps(analyze_results, cls=ToDictListEncoder)

@app.route('/chat', methods=["POST"])
@cross_origin(origin='*')
def chat():  
    requestData = json.loads(request.data) 
    input = requestData['Input']
    # Log in to huggingface and grant authorization to huggingchat
    sign = Login("zulkifli.fauzi@polyrific.com", "Polyrific*1")
    cookies = sign.login()

    # Save cookies to the local directory
    cookie_path_dir = "./cookies_snapshot"
    sign.saveCookiesToDir(cookie_path_dir)

    # Load cookies when you restart your program:
    # sign = login(email, None)
    # cookies = sign.loadCookiesFromDir(cookie_path_dir) # This will detect if the JSON file exists, return cookies if it does and raise an Exception if it's not.

    # Create a ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"
    data = {
        "result" : chatbot.chat("Hi! Could you please convert this text to be more friendly? but please keep words in brackets. here is the text: " + input)
    }
    return jsonify(data)

