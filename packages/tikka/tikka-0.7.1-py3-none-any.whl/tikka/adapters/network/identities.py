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
import logging
import struct
from typing import Optional

from substrateinterface import Keypair
from substrateinterface.exceptions import SubstrateRequestException

from tikka.domains.entities.identity import Identity
from tikka.interfaces.adapters.network.identities import NetworkIdentitiesInterface


class NetworkIdentities(NetworkIdentitiesInterface):
    """
    NetworkIdentities class
    """

    def get_identity_index(self, address: str) -> Optional[int]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkIdentitiesInterface.get_identity_index.__doc__
        )
        if not self.connections.is_connected():
            return None
        if self.connections.rpc.client is None:
            return None

        try:
            result = self.connections.rpc.client.query(
                "Identity", "IdentityIndexOf", [address]
            )
        except Exception as exception:
            logging.exception(exception)
            return None

        return result.value

    def get_identity(self, index: int) -> Optional[Identity]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkIdentitiesInterface.get_identity.__doc__
        )
        if not self.connections.is_connected():
            return None
        if self.connections.rpc.client is None:
            return None

        try:
            result = self.connections.rpc.client.query(
                "Identity", "Identities", [index]
            )
        except Exception as exception:
            logging.exception(exception)
            return None
        return Identity(
            index=index,
            next_creatable_on=result["next_creatable_identity_on"].value,
            removable_on=int(result["removable_on"].value),
            status=result["status"].value,
        )

    def change_owner_key(self, old_keypair: Keypair, new_keypair: Keypair) -> bool:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkIdentitiesInterface.change_owner_key.__doc__
        )
        if not self.connections.is_connected():
            return False
        if self.connections.rpc.client is None:
            return False

        identity_index = self.get_identity_index(old_keypair.ss58_address)
        if identity_index is None:
            return False

        # message to sign
        prefix_bytes = b"icok"
        genesis_hash_str = self.connections.rpc.client.get_block_hash(0)
        genesis_hash_bytes = bytearray.fromhex(genesis_hash_str[2:])
        identity_index_bytes = struct.pack("<I", identity_index)
        identity_pubkey_bytes = old_keypair.public_key
        message_bytes = (
            prefix_bytes
            + genesis_hash_bytes
            + identity_index_bytes
            + identity_pubkey_bytes
        )

        # message signed by the new owner
        signature_bytes = new_keypair.sign(message_bytes)

        params = {"new_key": new_keypair.ss58_address, "new_key_sig": signature_bytes}
        try:
            # create raw call (extrinsic)
            call = self.connections.rpc.client.compose_call(
                call_module="Identity",
                call_function="change_owner_key",
                call_params=params,
            )
        except Exception as exception:
            logging.exception(exception)
            return False

        try:
            # create extrinsic signed by current owner
            extrinsic = self.connections.rpc.client.create_signed_extrinsic(
                call=call, keypair=old_keypair
            )
        except Exception as exception:
            logging.exception(exception)
            return False

        try:
            response = self.connections.rpc.client.submit_extrinsic(
                extrinsic, wait_for_inclusion=True
            )
        except SubstrateRequestException as exception:
            logging.exception(exception)
            return False

        if response.is_success is False:
            logging.error(response.error_message)

        return response.is_success
