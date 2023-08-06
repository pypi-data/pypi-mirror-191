from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

v = '1.0.0'

setup(
    name='paguaganetwork',
    version=v,
    description='Bayesian network',
    long_description='Library to be able to create a bayesian network',
    author='Sara Paguaga',
    author_email='sara.paguaga@gmail.com',
    classifiers=classifiers,
    keywords=['probability', 'python'],
    packages=find_packages(),
    install_requires=['']
)