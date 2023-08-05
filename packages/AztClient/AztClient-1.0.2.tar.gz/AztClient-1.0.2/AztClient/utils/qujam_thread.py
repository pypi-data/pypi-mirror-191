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

import threading
from threading import Thread
from traceback import format_exc
import warnings


class QujamThreadWarning(UserWarning):
    pass


class QujamThread(Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None, _warning=False) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._exception = None
        self._exc_traceback = ''
        self._enable_warning = _warning

    def run(self) -> None:
        try:
            super().run()
        except Exception as exc:
            self._exception = exc
            self._exc_traceback = format_exc()
            if self._enable_warning:
                exc_warning = f"Execption happened in {self.getName()}:\n{self._exc_traceback}"
                warnings.warn(exc_warning, category=QujamThreadWarning)

    def has_exception(self) -> bool:
        return not not self._exception

    def get_exception(self) -> Exception:
        return self._exception

    def exception_traceback(self) -> str:
        return self._exc_traceback

    def joinable(self):
        if threading.current_thread() is self:
            return False
        return True
