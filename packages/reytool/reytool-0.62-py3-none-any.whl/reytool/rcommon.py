# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-08 13:11:09
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's common methods
"""


from typing import List, Tuple, Literal, Optional, Union
import os
import time
import random
from traceback import format_exc

from .rbasic import error
from .rtext import rprint


def exc(title: str = "Error", to_print: bool = True) -> str:
    """
    Print and return error messages, must used in 'except' syntax.

    Parameters
    ----------
    title : Print title.
    to_print : Whether print error messages.

    Returns
    -------
    Error messages.
    """

    error = format_exc()
    error = error.strip()
    if to_print:
        rprint(error, title=title, frame="half")
    return error

def digits(number: Union[int, float]) -> Tuple:
    """
    Judge the number of integer digits and deciaml digits.

    Parameters
    ----------
    number : Judge number.

    Returns
    -------
    Integer digits and deciaml digits.
    """

    number_str = str(number)
    if "." in number_str:
        integer_str, decimal_str = number_str.split(".")
        integer_digits = len(integer_str)
        deciaml_digits = len(decimal_str)
    else:
        integer_digits = len(number_str)
        deciaml_digits = 0
    return integer_digits, deciaml_digits

def randn(*thresholds: Union[int, float], precision: Optional[int] = None) -> Union[int, float]:
    """
    Get random number.

    Parameters
    ----------
    thresholds : Low and high thresholds of random range, range contains thresholds.
        - When length is 0, then low and high thresholds is 0 and 10.
        - When length is 1, then low and high thresholds is 0 and thresholds[0].
        - When length is 2, then low and high thresholds is thresholds[0] and thresholds[1].

    precision : Precision of random range, that is maximum decimal digits of return value.
        - None : Set to Maximum decimal digits of element of parameter *thresholds.
        - int : Set to this value.
    
    Returns
    -------
    Random number.
        - When parameters precision is 0, then return int.
        - When parameters precision is greater than 0, then return float.
    """
    
    thresholds_len = len(thresholds)
    if thresholds_len == 0:
        threshold_low = 0
        threshold_high = 10
    elif thresholds_len == 1:
        threshold_low = 0
        threshold_high = thresholds[0]
    elif thresholds_len == 2:
        threshold_low = thresholds[0]
        threshold_high = thresholds[1]
    else:
        error("number of parameter '*thresholds' must is 0 or 1 or 2", ValueError)
    if precision == None:
        threshold_low_desimal_digits = digits(threshold_low)[1]
        threshold_high_desimal_digits = digits(threshold_high)[1]
        desimal_digits_max = max(threshold_low_desimal_digits, threshold_high_desimal_digits)
        precision = desimal_digits_max
    magnifier = 10 ** precision
    threshold_low *= magnifier
    threshold_high *= magnifier
    number = random.randint(threshold_low, threshold_high)
    number = number / magnifier
    if precision == 0:
        number = int(number)
    return number

def sleep(*thresholds: Union[int, float], precision: Optional[int] = None) -> Union[int, float]:
    """
    Sleep random seconds.

    Parameters
    ----------
    thresholds : Low and high thresholds of random range, range contains thresholds.
        - When length is 0, then low and high thresholds is 0 and 10.
        - When length is 1, then sleep this value.
        - When length is 2, then low and high thresholds is thresholds[0] and thresholds[1].
    
    precision : Precision of random range, that is maximum decimal digits of sleep seconds.
        - None : Set to Maximum decimal digits of element of parameter *thresholds.
        - int : Set to this value.
    
    Returns
    -------
    Random seconds.
        - When parameters precision is 0, then return int.
        - When parameters precision is greater than 0, then return float.
    """

    thresholds_len = len(thresholds)
    if thresholds_len == 0:
        second = randn(0, 10, precision=precision)
    elif thresholds_len == 1:
        second = thresholds[0]
    elif thresholds_len == 2:
        second = randn(thresholds[0], thresholds[1], precision=precision)
    else:
        error("number of parameter '*thresholds' must is 0 or 1 or 2", ValueError)
    time.sleep(second)
    return second

def get_paths(path: Optional[str] = None, target: Literal["all", "file", "folder"] = "all", recursion: bool = True) -> List:
    """
    Get the path of files and folders in the path.

    Parameters
    ----------
    path : When None, then work path.
    target : Target data.
        - "all" : Return file and folder path.
        - "file : Return file path.
        - "folder" : Return folder path.

    recursion : Is recursion directory.

    Returns
    -------
    String is path.
    """

    if path == None:
        path = ""
    path = os.path.abspath(path)
    paths = []
    if recursion:
        obj_walk = os.walk(path)
        if target == "all":
            targets_path = [
                os.path.join(path, file_name)
                for path, folders_name, files_name in obj_walk
                for file_name in files_name + folders_name
            ]
            paths.extend(targets_path)
        elif target == "file":
            targets_path = [
                os.path.join(path, file_name)
                for path, folders_name, files_name in obj_walk
                for file_name in files_name
            ]
            paths.extend(targets_path)
        elif target in ["all", "folder"]:
            targets_path = [
                os.path.join(path, folder_name)
                for path, folders_name, files_name in obj_walk
                for folder_name in folders_name
            ]
            paths.extend(targets_path)
    else:
        names = os.listdir(path)
        if target == "all":
            for name in names:
                target_path = os.path.join(path, name)
                paths.append(target_path)
        elif target == "file":
            for name in names:
                target_path = os.path.join(path, name)
                is_file = os.path.isfile(target_path)
                if is_file:
                    paths.append(target_path)
        elif target == "folder":
            for name in names:
                target_path = os.path.join(path, name)
                is_dir = os.path.isdir(target_path)
                if is_dir:
                    paths.append(target_path)
    return paths