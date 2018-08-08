from Cryptography.Ciphers._cipher             import Cipher     # For abstract superclass
from Cryptography                 import misc                   # For miscellaneous functions



class Rotation(Cipher):

    # Cipher info:
    CIPHER_NAME         = "Rotation using Modular Addition"
    CHAR_SET            = "alphabet"
    CIPHER_TYPE         = "symmetric"
    KEY_TYPE            = "single character"

    IS_BLOCK_CIPHER      = False
    VARIABLE_BLOCK_SIZE  = False
    DEFAULT_BLOCK_SIZE   = 0
    MIN_BLOCKS_SIZE      = 0
    MAX_BLOCK_SIZE       = 0
    AUTO_TEST_BLOCK_SIZE = 0
    VARIABLE_KEY_SIZE    = False
    DEFAULT_KEY_SIZE     = 0
    MIN_KEY_SIZE         = 0
    MAX_KEY_SIZE         = 0
    AUTO_TEST_KEY_SIZE   = 0

    RESTRICT_ALPHABET   = True
    NEEDS_ENGLISH       = False


    # Constructor
    def __init__(self, plaintext:str, ciphertext:str, char_set:str, mode_of_op:str, key:str, public_key:str,
                    private_key:str, block_size:int, key_size:int, source_location:str, output_location:str) -> None:

        super().__init__(plaintext,   ciphertext,     char_set,     "",                    key,     "",
                    "",              0,              0,            source_location,     output_location    )




    # Algorithm to encrypt plaintext
    @misc.store_time_in("self.encrypt_time_overall", "self.encrypt_time_for_algorithm")
    def encrypt_plaintext(self) -> None:
        """
        This encrypts with a rotation cipher (using modular addition) and fills in self.ciphertext

        :return:          (None)
        """

        # Parameters for encryption
        plaintext  = self.plaintext
        key        = self.key
        alphabet   = self.char_set

        # Other important variables
        ciphertext    = []                                # The list to build up the ciphertext, one character at a time
        alphabet_size = Cipher.ALPHABETS.get(alphabet)      # The size of the alphabet (used as modulus)


        # Encrypt every single character in the plaintext
        for i in range(0, len(plaintext)):

            plain_val = misc.ord_adjusted(plaintext[i])   # The unicode value for the current plaintext char
            key_val   = misc.ord_adjusted(key[0])         # Figure out the unicode value of the key character


            # Figure out the encrypted character val
            encrypted_char = misc.chr_adjusted((plain_val + key_val) % alphabet_size)
            ciphertext.append(encrypted_char)

            # Print updates
            if i % misc.utf_8_to_int_blocks.update_interval == 0:
                print("Encryption percent done: {}{:.2%}{}"
                      .format("\u001b[32m",
                              i / len(plaintext),
                              "\u001b[0m"))

        # Concatenate all the characters in the list into one string
        ciphertext = "".join(ciphertext)

        # Set the self object's ciphertext
        self.ciphertext = ciphertext

        return None





    # Algorithm to decrypt plaintext
    @misc.store_time_in("self.decrypt_time_overall", "self.decrypt_time_for_algorithm")
    def decrypt_ciphertext(self) -> None:
        """
        This decrypts with a rotation cipher (using modular subtraction)

        :return:           (None)
        """

        # Parameters for decryption
        ciphertext = self.ciphertext
        key        = self.key
        alphabet   = self.char_set

        # Other important variables
        plaintext     = []                                # The list to build up the ciphertext, one character at a time
        alphabet_size = Cipher.ALPHABETS.get(alphabet)      # Size of alphabet (used as modulus)


        # Decrypt every single character in the ciphertext
        for i in range(0, len(ciphertext)):
            cipher_val = misc.ord_adjusted(ciphertext[i])  # The unicode value for the current ciphertext char
            key_val    = misc.ord_adjusted(key[0])         # Figure out the unicode value of the key character

            # Figure out the decrypted character val
            decrypted_char = misc.chr_adjusted((cipher_val - key_val) % alphabet_size)
            plaintext.append(decrypted_char)


            # Print updates
            if i % misc.utf_8_to_int_blocks.update_interval == 0:
                print("Decryption percent done: {}{:.2%}{}"
                      .format("\u001b[32m",
                              i / len(ciphertext),
                              "\u001b[0m"))


        # Concatenate all the characters in the list into one string
        plaintext = "".join(plaintext)


        # Fill in self's plaintext
        self.plaintext = plaintext


        return None






    # Write to the file about the statistics of the file (Call super-method)
    def write_statistics(self, file_path:str) -> None:
        """
        Write statistics

        :param file_path:   (str)  The file to write the statistics in
        :return:            (None)
        """

        super().write_statistics_in_file(file_path, {})
