_VERSION="1.0"

from setuptools import setup
setup(name = 'ChromaClade', 
    version = _VERSION, 
    description = "A GUI and CLI app for producing phylogenetic tree files coloured by observed molecular sequence states",
    author = 'Christopher Monit', 
    author_email = 'c.monit.12@ucl.ac.uk', 
    url = 'https://github.com/chrismonit/chroma_clade',
    #download_url = 'https://github.com/sjspielman/pyvolve/tarball/' + _VERSION,
    #platforms = 'Tested on Mac OS X.',
    package_dir = {'chroma_clade':'src'},
    packages = ['chroma_clade'],
    #package_data = {'tests': ['freqFiles/*', 'evolFiles/*']},
    package_data = {'chroma_clade': ['dat/*', 'pic/*']},
    install_requires=['biopython'], # Tkinter?
    #test_suite = "tests"
    long_description=open("README.txt").read()
)
