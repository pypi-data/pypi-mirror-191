# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import abc
from typing import Optional

from substrateinterface import Keypair

from tikka.domains.entities.identity import Identity
from tikka.interfaces.domains.connections import ConnectionsInterface


class NetworkIdentitiesInterface(abc.ABC):
    """
    NetworkIdentitiesInterface class
    """

    def __init__(self, connections: ConnectionsInterface) -> None:
        """
        Use connections to request identities information

        :param connections: ConnectionsInterface instance
        :return:
        """
        self.connections = connections

    @abc.abstractmethod
    def get_identity_index(self, address: str) -> Optional[int]:
        """
        Return the account Identity instance from address if exists

        :param address: Account address
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_identity(self, index: int) -> Optional[Identity]:
        """
        Return the account Identity instance from index if exists

        :param index: Identity index
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def change_owner_key(self, old_keypair: Keypair, new_keypair: Keypair) -> bool:
        """
        Change identity owner from old_keypair to new_keypair

        :param old_keypair: Keypair of current identity account
        :param new_keypair: Keypair of new identity account
        :return:
        """
        raise NotImplementedError
