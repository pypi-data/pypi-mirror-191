import setuptools
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="doc_classifier",
    version="0.0.9",
    url="https://github.com/amira-codecamp/doc-classifier",
    author="amira-codecamp",
    description="A package to classify scientific documents by field of study",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=['arabic-reshaper', 'joblib', 'nltk', 'scikit-learn==1.0.2'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    include_package_data=True,
    package_data={'': ['data/*.pkl']},
)