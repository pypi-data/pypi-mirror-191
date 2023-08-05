#  =============================================================================
#  GNU Lesser General Public License (LGPL)
#
#  Copyright (c) 2022 Qujamlee from www.aztquant.com
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  =============================================================================

from atexit import register
from .qujam_spi_base import QujamSpiObject
from .qujam_logger import get_logger, _QujamLogger


class MetaQujamApi(type):
    objs = []

    def __call__(cls, *args, **kwargs):
        obj = super(MetaQujamApi, cls).__call__(*args, **kwargs)
        cls.objs.append(obj)
        return obj


@register
def __clear():
    for obj in MetaQujamApi.objs:
        if not obj.isStopped():
            obj.Stop()
            obj.Join()


class QujamApiObject(metaclass=MetaQujamApi):
    def __init__(self):
        self.__logger = None
        self.__logger_title = None
        self._spi = QujamSpiObject(None)

    def _set_heart_beat(self, *args, **kwargs):
        pass

    def _set_logger(self, logger=None, title=None):
        if not logger:
            logger = get_logger()
        assert isinstance(logger, _QujamLogger), "'logger' must be returned from 'get_logger' method"
        self.__logger = logger

        if title is not None:
            assert isinstance(title, str), "'title' must be a string"
            self.__logger_title = title
            return
        self.__logger_title = title

    def _get_logger(self):
        if not self.__logger:
            self._set_logger()
        return self.__logger

    def debug(self, *msgs):
        self._get_logger().debug(*msgs, title=self.__logger_title)

    def info(self, *msgs):
        self._get_logger().info(*msgs, title=self.__logger_title)

    def warning(self, *msgs):
        self._get_logger().warning(*msgs, title=self.__logger_title)

    def error(self, *msgs):
        self._get_logger().error(*msgs, title=self.__logger_title)

    def critical(self, *msgs):
        self._get_logger().critical(*msgs, title=self.__logger_title)

    def _stop(self):
        self._spi.clear()

    def _join(self, wait: float = None):
        pass
