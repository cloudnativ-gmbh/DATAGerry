# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import logging
from typing import Union

from authlib.jose import jwt, JsonWebToken
from authlib.jose.errors import BadSignatureError, InvalidClaimError

from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.security.key.holder import KeyHolder

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


class TokenValidator:
    """
    Decodes and validates tokens
    """

    def __init__(self, database_manager: DatabaseManagerMongo):
        self.key_holder = KeyHolder(database_manager)

    def decode_token(self, token: Union[JsonWebToken, str, dict]):
        """
        Decodes a given token

        Params:
            token(JsonWebToken, str, dict): the given token
        Returns:
            JWTClaims: decoded token
        """
        try:
            decoded_token = jwt.decode(s=token, key=self.key_holder.get_public_key())
        except (BadSignatureError, Exception) as err:
            raise ValidationError(err) from err
        return decoded_token


    def validate_token(self, token: Union[JsonWebToken, str, dict]):
        """
        Validates a given token regarding its expiration

        Params:
            token(JsonWebToken, str, dict): the given token
        Returns:
            JWTClaims: decoded token
        """
        try:
            import time
            token.validate(time.time())
        except InvalidClaimError as err:
            raise ValidationError(err) from err


class ValidationError(CMDBError):

    def __init__(self, message):
        self.message = f'Error while decode the token operation - E: ${message}'
