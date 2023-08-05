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

from ..protobuf_wrapper import ProtoWrapper
from ..configurator_handles import DefaultConfigHandle


class MetaConfigurator(type):
    def __call__(cls, *args, **kwargs):
        obj = super(MetaConfigurator, cls).__call__(*args, **kwargs)
        obj._cfg_handles = (DefaultConfigHandle(),)
        return obj


class ConfiguratorBase(metaclass=MetaConfigurator):
    def ToProto(self, pyobj, pbobj):
        handles = getattr(self, "_cfg_handles")
        for handle in handles:
            pyobj, pbobj = handle.PreToProto(pyobj, pbobj)
        pbobj = self.to_proto(pyobj, pbobj)
        for handle in handles:
            pbobj = handle.PostToProto(pbobj)
        return pbobj

    def ToPyobj(self, pbobj, pyobj):
        handles = getattr(self, "_cfg_handles")
        for handle in handles:
            pbobj, pyobj = handle.PreToPyobj(pbobj, pyobj)

        pyobj = self.to_pyobj(pbobj, pyobj)
        for handle in handles:
            pyobj = handle.PostToPyobj(pyobj)
        return pyobj

    def SetCfgHandle(self, *handles):
        if handles:
            setattr(self, "_cfg_handles", getattr(self, "_cfg_handles") + handles)
        return self

    def to_proto(self, pyobj, pbobj: ProtoWrapper):
        raise NotImplementedError

    def to_pyobj(self, pbobj: ProtoWrapper, pyobj):
        raise NotImplementedError

    def get_attrs(self):
        raise NotImplementedError
