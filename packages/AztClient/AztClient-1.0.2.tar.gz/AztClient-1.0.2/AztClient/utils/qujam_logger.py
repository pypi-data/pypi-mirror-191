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
import enum
import logging as _logging
import time as _time
import sys as _sys
import colorlog as _colorlog
import atexit as _atexit

NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL = (
    _logging.NOTSET, _logging.DEBUG, _logging.INFO, _logging.WARNING, _logging.ERROR, _logging.CRITICAL
)

NOMICROSECOND, MICROSECOND, MILLSECOND = range(3)


class FileMode(enum.Enum):
    AppendNew = 'a'
    AppendBinaryNew = 'ab'
    AppendReadWriteNew = 'a+'
    AppendReadWriteBinaryNew = 'ab+'
    Text = 't'
    Binary = 'b'
    GeneralLine = 'U'
    ReadWrite = '+'
    ReadOnly = 'r'
    ReadOnlyBinary = 'rb'
    ReadWriteHead = 'r+'
    ReadWriteHeadBinary = 'rb+'
    WriteOnly = 'x'
    WriteOnlyNew = 'w'
    WriteOnlyBinaryNew = 'wb'
    WriteReadNew = 'w+'
    WriteReadBinaryNew = 'wb+'


class RootLoggerDisableError(Exception):
    pass


_root_logger_attr = "_qujam_root_logger"
_root_logger_name = "_qujam_root_logger_name"
_root_logger_enable = "_qujam_root_logger_enable"

_farewell_text_attr = "_qujam_farewell_text"

LEVEL_NAME_CN, LEVEL_NAME_EN = range(2)
_level_names_cn = {
    NOTSET: "缺省",
    DEBUG: "测试",
    INFO: "日志",
    WARNING: "警告",
    ERROR: "错误",
    CRITICAL: "致命",
}

_level_names_en = {
    NOTSET: 'NONE',
    DEBUG: 'DBUG',
    INFO: 'INFO',
    WARNING: 'WARN',
    ERROR: 'ERRO',
    CRITICAL: 'CRTI',
}


class _NormalFormatter(_logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, msecfmt='%s.%03d', style='%', validate=True):
        super(_NormalFormatter, self).__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate)
        self._msec_fmt = msecfmt

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = _time.strftime(datefmt, ct)
        else:
            s = _time.strftime(self.default_time_format, ct)
            if self._msec_fmt:
                s = self._msec_fmt % (s, record.msecs)
        return s


class _ColorFormatter(_colorlog.ColoredFormatter):

    def __init__(self, fmt=None, datefmt=None, msecfmt='%s.%03d', style="%", log_colors=None, reset=True,
                 secondary_log_colors=None,
                 validate=True, stream=None, no_color=False, force_color=False, defaults=None):
        super(_ColorFormatter, self).__init__(
            fmt=fmt,
            datefmt=datefmt,
            style=style,
            log_colors=log_colors,
            reset=reset,
            secondary_log_colors=secondary_log_colors,
            validate=validate,
            stream=stream,
            no_color=no_color,
            force_color=force_color,
            defaults=defaults,
        )
        self._msec_fmt = msecfmt

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = _time.strftime(datefmt, ct)
        else:
            s = _time.strftime(self.default_time_format, ct)
            if self._msec_fmt:
                s = self._msec_fmt % (s, record.msecs)
        return s


class _MetaQujamLogger(type):
    _loggers = dict()

    def __call__(cls, *args, **kwargs):
        logger_name = kwargs.get("name", None)
        if kwargs.pop("new", False) or logger_name not in cls._loggers:
            cls._loggers[logger_name] = super(_MetaQujamLogger, cls).__call__(*args, **kwargs)
        return cls._loggers[logger_name]


def _get_msec_fmt(msec):
    if msec == MILLSECOND:
        return "%s.%03d"
    elif msec == MICROSECOND:
        return "%s.%06d"
    return None


