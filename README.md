[![Tests](https://github.com/USEPA/ckanext-collaborator_orgs/workflows/Tests/badge.svg?branch=main)](https://github.com/USEPA/ckanext-collaborator_orgs/actions)

# ckanext-collaborator_orgs

Extends collaborator functionality to user organizations, allowing organization members edit or read-only access to private datasets

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.8 and earlier | no            |
| 2.9             | yes           |


## Installation

To install ckanext-collaborator_orgs:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/USEPA/ckanext-collaborator_orgs.git
    cd ckanext-collaborator_orgs
    pip install -e .
	pip install -r requirements.txt

3. Add `collaborator_orgs` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Create necessary database tables
   
   ckan -c /etc/ckan/default/ckan.ini collaborator-orgs init-db

5. Restart CKAN


## Config settings

None at present


## Developer installation

To install ckanext-collaborator_orgs for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/USEPA/ckanext-collaborator_orgs.git
    cd ckanext-collaborator_orgs
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini

## Disclaimer
The United States Environmental Protection Agency (EPA) GitHub project code is provided on an 
"as is" basis and the user assumes responsibility for its use. EPA has relinquished control of 
the information and no longer has responsibility to protect the integrity , confidentiality, 
or availability of the information. Any reference to specific commercial products, processes, 
or services by service mark, trademark, manufacturer, or otherwise, does not constitute or 
imply their endorsement, recommendation or favoring by EPA. The EPA seal and logo shall not be 
used in any manner to imply endorsement of any commercial product or activity by EPA or the 
United States Government.
