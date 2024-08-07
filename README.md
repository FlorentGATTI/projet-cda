# Projet CDA

# Installation
- ``git clone https://github.com/FlorentGATTI/projet-cda``
- ``cd cda_project``
- ``python -m venv env``
- ``source env/bin/activate``  # Sur Windows: env\Scripts\activate
- ``pip install -r requirements.txt``

# MongoDB 
- create new database in MongoDb called: **cda**
- create new collection **prenoms**
- launch ``python scripts/load_data.py`` to import **prenoms** to database
