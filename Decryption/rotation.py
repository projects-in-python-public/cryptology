import miscellaneous

# Cipher info:
alphabet = miscellaneous.char_sets
cipher_type = "symmetric"
key_size = "single character"








# Decrypt using user-entered info. Write relevant information and return decrypted text for cryptography_runner
def execute(data, output_location):
    """
    This function decrypts data using a user-provided key.

    :param data: (string) the data to be decrypted
    :param output_location: (string) the location to write out relevant info and statistics
    :return: (string) the decrypted data
    """


    # Decrypt the ciphertext. Write the plaintext and info to a file
    miscellaneous.execute_encryption_or_decryption(data, output_location, "Decryption", "rotation", "decrypt")




# Figure out the encryption and decryption code. Pass info to miscellaneous' testing_execute function
def testing_execute(encryption, decryption, plaintext, encryption_key, char_set_size, output_location):
    """
    Conducts a rotation decryption in testing mode

    :param encryption: (string) the name of the encryption cipher to use
    :param decryption: (string) the name of the decryption cipher to use (this)
    :param plaintext: (string) the plaintext to encrypt
    :param encryption_key: (string) the key to use to encrypt
    :param char_set_size: (int) the size of the character set to use
    :param output_location: (string) the name of the file to write statistics in
    :return: None
    """


    # Encryption code
    encryption_code = miscellaneous.general_encryption_code

    # Decryption code
    decryption_code = miscellaneous.general_decryption_code

    miscellaneous.testing_execute_encryption_and_decryption(encryption, decryption,
                                                            plaintext, encryption_key, char_set_size,
                                                            output_location,
                                                            "Rotation",
                                                            encryption_code, decryption_code)







# Returns string. This is the actual algorithm to decrypt
def decrypt(ciphertext, key, char_set_size):
    """
    This function decrypts the ciphertext using the set of unicode characters from 0 to end_char.

    :param ciphertext: (string )the text to be encrypted
    :param key: (string) the key with which the encryption is done
    :param char_set_size: (int) The number of characters in the character set
    :return: (string) the encrypted text
    """

    encrypted = "" # the string to build up the encrypted text
    key_index = 0 # the index in the key we are using for the vigenere encrypt


    for x in ciphertext:
        #  figure out the unicode value for the current character
        uni_val_cipher = ord(x)

        #  figure out the unicode value for the right character in the key. THen, update key_index for next iteratio
        uni_val_key = ord(key[key_index])
        key_index = (key_index + 1) % len(key)


        #  figure out the character by subtracting the two ascii's, the add it to the encrypted string
        encrypted_char = chr((uni_val_cipher - uni_val_key) % (char_set_size))
        encrypted = encrypted + encrypted_char



    return encrypted


