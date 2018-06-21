import miscellaneous # To handle user input and miscellaneous









# Encrypt using user-entered info. Write relevant information and return encrypted text for cryptography_runner
def execute(data, output_location):
    """
    This function asks the user for more information to conduct the cipher. Then it encrypt the information using the
    encrypt function located below. Finally, it returns the encrypted data back to cryptography_runner

    :param data: (string) the data to be encrypted
    :param output_location: (string) the location to print out the information
    :return: (string) the encrypted data
    """

    # Obtain the encrypted text. Also write statistics and relevant info a file
    encrypted = miscellaneous.encrypt_or_decrypt_with_single_char_key(data, output_location,
                                                                      "Encryption", "rotation", "encrypt")


    # Return encrypted text to be written in cryptography_runner
    return encrypted



# This function contains the actual algorithm to encrypt in a rotation cipher using a key
def encrypt(plain_text, key, num_chars):
    """
    This function encrypts the plain text using the set of unicode characters from 0 to end_char.

    :param plain_text: (string )the text to be encrypted
    :param key: (string) the key with which the encryption is done
    :param num_chars: (int) The number of characters in the character set
    :return: (string) the encrypted text
    """

    encrypted = "" # the string to build up the encrypted text
    key_index = 0 # the index in the key we are using for the vigenere encrypt


    for x in plain_text:
        #  figure out the unicode value for the current character
        uni_val_plain = ord(x)

        #  figure out the unicode value for the right character in the key
        key_char = key[key_index]
        uni_val_key = ord(key_char)


        #  figure out the character by combining the two ascii's, the add it to the encrypted string
        encrypted_char = chr((uni_val_plain + uni_val_key) % (num_chars))
        encrypted = encrypted + encrypted_char

        # update key_index for next iteration
        key_index = (key_index + 1) % len(key)

    return encrypted






