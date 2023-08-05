from setuptools import setup

global long_description

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='zettatel',
    version='0.1.3',
    description='a python package to help send messages using the Zettatel API',
    url='https://github.com/levin-mutai/zettatel',
    author='Levin Mutai',
    author_email='levinmutai2@gmail.com',
    license='MIT licence',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['zettatel', 'messages'],
    install_requires=['build == 0.10.0',
                      'certifi ',
                      'charset-normalizer == 3.0.1',
                      'click == 8.1.3',
                      'idna == 3.4',
                      'packaging == 23.0',
                      'pip-tools == 6.12.2',
                      'pyproject_hooks == 1.0.0',
                      'python-dateutil == 2.8.2',
                      'python-dotenv == 0.21.1',
                      'requests == 2.28.2',
                      'six == 1.16.0',
                      'tomli == 2.0.1',
                      'urllib3 == 1.26.14'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
)
