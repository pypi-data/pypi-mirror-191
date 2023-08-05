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

class AztUserInfo:
    def __init__(self, account=None, passwd=None, stgyid=None, stgycheck=None):
        self.__account = account
        self.__passwd = passwd
        self.__stgyid = stgyid
        self.__stgycheck = stgycheck

    def set(self, account=None, passwd=None, stgyid=None, stgycheck=None):
        if account:
            self.__account = account
        if passwd:
            self.__passwd = passwd
        if stgyid:
            self.__stgyid = stgyid
        if stgycheck:
            self.__stgycheck = stgycheck

    def getaccount(self):
        return self.__account

    def getpasswd(self):
        return self.__passwd

    def getstgyid(self):
        return self.__stgyid

    def getstgycheck(self):
        return self.__stgycheck
