# Translate a book with Google Cloud Translate API 
## Overview:

This script takes a text file input and by a specified delimiter (ex: ‘.’ and ‘\n’), sends the text to Google Cloud Translate API, stores translated text in memory and after the text file has been completed assembles the translated text file into an output file.

[Tqdm](https://pypi.python.org/pypi/tqdm) is being used to display progress of the translation job.

Before attempting this aware of the following:
5000 characters per request limit for the Translate API
Service quotas per user/day for Translate API within Google Cloud Platform quotas.

## Requirements:

- Python3
- Google cloud pip package
- Google Cloud Platform [Service Account](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) key in json

## Configure your environment:

Download [service account credentials][service-account], rename .json file to creds.json in same folder as translate-book.py.
[service-account]: (https://console.cloud.google.com/apis/credentials?project=_)

'sudo python -m pip install google-cloud --ignore-installed'


## To run:
`python3 translate-client.py input.txt outout.txt`

`$ python3 translate-client.py book.txt book-translated-2.txt
Input Text Loop: |####------| 415/1029  40% [elapsed: 08:09 left: 12:04,  0.85 iters/sec]`

