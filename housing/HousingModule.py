import logging
import logging.config
import logging.handlers
from housing.conf.Config import Config


class HousingModule:

    def __init__(self):

        # define config
        self.config = Config()

        #define logger
        logging.config.dictConfig(self.config.infra_params['logger'])
        self._logger = logging.getLogger(type(self).__name__)

    # define logger property
    def _get_logger(self):
        return self._logger
    logger = property(fget=_get_logger, fset=None)

    # the two following methods are added to be able to save pickled versions of instances of a class
    # by default, pickle cannot handle classes that contain loggers as attributes
    # see : https://stackoverflow.com/questions/2999638/how-to-stop-attributes-from-being-pickled-in-python/2999833#2999833
    def __getstate__(self):
        d = dict(self.__dict__)
        if '_logger' in d:
            del d['_logger']
        return d

    def __setstate__(self, d):
        if '_logger' not in d:
            d['_logger'] = logging.getLogger(type(self).__name__)
        self.__dict__.update(d)