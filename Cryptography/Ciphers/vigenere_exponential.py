from Cryptography.Ciphers._cipher             import Cipher     # For abstract superclass
from Cryptography                 import misc                   # For miscellaneous functions



class VigenereExponential(Cipher):

    # Cipher info:
    CIPHER_NAME         = "Vigenere using Modular Exponentiation"
    CHAR_SET            = "alphabet"
    CIPHER_TYPE         = "symmetric"
    KEY_TYPE            = "multiple characters"

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

    RESTRICT_ALPHABET   = False
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


        # Important variables to use during encryption
        ciphertext           = []                           # Build up the ciphertext here, one character at time
        key_index            = 0                            # The key index to get the character to use in the key
        characters_encrypted = 0                            # The number of characters encrypted




        # For each character in plaintext
        for char in plaintext:

            # Print updates (every 100 characters)
            characters_encrypted += 1
            if characters_encrypted % 1000 == 0 or characters_encrypted == len(self.plaintext):
                print("ENCRYPTION\tPercent of text done: {}{}%{} with {} characters"
                      .format("\u001b[32m",
                              format((characters_encrypted / len(plaintext)) * 100, ".2f"),
                              "\u001b[0m",
                              "{:,}".format(characters_encrypted)))


            # Obtain the two unicode values to operate on
            plain_val   = misc.ord_adjusted(char)                  # Find unicode value of plaintext char
            key_val     = misc.ord_adjusted(key[key_index])        # Find unicode value of the key
            key_index   = (key_index + 1) % len(key)               # Update key index for next iteration


            # Figure out the encrypted character
            encrypted_val = pow(plain_val, key_val, Cipher.ALPHABETS.get(self.char_set))
            encrypted_char = misc.chr_adjusted(encrypted_val)

            # Obtain the number of overlaps that come before this one (this plain_val) and NOT including this one
            overlap_counter = 0
            for i in range(0, plain_val):
                # If it is an overlap character
                if pow(i, key_val, Cipher.ALPHABETS.get(self.char_set)) == encrypted_val and i != plain_val:
                    overlap_counter += 1





            # Add the block of information to the ciphertext
            ciphertext.append("{}{} ".format(encrypted_char, overlap_counter))



        # Join the ciphertext
        ciphertext = "".join(ciphertext)

        # Set the self object's ciphertext
        self.ciphertext = ciphertext


        # Return none
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
        plaintext            = []                           # Build up the plaintext here, one character at a time
        key_index            = 0                            # The key index to get the character to use in the key
        characters_decrypted = 0                            # The number of characters encrypted
        ciphertext_index     = 0                            # An index used for reading the ciphertext



        # While not finished processing ciphertext. Will be processing one block/unit at a time
        while ciphertext_index < len(ciphertext):

            # Print updates (every 100 characters)
            characters_decrypted += 1
            if characters_decrypted % 1000 == 0 or characters_decrypted == len(self.plaintext):
                print("DECRYPTION\tPercent of text done: {}{}%{} with {} characters"
                      .format("\u001b[32m",
                              format((characters_decrypted / len(self.plaintext)) * 100, ".2f"),
                              "\u001b[0m",
                              "{:,}".format(characters_decrypted)))


            # Read in one block/unit (one char, followed by a number, followed by a space). Then, update ciphertext
            next_space_index = ciphertext.find(" ", ciphertext_index + 1)
            char = ciphertext[ciphertext_index]
            num_to_reach = int(ciphertext[ciphertext_index + 1: next_space_index], 10)
            ciphertext_index = next_space_index + 1



            # Get important variables
            cipher_val = misc.ord_adjusted(char)                  # The unicode value for the current ciphertext char
            key_val    = misc.ord_adjusted(key[key_index])        # Figure out the unicode value of the key character
            key_index  = (key_index + 1) % len(key)               # Update the key_index


            # Find the original plain char by taking all possibilities and multiplying with key_val for a match
            overlap_counter = 0
            plain_char = "\0"
            for i in range(0, 1114112):

                # If overlap(count has not yet reached number)
                if pow(i, key_val, Cipher.ALPHABETS.get(self.char_set)) == cipher_val:
                    if overlap_counter != num_to_reach:           # Not at the right plaintext char yet
                        overlap_counter += 1
                        continue
                    else:                                         # At the right plaintext char
                        break

            # Add plain char to plaintext
            plaintext += plain_char

        # Return none
        return None





    # Write to the file about the statistics of the file (Call super-method)
    def write_statistics(self, file_path:str) -> None:
        """
        Write statistics

        :param file_path:   (str)  The file to write the statistics in
        :return:            (None)
        """

        super().write_statistics_in_file(file_path, {})