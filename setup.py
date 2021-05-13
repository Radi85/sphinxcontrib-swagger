import os

from setuptools import setup, find_packages


DIR = os.path.dirname(__file__)


def get_version():
    with open(os.path.join(DIR, 'VERSION')) as version_file:
        version = version_file.read().strip()
    return version


with open(os.path.join(DIR, 'README.rst'), 'r', encoding='utf-8') as f:
    readme = f.read()


setup(
    name='sphinxcontrib-swagger',
    version=get_version(),
    description='Create Swagger documentation from openapi and embed it into exiting document.',
    long_description=readme,
    license='MIT',
    url='https://github.com/radi85/sphinx-swagger',
    keywords='sphinx openapi swagger rest api docs',
    author=u'Radico',
    project_urls={
        'Documentation': 'https://sphinx-swagger.readthedocs.io/index.html',
        'Source Code': 'https://github.com/radi85/sphinx-swagger',
    },
    packages=find_packages(exclude=['docs', 'test*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'sphinx>=1.5',
        'jinja2==2.11.3',
        'jsonschema==3.2.0',
        'PyYAML==5.4.1',
    ],
    classifiers=[
        'Topic :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
