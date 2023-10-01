# PIIRedaction
There are two apps that need to be run, python application hosted on Flask API Server and the client side application using Blazor PWA:
## 1. Flask Web API
This will host Python scripts for redact user input and send it to the hugging face chat API
### Prerequisites
1. Python 3.x
2. pip
### Required library installation
Install the following model and libraries:
#### Huggingface model: en_spacy_pii_distilbert
```
pip install https://huggingface.co/beki/en_spacy_pii_distilbert/resolve/main/en_spacy_pii_distilbert-any-py3-none-any.whl
```
#### Flask API Server
```
pip install flask
```

#### Presidio Analyzer
```
pip install presidio_analyzer
```

#### Presidio Anonymizer
```
pip install presidio_anonymizer
```

#### Pandas
```
pip install pandas
```

#### Hugchat
```
pip install hugchat
```
To run the Flask API server, go to the main folder/Python and then run the below command
```
flask --app main.py  run -p 7000
```
the API server will be listening on port 7000

## 2. Client side application
to run the client-side application, go to the main/Net/AILearning folder and then run the below command'
```
dotnet watch run ailearning
```
# Classifier
## 1. Flask Web API
This will host Python scripts for processing input file, train and test given sentence

### Prerequisites
1. Python 3.x
2. pip
### Required library installation
Install the following model and libraries:

#### Flask API Server
```
pip install flask
```
#### Pandas
```
pip install pandas
```
#### Sklearn
```
pip install sklearn
```
#### Skmultilearn
```
pip install skmultilearn
```
#### Neattext
```
pip install neattext
```
#### Pickle
```
pip install pickle
```

To run the Flask API server, go to the main folder/Python and then run the below command
```
flask --app main.py  run -p 7001
```
the API server will be listening on port 7000

## 2. Client side application
to run the client-side application, go to the main/Net/AILearning folder and then run the below command'
```
dotnet watch run ailearning
```

