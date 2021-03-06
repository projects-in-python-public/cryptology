from Cryptography.Ciphers._cipher             import Cipher     # For abstract superclass
from Cryptography                 import misc                   # For miscellaneous functions
import pyximport; pyximport.install()
from Cryptography_Cython.Ciphers_Cython import vigenere_cy



class Vigenere(Cipher):

    # Cipher info:
    CIPHER_NAME         = "Vigenere using Modular Addition"
    CHAR_SET            = "alphabet"
    CIPHER_TYPE         = "symmetric"
    KEY_TYPE            = "multiple characters"

    IS_BLOCK_CIPHER      = False
    VARIABLE_BLOCK_SIZE  = False
    DEFAULT_BLOCK_SIZE   = 0
    AUTO_TEST_BLOCK_SIZE = 0

    VARIABLE_KEY_SIZE    = False
    DEFAULT_KEY_SIZE     = 0
    AUTO_TEST_KEY_SIZE   = 0

    RESTRICT_ALPHABET   = True
    NEEDS_ENGLISH       = False


    # Constructor
    def __init__(self, plaintext:str, ciphertext:str, char_set:str, mode_of_op:str, key:str, public_key:str,
                    private_key:str, block_size:int, key_size:int, source_location:str, output_location:str) -> None:

        super().__init__(plaintext,   ciphertext,     char_set,     "",     key,                    "",
                    "",              0,              0,            source_location,     output_location    )



    # Algorithm to encrypt plaintext
    @misc.process_times("self.encrypt_time_for_algorithm", "self.encrypt_time_overall", "self.encrypt_time_for_key")
    @misc.static_vars(time_overall=0, time_algorithm=0, time_key=0)
    def encrypt_plaintext(self, plaintext="", key="", alphabet="") -> str:
        """
        This works like rotation, but cycles the letters of the key used. So, the first character is encrypted with
        the first letter, the second character with the second letter, and so on. When we run out of characters in
        the key, just start the cycle from the first key again.

        :param plaintext: (str) The plaintext to encrypt
        :param key:       (str) The key to encrypt with
        :param alphabet:  (str) The name of the character set to encrypt into
        :return:          (str) The encrypted ciphertext
        """

        # Parameters for encryption (if not provided)
        if plaintext == "" and key == "" and alphabet == "":
            plaintext  = self.plaintext
            key        = self.key
            alphabet   = self.char_set

        # Other important variables
        ciphertext    = []                              # The list to build up the ciphertext, one character at a time
        alphabet_size = Cipher.ALPHABETS.get(alphabet)  # The size of the alphabet (used as modulus)



        # Encrypt the plaintext
        ciphertext = vigenere_cy.encrypt_plaintext(plaintext, key, alphabet_size)



        # Set variables, and return
        self.ciphertext = ciphertext
        return ciphertext








    # Algorithm to decrypt plaintext
    @misc.process_times("self.decrypt_time_for_algorithm", "self.decrypt_time_overall", "self.decrypt_time_for_key")
    @misc.static_vars(time_overall=0, time_algorithm=0, time_key=0)
    def decrypt_ciphertext(self, ciphertext="", key="", alphabet="") -> str:
        """
        This does the same thing as encrypt, but modularly subtracts to do the reversal.

        :param ciphertext: (str) The ciphertext to decrypt
        :param key:        (str) The key to decrypt with
        :param alphabet:   (str) The name of the alphabet to use
        :return:           (str) The decrypted plaintext
        """

        # Parameters for decryption (if not provided)
        if ciphertext == "" and key == "" and alphabet == "":
            ciphertext = self.ciphertext
            key        = self.key
            alphabet   = self.char_set


        # Other important variables
        plaintext     = []                              # The list to build up the ciphertext, one character at a time
        alphabet_size = Cipher.ALPHABETS.get(alphabet)  # Size of alphabet (used as modulus)






        # Decrypt the ciphertext
        plaintext = vigenere_cy.decrypt_ciphertext(ciphertext, key, alphabet_size)




        # Set variables and return
        self.plaintext = plaintext
        return plaintext








    # Write to the file about the statistics of the file (Call super-method)
    def write_statistics(self, file_path:str, leave_empty={}) -> None:
        """
        Write statistics

        :param file_path:   (str)  The file to write the statistics in
        :param leave_empty: (dict) Exists to match superclass method signature
        :return:            (None)
        """
        super().write_statistics(file_path)



































