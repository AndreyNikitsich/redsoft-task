from django.contrib.auth.hashers import BasePasswordHasher, mask_hash
from django.utils.crypto import constant_time_compare
from Crypto.Cipher import AES
from django.conf import settings
from django.utils.translation import gettext_noop as _


class AesPasswordEncryption(BasePasswordHasher):
    """
    The Salted AES password encryption algorithm
    """

    algorithm = "aes"

    def encode(self, password, nonce=None):
        if nonce:
            nonce = nonce.encode()
        cipher = AES.new(settings.PASSWORD_ENCRYPTION_KEY, AES.MODE_EAX, nonce=nonce)
        nonce = cipher.nonce.decode()
        hash, _ = cipher.encrypt_and_digest(password.encode())
        return "%s$%s$%s" % (self.algorithm, nonce, hash)

    def decode(self, encoded):
        algorithm, nonce, hash = encoded.split("$", 2)
        assert algorithm == self.algorithm
        return {
            "algorithm": algorithm,
            "hash": hash,
            "nonce": nonce,
        }

    def verify(self, password, encoded):
        decoded = self.decode(encoded)
        encoded_2 = self.encode(password, decoded["nonce"])
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        decoded = self.decode(encoded)
        return {
            _("algorithm"): decoded["algorithm"],
            _("nonce"): mask_hash(decoded["nonce"], show=2),
            _("hash"): mask_hash(decoded["hash"]),
        }

    def must_update(self, encoded):
        return False

    def harden_runtime(self, password, encoded):
        pass
