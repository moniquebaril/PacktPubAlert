import logging


logging.basicConfig(
    filename='packt_alert.log',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s:%(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')

