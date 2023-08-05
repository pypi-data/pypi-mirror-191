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

import dataclasses


def get_dataclass_attrs(dataclass):
    datacls_fields = getattr(dataclass, "__dataclass_fields__", None)
    if datacls_fields:
        return tuple(f.name for f in datacls_fields.values() if f._field_type is dataclasses._FIELD and f.repr)
    all_attrs = dir(dataclass)
    return tuple(filter(lambda x: not x.startswith("_") and not callable(getattr(dataclass, x)), all_attrs))


def get_protoclass_attrs(protoclass, wrap=False):
    if wrap:
        return [field.name for field in protoclass.getattr("DESCRIPTOR", _raise=True).fields]
    return [field.name for field in getattr(protoclass, "DESCRIPTOR").fields]
