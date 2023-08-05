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
from .base_handle import DefaultConfigHandle
from AztClient.protocols import EnumProto as _EProto


class Azt_PlaceOrder_effect_handle(DefaultConfigHandle):
    def PostToPyobj(self, pyobj):
        if pyobj.effect is None:
            if pyobj.order_side == _EProto.KOrderDirection_Buy:
                pyobj.effect = _EProto.KPositionEffect_Open
            elif pyobj.order_side == _EProto.KOrderDirection_Sell:
                pyobj.effect = _EProto.KPositionEffect_Close
        return pyobj
