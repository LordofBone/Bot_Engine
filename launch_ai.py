import argparse
import logging

from functions.core_systems import CoreInterface

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start AI')

    parser.add_argument('-l', '--log-level', action="store", dest="log_level", type=str, default='INFO',
                        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'], help='Logging level')

    args = parser.parse_args()

    log_level = args.log_level

    logging.basicConfig(level=log_level)

    CoreInterface.boot()
