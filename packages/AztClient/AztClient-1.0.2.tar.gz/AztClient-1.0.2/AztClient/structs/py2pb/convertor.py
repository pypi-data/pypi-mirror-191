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

import uuid
import sys as _sys
from .tools import get_dataclass_attrs

_register_tag = f"__Py2Pb_Register_Object_{uuid.uuid4()}__"
_auto_cfg_tag = f"__Auto_Configurator_{uuid.uuid4()}"
_pbmpysingle = dict()


def _register_pypb(pycls, pbcls):
    global _pbmpysingle
    _pbmpysingle[pbcls] = pycls


def Registered(pyobj):
    return hasattr(pyobj, _register_tag)


def GetConvertor(pyobj):
    return getattr(pyobj, _register_tag)


def GetPbCls(pycls):
    _convertor = getattr(pycls, _register_tag)
    return _convertor.pbcls


def GetPyCls(pbcls):
    return _pbmpysingle.get(pbcls)


def GetAutoConfigurator():
    return getattr(_sys.modules[__name__], _auto_cfg_tag, None)


def SetAutoConfigurator(cls):
    setattr(_sys.modules[__name__], _auto_cfg_tag, cls)


# @cal_time
def ToProto(pyobj):
    return GetConvertor(pyobj).ToProto(pyobj)


# @cal_time
def ToPyobj(pbobj):
    return GetConvertor(GetPyCls(pbobj.__class__)).ToPyobj(pbobj)


def ToPyobjSpec(pbobj, pycls):
    return GetConvertor(pycls).ToPyobj(pbobj)


class RegisterConvertor:

    def __init__(self, *cfgtors, pyclass=None, protobuf=None, py_spec=False):
        self.cfgtors = cfgtors
        self.pycls = None
        self.pbcls = protobuf
        self._py_spec = py_spec
        self._enable_auto_attrs = True
        self._auto_attrs_handles = ()
        self._py_handles = ()
        if pyclass:
            self.Register(pyclass)

    def Register(self, pyclass):
        if not pyclass:
            raise Exception("Parameter 'pyclass' cannot be None")
        if hasattr(pyclass, _register_tag):
            return
        if not self.pbcls:
            raise Exception("The parameter 'protobuf' must be passed before register")

        self.pycls = pyclass
        setattr(self.pycls, _register_tag, self)
        if not self._py_spec:  # 如果不是特殊情况(多个pycls对一个pbcls)
            _register_pypb(self.pycls, self.pbcls)
        if self._enable_auto_attrs:
            self._add_auto_attrs()
        if self._py_handles:
            self._add_py_handles()
        return self.pycls

    def SetAutoAttrs(self, enable=True, *handles):
        self._enable_auto_attrs = enable
        if handles:
            self._auto_attrs_handles = handles
        return self

    def SetPyHandles(self, *py_handles):
        if py_handles:
            self._py_handles = py_handles
        return self

    def ToProto(self, pyobj):
        pbobj = self.pbcls()
        for cfgtor in self.cfgtors:
            pbobj = cfgtor.ToProto(pyobj, pbobj)
        return pbobj

    def ToPyobj(self, pbobj):
        pyobj = self.pycls()
        for cfgtor in self.cfgtors:
            pyobj = cfgtor.ToPyobj(pbobj, pyobj)
        return pyobj

    def _add_auto_attrs(self):
        _auto_cfg = GetAutoConfigurator()
        if not _auto_cfg:
            return
        pycls_attrs = get_dataclass_attrs(self.pycls)
        if not pycls_attrs:
            return
        ready_cfg_attrs = ()
        for cfg in self.cfgtors:
            ready_cfg_attrs += cfg.get_attrs()
        remain_attrs = tuple(filter(lambda x: x not in ready_cfg_attrs, pycls_attrs))
        if not remain_attrs:
            return
        _auto_cfgtor = _auto_cfg(*remain_attrs)
        if self._auto_attrs_handles:
            _auto_cfgtor = _auto_cfgtor.SetCfgHandle(*self._auto_attrs_handles)
        self.cfgtors += (_auto_cfgtor,)

    def _add_py_handles(self):
        for py_handle in self._py_handles:
            self.pycls = py_handle.Handle(self.pycls)
