from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='djnfusion',
    version='0.1',
    description='A lightweight component to integrate InfusionSoft CRM with Django. This package is in no way affiliated with, or related to, InfusionSoft.',
    long_description=readme(),
    classifiers=[ # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    url='http://github.com/gnowsis/djnfusion',
    author='Bernhard Schandl',
    author_email='bernhard.schandl@gmail.com',
    license='MIT',
    packages=['djnfusion'],
    install_requires=[
        'django',
    ],
    extras_require = {
        'background_tasks': ['celery'],
    },
    zip_safe=False,
)