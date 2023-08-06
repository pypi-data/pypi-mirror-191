from setuptools import setup, find_packages

setup(
    name='filter_pkg',
    version='0.1.0',
    description='This is a package created for random generating JSON, Numbers and passwords',
    author='Varun Katiyar',
    author_email='varunkatiyar819@gmail.com',
    url='https://github.com/varunkatiyar819/filter_pkg',
    packages=find_packages(),
    install_requires=[
        'random',
        'string',
        'JSON'
    ],
)
