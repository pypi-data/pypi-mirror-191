import os.path
import setuptools
from setuptools import setup

def read(name):
    mydir = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(mydir, name)).read()

setuptools.setup(
    name='mkdocs-conditional-include',
    version='0.0.1',
    packages=['mkdocs_conditional_include'],
    url='https://github.com/KaiReichart/mkdocs-conditional-include',
    license='Apache',
    author='Kai Reichart',
    author_email='kai@reichart.dev',
    description='A mkdocs plugin that lets you conditionally include files or trees.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=['mkdocs'],

    # The following rows are important to register your plugin.
    # The format is "(plugin name) = (plugin folder):(class name)"
    # Without them, mkdocs will not be able to recognize it.
    entry_points={
        'mkdocs.plugins': [
            'conditional_include = mkdocs_conditional_include:ConditionalInclude',
        ]
    },
)
