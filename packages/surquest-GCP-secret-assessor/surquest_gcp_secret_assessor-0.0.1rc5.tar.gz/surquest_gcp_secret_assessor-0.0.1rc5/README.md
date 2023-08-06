![GitHub](https://img.shields.io/github/license/surquest/python-gcp-secrets-assessor?style=flat-square)
![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/surquest/python-gcp-secrets-assessor/test.yml?branch=main&style=flat-square)
![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/surquest/6e25c317000917840152a5e702e71963/raw/python-gcp-secrets-assessor.json&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/surquest-GCP-secret-assessor?style=flat-square)

# Introduction

This project is designed to simplify access to the secrets stored in the Secret Manager within Google Cloud Platform (GCP) during the development life cycle of Python apps.

Let's imagine you are working on a Python-based application running in Google Cloud Run as part of a team. In this case:

* Development is done locally on your machine,
* Code versioning and CI/CD pipelines are orchestrated with a Git repository such as GitHub
* The deployed application is running in Cloud Run, where the secrets are mounted as environmental variables.

The problem is that you need to have the secret available in your local environment, as well as in the environment where the application unit and integration tests are running, and finally in the Cloud Run environment.

This Python package unifies access to secrets across all the above-mentioned environments. It first looks if the secret is available as an environmental variable. If not, it tries to load it from the Secret Manager with the help of default application credentials sourced from the `GOOGLE_APPLICATION_CREDENTIALS` environmental variable.

This approach allows you to have the same codebase for all the environments and maintain carefully only the default application credentials.


# Quick start

``python
from surquest.GCP.secret_assessor import Secret

secret_value = Secret.get("my-secret-name")
``

# Local development

You are more than welcome to contribute to this project. To make your start easier we have prepared a docker image with all the necessary tools to run it as interpreter for Pycharm or to run tests.


## Build docker image
```
docker build `
     --tag surquest/gcp/secretassessor `
     --file package.base.dockerfile `
     --target test .
```

## Run tests
```
docker run --rm -it `
 -v "${pwd}:/opt/project" `
 -e "GOOGLE_APPLICATION_CREDENTIALS=/opt/project/credentials/keyfile.json" `
 -w "/opt/project/test" `
 surquest/gcp/secretassessor pytest
```