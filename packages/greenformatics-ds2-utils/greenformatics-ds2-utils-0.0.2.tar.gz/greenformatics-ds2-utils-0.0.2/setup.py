from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'This is a utility package to support data scraping from different data sources.'
LONG_DESCRIPTION = 'This is a utility package to support data scraping from different data sources like REST' \
                   'and SOAP APIs, Google Sheets, online CSV files, databases including SQL, NoSQL and LDAP etc.' \
                   'The goal of this package to get all the necessary utilities together, maintain them in a single' \
                   'code base and make the available for all the data scraping project from PyPi hence it is' \
                   'upgradeable in a particular data scraper program.'

setup(
    name="greenformatics-ds2-utils",
    version=VERSION,
    author="Adam Fónagy",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=['psycopg2~=2.9.5', 'mock~=4.0.3', 'sqlalchemy~=1.4.42', 'requests~=2.28.1',
                      'google-api-python-client~=2.76.0', 'google-auth-httplib2~=0.1.0'],
    keywords=['python', 'data scraping', 'utilities', 'util', 'utility'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ]
)