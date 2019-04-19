#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This is module of the seasounds library.

This module contains all the functions to create your own dataset for classification with Machine Learning.
All data was collected from the Watkins Marine Mammals database.
"""

import subprocess
import time
import os
from urllib import request
import requests
from bs4 import BeautifulSoup


def get_all_species():
    """Create dictionary with available Marine Mammal species in the Watkins database.

    The database can be found here https://cis.whoi.edu/science/B/whalesounds/index.cfm 

    Parameters
    ----------
    None

    Returns
    -------
    Dictionary of available species in the Watkins Marine Mammal sound Database.

    Usage
    -----
    all_mammals = get_all_species()

    """
    url = "https://cis.whoi.edu/science/B/whalesounds/index.cfm"
    try:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "html.parser")
        soup = soup.find_all(class_="large-3 columns")
        catalog = {node.text.strip(): node.a['href'].split('=')[1] for node in soup[:-1]}
        return catalog
    except ConnectionError as e:
        print(e)
        print('There was a connection problem')
        return

def get_links(species_code):
    """Make an iterable with all the downloadable audio files.

    Parameters
    ----------
    species_code: str Code from the catalog of marine species

    Returns
    -------
    Generator with all the links to the downloadable file

    """
    base_url = "https://cis.whoi.edu/science/B/whalesounds/bestOf.cfm?code="

    try:
        species_request = requests.get(base_url+species_code)
        species_soup = BeautifulSoup(species_request.text, features="html.parser")
        species_soup = species_soup.find_all("a", target="_blank")
        for element in species_soup[2:]:
            yield element['href']
    except ConnectionError as e:
        print(e)
        print("There were some troubles with the connection. Try again later")

def download_links(links, directory):
    """
    Download specific links to a given directory.

    Parameters
    ----------
    links: iter with all the links to be downloaded
    directory: str desired directory to save the audio files

    Returns
    -------
    None

    """
    download_base = " https://cis.whoi.edu"
    if os.path.isdir(directory):
        files = os.listdir(directory)
        file_number = max([int(path.split('_')[-1].split('.')[0]) for path in files])
        file_number += 1
        for index, link in enumerate(links):
            try:
                request.urlretrieve(download_base+link, f"{directory}/{directory}_{file_number + index}.wav")
                time.sleep(1)
            except ConnectionError as e:
                print(e)
                print(f"There was a problem downloading {download_base+link}")
        return
    else:
        try:  
            os.mkdir(directory)
        except OSError:  
            print (f"Creation of the directory {directory} failed")
        else:  
            print (f"Successfully created the directory {directory}")

        for index, link in enumerate(links):
            try:
                request.urlretrieve(download_base+link, f"{directory}/{directory}_{index}.wav")
                time.sleep(1)
            except ConnectionError as e:
                print(e)
                print(f"There was a problem downloading {download_base+link}")
        return

def build_dataset(categories):
    """Create dataset with the classes to be classified.

    Store the audio files in different directories in the current working directory

    Parameters
    ----------
    categories: dict of the name of the class and code in the catalog there could be more
    than one code for each class.

    Returns
    -------
    None

    """ 
    for category in categories:
        codes = categories[category] if isinstance(categories[category], list) else [categories[category]]
        for code in codes:
            code_links = get_links(code)
            download_links(code_links, category)
    return


def cut_sounds(sound_directory, time):
    """Split file into specific time intervals.

    Parameters
    ----------
    sound_directory: str  path to the directory for the audio file
    time: str duration of the splits

    Returns
    -------
    None

    """
    target_path = f'{sound_directory}/split_{time}'
    subprocess.run(f'mkdir {target_path}', shell=True)
    print(f'Creating the {target_path} folder')
    audio_files = [file for file in os.listdir(sound_directory) if not file.startswith('split_')]
    time_cmd = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "
    for element in audio_files: 
        full = f'{time_cmd}{sound_directory}/{element}'
        output = subprocess.check_output(full, shell=True) 
        if float(output) < 6:
            subprocess.run(f'cp {sound_directory}/{element} {target_path}/', shell=True) 
        else: 
            base, extension = element.split('.')
            
            split_cmd = f'ffmpeg -i {sound_directory}/{element} -f segment -segment_time 5 -c copy "{target_path}/{base}_%3d.{extension}"'
            print(split_cmd)
            subprocess.run(split_cmd, shell=True)
    return
