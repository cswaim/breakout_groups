import logging

class SkipInfocon(logging.Filter):
    """ filter to not log infocon messages"""
    def filter(self, record):
        return not record.levelname == "INFOCON"