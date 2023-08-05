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
import datetime
import pandas as pd
from ..tools import get_protoclass_attrs
from ..convertor import ToPyobj

from .base import ConfiguratorBase, ProtoWrapper
from AztClient.protocols import MsgProto, EnumProto


class AztCalendarConfigurator(ConfiguratorBase):
    def to_proto(self, pyobj, pbobj: ProtoWrapper):
        raise NotImplementedError

    def get_attrs(self):
        return ()

    def to_pyobj(self, pbobj: ProtoWrapper, pyobj):
        dates_str = pbobj.getattr("calendar", _raise=True)
        setattr(pyobj, "market", pbobj.getattr("market", _raise=True))
        if not dates_str:
            setattr(pyobj, "calendar", [])
            return pyobj
        dt_year = pbobj.getattr("calendar_year", _raise=True)
        dt_list = list(map(lambda x: datetime.datetime.strptime(f"{dt_year}{x}", "%Y%m%d"),
                           filter(lambda x: x, dates_str.split(","))))
        setattr(pyobj, "calendar", dt_list)
        return pyobj


class AztFundamentalDataConfigurator(ConfiguratorBase):
    def to_proto(self, pyobj, pbobj: ProtoWrapper):
        raise NotImplementedError

    def get_attrs(self):
        return ()

    def __init__(self, datapb, dataname, dtattrs=()):
        self._datapb = datapb
        self._dataname = dataname
        self._fields = ['pub_date'] + sorted(
            list(set(get_protoclass_attrs(self._datapb)) - {'pub_date', 'market', 'code'}))
        self._dtattrs = set(dt for dt in dtattrs if dt in self._fields)

    def to_pyobj(self, pbobj: ProtoWrapper, pyobj):
        df = pd.DataFrame(
            list(dict((attr, getattr(data, attr)) for attr in self._fields) for data in
                 pbobj.getattr(self._dataname, _raise=True)))
        if not df.empty:
            for dtattr in self._dtattrs:
                try:
                    df[dtattr] = df[dtattr].apply(lambda x: datetime.datetime.fromtimestamp(x))
                except KeyError:
                    continue
                except Exception:
                    raise
        return df


class AztFundamentalConfigurator(ConfiguratorBase):
    def to_proto(self, pyobj, pbobj: ProtoWrapper):
        raise NotImplementedError

    def get_attrs(self):
        return ()

    def __init__(self, mapping):
        self._mapping = mapping
        pass

    def to_pyobj(self, pbobj: ProtoWrapper, pyobj):
        setattr(pyobj, "market", pbobj.getattr("market", _raise=True))
        setattr(pyobj, "code", pbobj.getattr("code", _raise=True))
        data_type = pbobj.getattr("fundamentals_type", _raise=True)
        setattr(pyobj, "fundamentals_type", data_type)
        datapb = self._mapping[data_type]()
        if pbobj.getattr("datas").Unpack(datapb):
            setattr(pyobj, "datas", ToPyobj(datapb))
        return pyobj


class AztQuoteMsgConfigurator(ConfiguratorBase):

    def to_proto(self, pyobj, pbobj: ProtoWrapper):
        raise NotImplementedError

    def to_pyobj(self, pbobj: ProtoWrapper, pyobj):
        data_type = pbobj.getattr("data_type")
        if data_type is not None:
            setattr(pyobj, "data_type", data_type)
        base_msg_pb = pbobj.getattr("quote_base_msg")
        if base_msg_pb is None:
            return pyobj
        base_msg_py = ToPyobj(base_msg_pb)
        setattr(pyobj, "quote_base_msg", base_msg_py)
        extra_any = pbobj.getattr("extra_data")
        sec_type = base_msg_py.security_type
        if sec_type == EnumProto.KSecurityType_Stock:
            extra_pbobj = MsgProto.Quote_QuoteStockExtra()
        elif sec_type == EnumProto.KSecurityType_Fund:
            extra_pbobj = MsgProto.Quote_QuoteStockExtra()  # 待完善
        elif sec_type == EnumProto.KSecurityType_Bond:
            extra_pbobj = MsgProto.Quote_QuoteStockExtra()  # 待完善
        elif sec_type == EnumProto.KSecurityType_Index:
            extra_pbobj = MsgProto.Quote_QuoteStockExtra()  # 待完善
        else:
            extra_pbobj = MsgProto.Quote_QuoteStockExtra()  # 待完善
        extra_any.Unpack(extra_pbobj)
        extra_pyobj = ToPyobj(extra_pbobj)
        setattr(pyobj, "extra_data", extra_pyobj)
        return pyobj

    def get_attrs(self):
        return ()
