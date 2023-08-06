from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='pydeequ-module',
    version='0.0.1',
    description='data assertion pydeequ module',
    long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url='',
    author='IIG',
    author_email='',
    license='MIT',
    classifiers=classifiers,
    keywords='pydeequ-data-assertion',
    packages=find_packages(),
    install_requires=['']
)