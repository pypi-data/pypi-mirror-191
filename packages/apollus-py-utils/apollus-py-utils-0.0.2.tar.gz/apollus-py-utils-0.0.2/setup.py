from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='apollus-py-utils',
    version='0.0.2',
    license='MIT License',
    author='Fabiel Prestes',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='fabiel.prestes@apollusehs.com.br',
    keywords='apollus',
    description=u'Funcoes Utils',
    packages=['database'],
    install_requires=['boto3', 'psycopg2-binary'],)