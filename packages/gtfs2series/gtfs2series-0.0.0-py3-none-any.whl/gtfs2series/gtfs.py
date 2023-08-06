import zipfile
import json
import csv
import pandas as pd
import warnings

# Required files as specified by the GTFS specification
FILES = [
    'agency', 'stops', 'routes', 'trips',
]


class TransitData:
    """A class to store GTFS data.

    This class offers methods to import GTFS data.
    """
    def summary():
        return 'Summary of the GTFS data.'

    def view():
        return 'View the GTFS data of a selected table.'
    
    def check():
        return 'Check the GTFS data for errors.'


def import_schedule(file_path):
    """Imports a GTFS .zip file and creates a GTFS object.

    The .zip file must contain the following files:

    - agency.txt
    - stops.txt
    - routes.txt
    - trips.txt

    Those files will be read and stored in a GTFS object, all others will be ignored.

    Parameters
    ----------
    file_name : string

    Returns
    -------
    gtfs_schedule : dictionary
        A dictionary where the key is the name of the file and its value is a Pandas DataFrame with its contents.

    Examples
    --------
    >>> g2s.gtfs.import_schedule('gtfs_schedule.zip')
    <gtfs2series.gtfs.GTFS object at 0x7f8b8c0b7f98>
    """
    # Unzip file
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall('gtfs_schedule')
    
    # Read files and store as Pandas DataFrames
    gtfs_schedule = {}
    for file in FILES:
        with open('gtfs_schedule/' + file + '.txt', 'r') as f:
            reader = csv.DictReader(f)
            gtfs_schedule[file] = pd.DataFrame(reader)
    
    return gtfs_schedule


def import_realtime(file_path):
    """Imports a snapshot of GTFS Realtime data.

    Parameters
    ----------
    file_name : string

    Returns
    -------
    gtfs_realtime : object
        A GTFS object with the payload data and other .

    Examples
    --------
    >>> g2s.gtfs.import_schedule('gtfs_schedule.zip')
    <gtfs2series.gtfs.GTFS object at 0x7f8b8c0b7f98>

    Raises
    ------
    ValueError
        If the file is not a .zip file.
    
    Warns
    -----
    UserWarning
        If the GTFS Schedule data has not been imported yet.
    """
    # Errors
    if not zipfile.is_zipfile(file_path):
        raise ValueError('The file is not a .zip file.')
    
    # Warnings
    if self.empty is True:
        warnings.warn('GTFS Schedule data should be imported first.')
    
    return 'Import realtime.'


def sample_data():
    """Provides sample data to test the package.

    Upon 

    Parameters
    ----------
    x : int
        This is the description.

    Returns
    -------
    GTFS : TransitData object
        An object holding GTFS Schedule and Realtime data gathered from MBTA.

    Examples
    --------
    >>> td = g2s.gtfs.sample_data()
    <gtfs2series.gtfs.TransitData object at 0x7f8b8c0b7f98>
    """
    return 'Función llegada().'


def realtime_data_collection(url, interval, timeout):
    """Collects GTFS Realtime data and stores it on a database.


    This is a process that runs in the background and updates the GTFS Realtime data

    Parameters
    ----------
    x : int
        Descripción del parámetro.
    """
    return 'Función llegada().'