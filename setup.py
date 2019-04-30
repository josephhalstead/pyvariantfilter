import setuptools

with open('readme.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyvariantfilter',
    version='0.0.1',
    author='Joseph Halstead',
    author_email='josephhalstead89@gmail.com',
    description='Python package for filtering variants.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/josephhalstead/pyvariantfilter',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
   'pysam>=0.15.2',
   'pandas>=0.23.4'
],
)