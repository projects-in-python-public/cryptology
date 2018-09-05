from Cryptography.Ciphers._cipher             import Cipher     # For abstract superclass
from Cryptography.Ciphers.rotation             import Rotation  # For Rotation class
from Cryptography                 import misc                   # For miscellaneous functions



class RotationUnknown(Rotation):

    # Cipher info:
    CIPHER_NAME         = "Rotation without Given Key"
    CHAR_SET            = "alphabet"
    CIPHER_TYPE         = "symmetric"
    KEY_TYPE            = "calculated single character"

    # Block cipher info
    IS_BLOCK_CIPHER      = False
    VARIABLE_BLOCK_SIZE  = False
    DEFAULT_BLOCK_SIZE   = 0
    AUTO_TEST_BLOCK_SIZE = 0

    VARIABLE_KEY_SIZE    = False
    DEFAULT_KEY_SIZE     = 0
    AUTO_TEST_KEY_SIZE   = 0

    # Restrictions
    RESTRICT_ALPHABET   = True
    NEEDS_ENGLISH       = True


    # Constructor
    def __init__(self, plaintext:str, ciphertext:str, char_set:str, mode_of_op:str, key:str, public_key:str,
                    private_key:str, block_size:int, key_size:int, source_location:str, output_location:str) -> None:

        super().__init__(plaintext,   ciphertext,     char_set,     "",                    key,     "",
                    "",              0,              0,            source_location,     output_location    )

        # The percent of the decrypted text that is in English
        self.percent_english = 0


    # Should only be called with tests
    @misc.store_time_in("self.encrypt_time_overall", "self.encrypt_time_for_algorithm")
    def encrypt_plaintext(self) -> None:
        """
        This is the same thing as rotation's encrypt.

        :return:          (None)
        """

        # Same exact thing as Rotation's.
        Rotation.encrypt_plaintext(self)


        # Return none
        return None


    # Algorithm to decrypt plaintext
    @misc.store_time_in("self.decrypt_time_overall", "self.decrypt_time_for_algorithm")
    def decrypt_ciphertext(self) -> None:
        """
        In order to decrypt, decrypt with rotation with random unicode values to see if the result is in English. For
        this to work, the plaintext must be in mostly English. The "random" unicode values are tested starting from 0 to
        the maximum unicode value.

        :return:           (None)
        """

        # Parameters for decryption
        ciphertext = self.ciphertext
        key        = self.key
        alphabet   = self.char_set



        # Try to decrypt the ciphertext using every single unicode value
        for key_val in range(0, Cipher.ALPHABETS.get("unicode")):

            # Set the key and proceed to decrypt (temporarily disable printing)
            self.key = misc.chr_adjusted(key_val)                                # Get key for correctness
            misc.disable_print()
            Rotation.decrypt_ciphertext(self)                                    # Decrypt
            misc.enable_print()

            # Assess the generated plaintext for correctness (English)
            is_english, self.percent_english = misc.is_english_bag_of_words(self.plaintext)

            # Print updates
            #print("Done with: {}\tPercent English: {}%"
            #      .format(repr(misc.chr_adjusted(key_val)),
            #              format(self.percent_english * 100, ".2f") ))
            print("{:27}{}"
                  .format("Done with: {}{}{}".format("\u001b[32m", repr(misc.chr_adjusted(key_val)), "\u001b[0m"),
                          "Percent English: {}{}%{}".format("\u001b[32m",
                                                            format(self.percent_english * 100, ".2f"),
                                                            "\u001b[0m")))


            # If correct, then break out of the loop and return
            if is_english is True:
                break




        # Fill in self's plaintext and the key
        self.plaintext       = self.plaintext
        self.key             = self.key
        self.percent_english = self.percent_english


        # Return none
        return None



    # Write to the file about the statistics of the file (Call super-method)
    def write_statistics(self, file_path:str, leave_empty={}) -> None:
        """
        Write statistics.

        :param file_path:   (str)  The file to write the statistics in
        :param leave_empty: (dict) Exists to match superclass method
        :return:            (None)
        """

        extra_lines = {}

        extra_lines[22] = "Microseconds per rotation: {}(µs)".format(format(self.decrypt_time_for_algorithm
                                                                  / misc.ord_adjusted(self.key)* 1000000, ".12f")[0:14])
        extra_lines[23] = "Percent of text in English: {}".format("{:.2%}".format(self.percent_english))





        Cipher.write_statistics(self, file_path, extra_lines)
