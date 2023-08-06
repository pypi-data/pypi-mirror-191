from setuptools import setup, find_packages
with open('README.md') as f:
    f = open('README.md', 'r', encoding='utf-8')
    long_description = f.read()

classifiers = [
    'Programming Language :: Python :: 3'
]

setup(
    name='Italian Tweets Analyzer',
    version='2.1',
    description='Italian tweets analyzer is a tool created for the thesis work at the University of Bari \"Aldo Moro\" '
                'of the course \"Methods for the information retrieval\". It can perform analysis on Italian tweets and'
                ' it provides several features. This project is an upgraded version of the tool: Hate-Tweet-Map.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='Davide Savino Volpicella',
    author_email='s.volpicella3@studenti.uniba.it',
    license='MIT',
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=['']
)