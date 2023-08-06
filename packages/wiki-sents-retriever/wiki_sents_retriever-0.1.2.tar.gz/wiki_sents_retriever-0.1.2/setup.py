from setuptools import setup

setup(
    name='wiki_sents_retriever',
    version='0.1.2',
    description='Query English Wikipedia',
    author='Christoph Schuhmann',
    url='https://huggingface.co/datasets/ChristophSchuhmann/wikipedia-3sentence-level-retrieval-index',
    license='BSD 2-clause',
    packages=['wiki_sents_retriever'],
    install_requires=[
        'transformers',
        'faiss-cpu',
        'numpy',
        'pandas',
        'torch'
    ]
)
