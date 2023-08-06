from setuptools import find_packages, setup

VERSION = '0.0.0'
DESCRIPTION = 'Transform GTFS Realtime data into multivariate time series.'
LONG_DESCRIPTION = 'Transform GTFS Realtime data into multivariate time series, filtering by selected parameters and adding as many time-indexed variables as needed.'

setup(
    name='gtfs2series',
    packages=find_packages(include=['gtfs2series']),
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Fabián Abarca',
    license='MIT',
    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'requests',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
    ],
)
