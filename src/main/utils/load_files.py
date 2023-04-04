import json
from logger.app_logging import getlogger
import pandas as pd

logger = getlogger(__name__)

##################################################


def loadfile(filename):
    file_obj = None
    json_file = None

    if filename is None:
        return None

    filename_comps = filename.split('.')
    ext = filename_comps[len(filename_comps) - 1].lower()
    if (ext != 'json' and ext != 'csv'):
        logger.error("Error: only '.json' and '.csv' files allowed")
        return None

    try:
        logger.debug("filename = " + filename + ", ext = " + ext)
        if (ext == 'csv'):
            # file_obj is a Pandas dataframe
            logger.debug("Reading CSV file")
            file_obj = pd.read_csv(filename, encoding="utf-8")
        else:
            # JSON
            json_file = open(filename, "r")
            # fileObj is a JSON object in the Python json package
            file_obj = json.load(json_file)
    except FileNotFoundError as e:
        logger.error("FileNotFoundError: %s", str(e))
        raise
    except UnicodeDecodeError as e:
        logger.error("UnicodeDecodeError: %s", str(e))
        raise
    except ValueError as e:
        logger.error("ValueError: %s", str(e))
        raise
    except IOError as e:
        logger.error("IOError: %s", str(e))
        raise
    except:
        logger.exception("Unexpected error in loadFile")
        raise
    finally:
        if bool(json_file):
            json_file.close()

        return file_obj
