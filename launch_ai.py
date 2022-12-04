import argparse
import logging
import os
import sys

chatbot_dir = os.path.join(os.path.dirname(__file__), 'Chatbot_8')

sys.path.append(chatbot_dir)

from functions.core_systems import CoreInterface

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start AI')

    parser.add_argument('-p', '--portainer-run', action="store_false", dest="portainer_run",
                        help='Whether to skip running of portainer/db container on startup')

    parser.add_argument('-l', '--log-level', action="store", dest="log_level", type=str, default='INFO',
                        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'], help='Logging level')

    args = parser.parse_args()

    portainer_run = args.portainer_run
    log_level = args.log_level

    logging.basicConfig(level=log_level)

    CoreInterface.boot(portainer_boot=portainer_run)
