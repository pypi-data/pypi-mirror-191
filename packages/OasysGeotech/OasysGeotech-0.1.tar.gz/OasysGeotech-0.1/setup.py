from setuptools import setup, find_packages


setup(
    name='OasysGeotech',
    version='0.1',
    license='MIT',
    author="M Johnson",
    author_email='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/mjjohnson99/oasys-geo-py',
    keywords=['OASYS','SLOPE','PDISP','ALP'],
    install_requires=[''],
)