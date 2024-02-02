import logging


def get_logger(file_name):
    prefix = ".log"
    logging.basicConfig(filename=file_name + prefix,
                        filemode='a',
                        level=logging.INFO,
                        format='%(asctime)s - %(message)s')

    return logging.getLogger(__name__)
