from Cryptography.Ciphers._cipher             import Cipher     # For abstract superclass
from Cryptography                 import misc                   # For miscellaneous functions



class VigenereMultiplicative(Cipher):

    # Cipher info:
    CIPHER_NAME         = "Vigenere using Modular Multiplication"
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
        This follows a similar format to vigenere, but uses modular multiplication instead of modular addition.
        However, because modular multiplication is not reversible like modular addition in a very straightforward
        way, I must store the number of unicode values that give the same result as the plaintext character unicode
        value when the modular multiplication is done. This is done so that the original plaintext character can be
        calculated without confusing it for other unicode values that just happen to coincide.

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

            # Print updates (every 1000 characters)
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
            encrypted_val = (plain_val * key_val) % Cipher.ALPHABETS.get(self.char_set)
            encrypted_char = misc.chr_adjusted(encrypted_val)

            # Obtain the number of overlaps that come before this one (this plain_val) and NOT including this one
            overlap_counter = 0
            for i in range(0, plain_val):
                # If it is an overlap character
                if (i * key_val) % Cipher.ALPHABETS.get(self.char_set) == encrypted_val and i != plain_val:
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
        In order to reverse the modular multiplication, I have to test unicode values by applying the modular
        multiplication with the key's unicode value to see if it matches the ciphertext value. However, because there
        may be coincidences in which unicode values which are not the original plaintext character's unicode value, I
        must take into account the number of overlaps, which was calculated during encryption. So, when I test values
        up from 0, I can stop when I reach the number of overlaps, indicating that I had reached the original value.

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

            # Print updates (every 1000 characters)
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
                if (i * key_val) % Cipher.ALPHABETS.get(self.char_set) == cipher_val:
                    if overlap_counter != num_to_reach:                # Not at right plaintext char yet
                        overlap_counter += 1
                        continue
                    else:                                              # At the right plaintext char
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
