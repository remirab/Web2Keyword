import os
import settings
from numpy import exp, mean
from datetime import datetime
from cache import LOGGER_HANDLER

class Utility:
    @staticmethod
    def time_interval(ts1: int, ts2: int)-> float:
        """ 
        Calculate time interval between two timestamps in seconds
        
        Keyword arguments:
        ts1 -- Standard Timestamp format
        ts2 -- Standard Timestamp format
            return : time interval in seconds 
        """
        timestamp1 = datetime.fromtimestamp(abs(ts1) / 1000)
        timestamp2 = datetime.fromtimestamp(abs(ts2) / 1000)
        if ts2 >= ts1:
            interval = timestamp2 - timestamp1
        else:
            interval = timestamp1 - timestamp2
        return interval.total_seconds()

    @staticmethod
    def time_interval_mean(arrival_time: int, ts: list)-> float:
        """
        Calculate mean of time intervals in seconds

        Keyword arguments:
        arrival_time -- event create Standard Timestamp
        ts -- list of enets all Standard Timestamps
            return : mean of time intervals
        """
        output = []
        if len(ts) != 0:
            for i in range(len(ts)):
                if i == 0:
                    output.append(Utility.time_interval(arrival_time, ts[i]))
                else:
                    output.append(Utility.time_interval(ts[i], ts[i - 1]))
        else:
            return 0.0
        return float(mean(output))

    @staticmethod
    def find_file(name: str, path: str)-> str:
        """
        Search for the file in folders and subfolders from 'path' point forward

        Keyword arguments:
        name -- file name
        path -- the path point that function starts searching for the file
            return : abs_path_to_file
        """
        for root, _, files in os.walk(path):
            if name in files:
                return os.path.abspath(os.path.join(root, name))

    @staticmethod
    def log(level: str, message: str):
        """
        Create logger instance object considering global settings of LOG

        Keyword arguments:
        level -- Level of logging str (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        message -- logging message as string
            return : Instantiated Logger object
        """
        if settings.LOG:
            eval(f"LOGGER_HANDLER.{level}('{message}')")
        else:
            pass
