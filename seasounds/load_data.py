#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Module for loading sound files.

Author: Erika Peláez
MIT license

This module contains all the functions to load files whether all together or by batches.
"""

import os
import librosa


def batch_loader(files_path, time_limit, batch_size=100):
    """Create generator from files.

    Returns a generator to iterate over the entire data set without having to overload RAM

    Parameters
    ----------
    files_path: str Path to the folder where the files are stored
    batch_size: int Number of samples per batch
    time_limit:

    Returns
    -------
    Generator of with the files divided by n batches of batch_size size

    """
    file_list = os.listdir(files_path)
    sampling_rate = []
    sounds = []
    for number in range(len(file_list)//batch_size):
        lower_index = number * batch_size
        upper_index = (number + 1) * batch_size
        for audio_file in file_list[lower_index:upper_index]:
            sound, sampling = librosa.load(f'{files_path}/{audio_file}', duration=time_limit)
            sounds.append(sound)
            sampling.append(sound)
        yield sampling_rate, sounds



def load_sound_files(files_path, time_limit):
    """Load files to memory.

    Parameters
    ----------
    files_path: str Path to the audio files to load
    time_limit: float Number of seconds to load from the file

    Returns
    -------
    tuple with list of sampling rates and list of sound signals.
    
    """
    file_list = os.listdir(files_path)
    sampling_rate = []
    sounds = []
    for audio_file in file_list:
        sound, sampling = librosa.load(f'{files_path}/{audio_file}', duration=time_limit)
        sounds.append(sound)
        sampling.append(sound)
    return sampling_rate, sounds