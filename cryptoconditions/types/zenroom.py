import base58
from base64 import urlsafe_b64decode, urlsafe_b64encode

from pyasn1.codec.der.encoder import encode as der_encode
from pyasn1.codec.native.decoder import decode as nat_decode

from cryptoconditions.crypto import base64_add_padding, base64_remove_padding
from cryptoconditions.types.base_sha256 import BaseSha256
from cryptoconditions.schemas.fingerprint import ZenroomFingerprintContents

from cryptoconditions.zencode import read_zencode
from zenroom_minimal import Zenroom

import pdb

class ZenroomSha256(BaseSha256):
    """ """

    TYPE_ID = 5
    TYPE_NAME = 'zenroom-sha-256'
    TYPE_ASN1 = 'zenroomSha256'
    TYPE_ASN1_CONDITION = 'zenroomSha256Condition'
    TYPE_ASN1_FULFILLMENT = 'zenroomSha256Fulfillment'
    TYPE_CATEGORY = 'simple'

    CONSTANT_COST = 131072
    PUBLIC_KEY_LENGTH = 32
    SIGNATURE_LENGTH = 64

    # TODO docstrings
    # TODO is conf necessary?
    def __init__(self, *, script=None, data=None, keys=None, conf=None):
        """
        ZENROOM: Zenroom signature condition.

        This condition implements Zenroom signatures.

        ZENROOM is assigned the type ID 4. It relies only on the ZENROOM feature suite
        which corresponds to a bitmask of 0x20.

        Args:
            public_key (bytes): Zenroom public key.
            signature (bytes): Signature.

        """
        self.script = script
        self.data = data
        self.keys = keys
        self.conf = conf

    # TODO validate script
    def _validate_script(self, script):
        return script

    @property
    def script(self):
        return self._script

    @script.setter
    def script(self, script):
        self._script = self._validate_script(script)

    # TODO validate data
    def _validate_data(self, data):
        return data

    @property
    def data(self):
        return self._data or b''

    @data.setter
    def data(self, data):
        self._data = self._validate_data(data)

    # TODO validate keys
    def _validate_keys(self, keys):
        return keys

    @property
    def keys(self):
        return self._keys or b''

    @keys.setter
    def keys(self, keys):
        self._keys = self._validate_keys(keys)

    # TODO validate conf
    def _validate_conf(self, conf):
        return conf

    @property
    def conf(self):
        return self._conf or b''

    @conf.setter
    def conf(self, conf):
        self._conf = self._validate_conf(conf)


    @property
    def asn1_dict_payload(self):
        return {
            'script': self.script,
            'data': self.data,
            'keys': self.keys,
            'conf': self.conf,
        }

    @property
    def fingerprint_contents(self):
        asn1_fingerprint_obj = nat_decode(
            {'script': self.script},
            asn1Spec=ZenroomFingerprintContents(),
        )
        return der_encode(asn1_fingerprint_obj)


    def calculate_cost(self):
        # TODO needs to be modified ???
        return ZenroomSha256.CONSTANT_COST

    def to_asn1_dict(self):
        return {self.TYPE_ASN1: self.asn1_dict_payload}

    # TODO Adapt according to outcomes of
    # https://github.com/rfcs/crypto-conditions/issues/16
    def to_dict(self):
        """
        Generate a dict of the fulfillment

        Returns:
            dict: representing the fulfillment
        """
        return {
            'type': ZenroomSha256.TYPE_NAME,
            'script': base58.b58encode(self.script),
            'data': base58.b58encode(self.data),
            'keys': base58.b58encode(self.keys),
            'conf': base58.b58encode(self.conf),
        }

    # TODO Adapt according to outcomes of
    # https://github.com/rfcs/crypto-conditions/issues/16
    def to_json(self):
        """
        Generate a dict of the fulfillment

        Returns:
            dict: representing the fulfillment
        """
        return {
            'type': ZenroomSha256.TYPE_NAME,
            'script': base64_remove_padding(
                urlsafe_b64encode(self.script)),
            'data': base64_remove_padding(
                urlsafe_b64encode(self.data)),
            'keys': base64_remove_padding(
                urlsafe_b64encode(self.keys)),
            'conf': base64_remove_padding(
                urlsafe_b64encode(self.conf)),
        }

    # TODO Adapt according to outcomes of
    # https://github.com/rfcs/crypto-conditions/issues/16
    def parse_dict(self, data):
        """
        Generate fulfillment payload from a dict

        Args:
            data (dict): description of the fulfillment

        Returns:
            Fulfillment
        """
        self.script = base58.b58decode(data['script'])
        self.data = base58.b58decode(data['data'])
        self.keys = base58.b58decode(data['keys'])
        self.conf = base58.b58decode(data['conf'])

    # TODO Adapt according to outcomes of
    # https://github.com/rfcs/crypto-conditions/issues/16
    def parse_json(self, data):
        """
        Generate fulfillment payload from a dict

        Args:
            data (dict): description of the fulfillment

        Returns:
            Fulfillment
        """
        self.script = urlsafe_b64decode(base64_add_padding(
            data['script']))
        self.data = urlsafe_b64decode(base64_add_padding(
            data['data']))
        self.keys = urlsafe_b64decode(base64_add_padding(
            data['keys']))
        self.conf = urlsafe_b64decode(base64_add_padding(
            data['conf']))

    def parse_asn1_dict_payload(self, data):
        self.script = data['script']
        self.data = data['data']
        self.keys = data['keys']
        self.conf = data['conf']

    def validate(self, *, message):
        """
        Verify the signature of this Zenroom fulfillment.

        The signature of this Zenroom fulfillment is verified against
        the provided message and public key.

        Args:
            message (str): Message to validate against.

        Return:
            boolean: Whether this fulfillment is valid.
        """
        zenroom = Zenroom(read_zencode)

        print(self.script)
        print(self.data)
        print(self.keys)
        print(self.conf)

        try:
            zenroom.load(self.script.decode('utf-8'))
            zenroom.load_data(self.data.decode('utf-8'))
            zenroom.load_keys(self.keys.decode('utf-8'))
            result = zenroom.eval()
            print(result)
        except:
            return False

        print("VALID")
        return False
