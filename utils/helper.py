import logging

# setup logging
def setup_logging():
    logging.basicConfig(
        filename = './storage/collage-maker.log',
        format = '%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s',
        level = logging.INFO
    )
