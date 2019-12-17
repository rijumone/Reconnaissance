import sys
import time
import subprocess
from loguru import logger

def main(seconds):
    seconds = int(seconds)
    while True:
        subprocess.check_output([
            'sudo',
            'service',
            'tor',
            'restart',
        ])
        logger.info('sleeping for {} seconds'.format(seconds))
        time.sleep(seconds)


if __name__ == '__main__':
    main(sys.argv[1])