class _QujamLogger(metaclass=_MetaQujamLogger):
    _default_log_colors = {
        'DEBUG': 'green',
        'INFO': 'white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    def __init__(self, *, name=None, filename=None, filemode=None, level=INFO, level_name=LEVEL_NAME_CN,
                 fmt=None, datefmt=None, msec=MILLSECOND, log_colors=None, hint_left='[', hint_right=']',
                 hint_separator=' '):
        if filename:
            assert isinstance(filename, str), "'filename' must be of type str"
            if not isinstance(filemode, (FileMode, str)):
                filemode = FileMode.AppendNew
            if type(filemode) == FileMode:
                filemode = filemode.value
            _hdr = _logging.FileHandler(filename, encoding="utf-8", mode=filemode)
        else:
            _hdr = _logging.StreamHandler()

        if level_name == LEVEL_NAME_EN:
            self._level_names = _level_names_en
        elif level_name == LEVEL_NAME_CN:
            self._level_names = _level_names_cn
        elif isinstance(level_name, dict):
            self._level_names = level_name
        else:
            self._level_names = {}
        self._hint_left = hint_left
        self._hint_right = hint_right
        self._hint_separator = hint_separator
        # self._default_format = f"{self._get_hint_str('%(asctime)s')}{self._get_hint_str('%(name)s')}%(message)s"
        if not name:
            name = _get_root_logger_name()
        fmt = fmt or f"{self._get_hint_str('%(asctime)s')}{self._get_hint_str('%(name)s')}%(message)s"

        self._logger = _logging.getLogger(name)
        for _old_handle in self._logger.handlers:
            self._logger.removeHandler(_old_handle)
        if log_colors is None:
            log_colors = self._default_log_colors
        msec = _get_msec_fmt(msec)
        if not log_colors or filename:
            _formatter = _NormalFormatter(fmt, datefmt=datefmt, msecfmt=msec)
        else:
            _formatter = _ColorFormatter(f"%(log_color)s{fmt}", log_colors=log_colors, datefmt=datefmt, msecfmt=msec)
        _hdr.setFormatter(_formatter)
        self._logger.addHandler(_hdr)
        self._logger.setLevel(level)

    def _get_hint_str(self, msg, separator=True):
        if separator:
            return f"{self._hint_left}{msg}{self._hint_right}{self._hint_separator}"
        return f"{self._hint_left}{msg}{self._hint_right}"

    def _get_level_name(self, level):
        lname = self._level_names.get(level, None)
        return self._get_hint_str(lname) if lname else ""

    def __make_title(self, title):
        return "" if not title else self._get_hint_str(title)

    def debug(self, *msgs, title=None):
        self._logger.debug(f"{self._get_level_name(DEBUG)}{self.__make_title(title)}{' '.join(list(map(str, msgs)))}")

    def info(self, *msgs, title=None):
        self._logger.info(f"{self._get_level_name(INFO)}{self.__make_title(title)}{' '.join(list(map(str, msgs)))}")

    def warning(self, *msgs, title=None):
        self._logger.warning(
            f"{self._get_level_name(WARNING)}{self.__make_title(title)}{' '.join(list(map(str, msgs)))}")

    def error(self, *msgs, title=None):
        self._logger.error(f"{self._get_level_name(ERROR)}{self.__make_title(title)}{' '.join(list(map(str, msgs)))}")

    def critical(self, *msgs, title=None):
        self._logger.critical(
            f"{self._get_level_name(CRITICAL)}{self.__make_title(title)}{' '.join(list(map(str, msgs)))}")


def get_logger(name=None, filename=None, filemode=None, level=INFO, level_name=LEVEL_NAME_CN, fmt=None, datefmt=None,
               msec=MILLSECOND, log_colors=None, hint_left='[', hint_right=']', hint_separator=' ', new=False):
    if name is None:
        return _get_root_logger()
    return _QujamLogger(
        name=name,
        filename=filename,
        filemode=filemode,
        level=level,
        level_name=level_name,
        fmt=fmt,
        datefmt=datefmt,
        msec=msec,
        log_colors=log_colors,
        hint_left=hint_left,
        hint_right=hint_right,
        hint_separator=hint_separator,
        new=new,
    )


def set_root_logger(name=None, filename=None, filemode=None, level=INFO, level_name=LEVEL_NAME_CN, fmt=None,
                    datefmt=None,
                    msec=MILLSECOND, log_colors=None, hint_left='[', hint_right=']', hint_separator=' ',
                    farewell=True, farewell_text=None, disable=False):
    now_module = _sys.modules[__name__]
    if disable:
        _atexit.unregister(_farewell)
        setattr(now_module, _root_logger_enable, False)
        return
    elif hasattr(now_module, _root_logger_enable):
        _atexit.register(_farewell)
        setattr(now_module, _root_logger_enable, True)

    if isinstance(name, str):
        setattr(now_module, _root_logger_name, name)

    setattr(now_module, _root_logger_attr, _QujamLogger(
        filename=filename,
        filemode=filemode,
        level=level,
        level_name=level_name,
        fmt=fmt,
        datefmt=datefmt,
        msec=msec,
        log_colors=log_colors,
        hint_left=hint_left,
        hint_right=hint_right,
        hint_separator=hint_separator,
        new=True,
    ))
    if farewell and isinstance(farewell_text, str):
        _set_farewall_text(farewell_text)
    elif not farewell:
        _set_farewall_text(False)


def _get_root_logger():
    now_module = _sys.modules[__name__]
    if not getattr(now_module, _root_logger_enable, True):
        raise RootLoggerDisableError("The root logger has been disabled!")
    root_logger = getattr(now_module, _root_logger_attr, None)
    if not root_logger:
        root_logger = _QujamLogger()
        setattr(now_module, _root_logger_attr, root_logger)
    return root_logger


def _get_root_logger_name():
    now_module = _sys.modules[__name__]
    name = getattr(now_module, _root_logger_name, None)
    if not name:
        name = "Root"
        setattr(now_module, _root_logger_name, name)
    return name


def _set_farewall_text(text):
    now_module = _sys.modules[__name__]
    setattr(now_module, _farewell_text_attr, text)


def _get_farewell_text():
    now_module = _sys.modules[__name__]
    farewall_text = getattr(now_module, _farewell_text_attr, None)
    if farewall_text is None:
        farewall_text = "程序已退出，欢迎下次使用！"
        setattr(now_module, _farewell_text_attr, farewall_text)
    return farewall_text


def debug(*msgs, title=None):
    _get_root_logger().debug(*msgs, title=title)


def info(*msgs, title=None):
    _get_root_logger().info(*msgs, title=title)


def warning(*msgs, title=None):
    _get_root_logger().warning(*msgs, title=title)


def error(*msgs, title=None):
    _get_root_logger().error(*msgs, title=title)


def critical(*msgs, title=None):
    _get_root_logger().critical(*msgs, title=title)


@_atexit.register
def _farewell():
    farewell_text = _get_farewell_text()
    if farewell_text:
        info(farewell_text)
