from Cryptography import misc
from Cryptography import test                                 # for manual/automatic testing


import datetime # to be used in fileName
import os # to delete files in decrypted and encrypted









last = "" # Store the path to the last created encrypted file



###################################################################################### START OF MAIN FUNCTION ##########
def main():


    #  Print out info when the program first begins
    global last
    if last == "":
        print()
        print("See README for usage."
              + "\nTo print out the available cipher types, type \"help\".")
        print()
        usage()


    # forever while loop to continually take in user input and executing commands
    while True:

        # Obtain information from the user command
        cipher, encrypt, data, output_location = parse_user_input()

        # Set up the global variable last for next iteration
        last = output_location

        # print out the data, and let the user know where the output location is
        print_data_and_location( data, output_location )

        # execute the encryption/decryption on the data
        execute_encryption_or_decryption( encrypt, cipher, data, output_location )

    # End of forever while loop
######################################################################################## END OF MAIN FUNCTION ##########


# Print out available Encryption/Decryption types
def usage():
    print("ENCRYPTION/DECRYPTION TYPES AVAILABLE: ")
    print("Available for both encryption and decryption: ", end = "")
    print(*(misc.ENCRYPTION_SET & misc.DECRYPTION_SET), sep=", ")
    print("Available for decryption only: ", end = "")
    print(*(misc.DECRYPTION_SET - misc.ENCRYPTION_SET), sep=", ")
    print()


# Parse user input and return relevant information
def parse_user_input():
    """
    This function parses user input and returns relevant information.
    User input is unix-like, with: command [options] (argument) <optional argument>
        encrypt (cipher) (plaintext_file_path*) <output_file_path>
        decrypt (cipher) (ciphertext_file_path) <output_file_path>
        test    [options] <cipher>
        help
        exit
        database TODO

    * File paths with spaces in the name must be escaped with "\ ".
    So the path:     Resources/Library/Space File.txt
    is typed out as: Resources/Library/Space\ File.txt

    :return: cipher           (string) stores the cipher type that the user wants to use
    :return: encrypt          (boolean) decides whether encryption or decryption is used
    :return: data             (string) the information to be encrypted/decrypted
    :return: output_location  (string) the output location of the generated file
    """

    # Variables to return
    cipher          = ""      # The name of the cipher to use
    encrypt_mode    = True    # Whether I am in encrypt mode or in decrypt mode
    data            = ""      # The string of the input. Either plaintext or ciphertext
    output_location = ""      # The file path to store the output of encryption/decryption





    statement = input("Enter statement: ")                # Obtain the user input


    # Return only when the statements are "encrypt" or "decrypt". Otherwise, keep looping when handling other commands.
    while True:


        # Read command (the first word)
        if statement.find(" ") != -1:                                      # If multiple words
            command = statement[0 : statement.find(" ")]
        else:
            command = statement                                            # Else, statement is the word

        # Handle command: help
        if command == "help":

            usage()                                                     # Print helpful info
            statement = input("Enter statement: ")                      # Obtain user input for next iteration
            continue                                                    # Jump to next iteration

        # Handle command: clear
        if command == "clear":

            # delete files in /Files_Decrypted
            for file in os.listdir("Resources/Files_Decrypted"):
                    os.unlink("Resources/Files_Decrypted/" + file)
            # delete files in /Files_Encrypted
            for file in os.listdir("Resources/Files_Encrypted"):
                    os.unlink("Resources/Files_Encrypted/" + file)
            # Obtain next command
            statement = input("Files deleted. Enter statement: ")        # obtain user input
            continue

        # Handle command: exit
        if command == "exit":
            print("Exiting program...")
            exit(0)

        # Handle command: test <cipher>
        if command == "test":

            prompt = ""                                                 # The prompt to return
            statement = statement.split(" ")                            # Split statement into words separated by spaces

            # There should only be two arguments total (the command + option) or (the command + optional_arg). If
            # there are more arguments than two, then return error
            if len(statement) > 2:
                extra_args = " ".join(statement)                        # List to string
                extra_args = extra_args[extra_args.find(" ",            # extra args is after second space
                                 extra_args.find(" ") + 1) + 1:]
                prompt = "Extra argument (" + extra_args + ") given! Enter another statement: "

            # If no optional arguments or flags provided, enter testing mode with no cipher provided
            if len(statement) == 1:
                test.manual_testing("")
                prompt = "Manual testing done! Enter another statement: "

            # Read for the "-a" flag for automated testing
            if statement[1] == "-a":
                test.automated_testing()
                prompt = "Automated testing done! Enter another statement: "

            # If a Decryption cipher is provided, enter manual testing and run the test on that cipher
            else:
                test.manual_testing(statement[1])
                prompt = "Manual testing done! Enter another statement: "

            statement = input(prompt)                                   # Obtain user input for next iteration
            continue                                                    # Jump to the next iteration


        # Handle command: encrypt or decrypt (cipher) (plaintext_file_path*) <output_file_path>
        if command == "encrypt" or command == "decrypt":


            # Set encrypt_mode based on command encrypt/decrypt
            if command == "decrypt": encrypt_mode = False


            # Function to split statement into list separated by spaces. (file_paths may have spaces escaped with "\ ")
            def statement_to_list(statement):
                """
                This splits a string at every space not escaped. Elements are stored into a list

                :param   (string) the string to split
                :return: (list) the split string
                """

                list_to_return = []                            # Construct the list here


                # Loop through the statement, and split when space is occurred. Ignore escaped's spaces ("\ ")
                while statement != "":

                    unescaped_space_index = -1

                    # Loop until an unescaped space is found
                    while True:

                        unescaped_space_index = statement.find(" ", unescaped_space_index + 1)    # Find space index

                        if unescaped_space_index == -1:                                           # If no more spaces
                            list_to_return.append(statement)
                            statement = ""
                            break

                        if statement[unescaped_space_index - 1] == "\\":                          # If escaped, continue
                            continue
                        else:                                                                     # Else, space found
                            break

                    # If statement is empty, just break
                    if statement == "":
                        break

                    # Replace all escaped spaces up to the unescaped_space_index with just a space
                    list_element = statement[0:unescaped_space_index]
                    list_element = list_element.replace("\ ", " ")

                    # Save the segment up to the space and cut out from var statement
                    list_to_return.append(list_element)
                    statement = statement[unescaped_space_index + 1:]

                return list_to_return
            statement_list = statement_to_list(statement)

            # If too many arguments given (>3), then print error, and jump to the next iteration
            if len(statement_list) > 1 + 3:
                statement = input("Too many arguments (more than 3) were given! Enter another statement:")
                continue


            # Read the FIRST argument (index 1), and check that it is a legitimate encrypt/decrypt cipher. If not a
            # legitimate cipher, then print error and get the user to enter another command.
            cipher = statement_list[1]
            if not ((command == "encrypt" and cipher in misc.ENCRYPTION_SET) \
                       or (command == "decrypt" and cipher in misc.DECRYPTION_SET)):     # If not legitimate cipher
                statement = input("Cipher (" + cipher + ") not recognized as "
                                  + ("an" if command == "encrypt" else "a")
                                  + " "
                                  + command
                                  + "ion cipher! Enter another statement: ")
                continue



            # Read the SECOND argument (source file path). Get data from source. If there is a failure, then print
            # error and get the user to enter another command
            input_path = statement_list[2]


            # If the input is "last", then use the data from the file path "pointed" to by last
            if input_path == "last":

                #  open the file and store its contents in the string data
                try:
                    my_file = open(last, "r", encoding="utf-8")
                    data = my_file.read()
                    my_file.close()
                except IOError:
                    statement = input("There is no last file! Try again: ")
                    continue
            # Otherwise, a source is given (NOT last)
            elif not input_path == "last":

                #  Try to open the file as is (the literal file path)
                try:
                    my_file = open(input_path, "r", encoding="utf-8")
                    data = my_file.read()
                    my_file.close()

                except IOError:  # Search within Resources/Library, Resources/Files_Encrypted...
                    try:                                                              # Search Resources/Library
                        my_file = open("Resources/Library/"
                                       + input_path, "r", encoding="utf-8")
                        data = my_file.read()
                        my_file.close()

                    except IOError:
                        try:                                                          # Search Resources/Files_Encrypted
                            my_file = open("Resources/Files_Encrypted/"
                                           + input_path, "r", encoding="utf-8")
                            data = my_file.read()
                            my_file.close()

                        except IOError:
                            try:                                                      # Search Resources/Files_Decrypted
                                my_file = open("Resources/Files_Decrypted/"
                                               + input_path, "r", encoding="utf-8")
                                data = my_file.read()
                                my_file.close()

                            except IOError:                                           # File not found
                                # File could not be found, inform the user of the error
                                statement = input("No such file or directory! Try again: ")
                                continue


                # if the input was empty, return an error
                if len(data) == 0:
                    statement = input("There is no data to process in file("
                                      + input_path + ")! Try again: ")
                    continue


            # Read the THIRD argument (output file path if it exists)
            try: output_path = statement_list[3]
            except: pass

            # If an output filepath is given, use that. Check that it could be opened or if it already exists
            if len(statement_list) == 1 + 3:
                output_location = statement_list[3]

                # See if the file already exists
                try:                                                                   # See if file already exists
                    my_file = open(output_location, "r", encoding="utf-8")
                    data = my_file.read()
                    my_file.close()
                except IOError:
                    statement = input("File (" + output_location + ") already exists."
                                      + "If you do not want to overwrite, then enter another new statement."
                                      + "Otherwise, to overwrite, press \"Enter.\" Proceed: ")
                    if not statement == "":                                            # New statement
                        continue
                    elif statement == "":                                              # User wants to overwrit, proceed
                        pass

                # See if the file is openable
                try:                                                                   # Try to open file
                    my_file = open(output_location, "w", encoding="utf-8")
                    data = my_file.read()
                    my_file.close()
                except Exception:
                    statement = input("File (" + output_location+ ") is not openable! Enter another statement: ")
                    continue
            # Output filepath not given. Use default format
            else:

                # Encrypt default format
                if command == "Encrypt":                               # Encrypt's default format
                    now = datetime.datetime.now()                      # For the time and date
                    output_location = "Resources/Files_Encrypted/" + input_path + cipher + "_encrypted_" \
                                      + now.strftime("%Y-%m-%d_h%Hm%Ms%S")

                # Decrypt default format
                else:                                                  # Decrypt's default format
                    now = datetime.datetime.now()                      # For the time and date
                    output_location = "Resources/Files_Decrypted/" + input_path + cipher + "_decrypted_" \
                                      + now.strftime("%Y-%m-%d_h%Hm%Ms%S")


            # Return all relevant variables
            return cipher, encrypt_mode, data, output_location




            # The command has not been found. Tell the user to enter another legitimate command







        # Command not recognized
        else:
            # Print out prompt
            statement = input("Command (" + command + ") not recognized! Enter another statement: ")
            continue



    """
    statement = input("Enter statement: ") # obtain user input

    # While the statement is invalid, keep prompting the user. If valid, break from loop
    while True:


        commands = statement.split() #  split the statement into an array of words


        # if no input, prompt the user to enter a statement
        if len(statement) == 0:
            statement = input("No arguments are supplied! Try again: ")
            continue




        # PROCESS THE FIRST WORD IN THE STATEMENT
        # If command is "help", print usage, and ask for another statement
        if commands[0] == "help":
            usage()
            statement = input("Enter statement: ")  # obtain user input
            continue

        # If command is "exit", then exit
        elif commands[0] == "exit":
            exit()

        # If command is "test", then enter testing mode
        elif commands[0] == "test":
            test.manual_testing()

        # If command is "-e", then set encrypt and check for the following argument
        elif commands[0] == "-e":
            encrypt = True
            #  check if there are arguments following -e and make note of it if there are none
            if len(commands) == 1:
                statement = input("No arguments are supplied! Try again: ")
                continue

        elif commands[0] == "-d":
            encrypt = False
            #  check if there are arguments following -d and make note of it if there are none
            if len(commands) == 1:
                statement = input("No arguments are supplied! Try again: ")
                continue

        elif commands[0] == "clear":
            # delete files in /Files_Decrypted
            for file in os.listdir("Resources/Files_Decrypted"):
                    os.unlink("Resources/Files_Decrypted/" + file)
            # delete files in /Files_Encrypted
            for file in os.listdir("Resources/Files_Encrypted"):
                    os.unlink("Resources/Files_Encrypted/" + file)

            # Obtain next command
            statement = input("Files deleted. Enter statement: ")  # obtain user input
            continue

        else:
            statement = input("Unrecognized command! Try again: ")
            continue








        # PROCESS THE INPUT TEXT/FILE (second part) in the statement.
        index = 1  # This is the current index for the array statement
        if commands[index] == "last":

            file_given = True # update file_given

            #  open the file and store its contents in the string data
            try:
                my_file = open(last, "r", encoding="utf-8")
                data = my_file.read()
                my_file.close()
            except IOError:
                statement = input("There is no last file! Try again: ")
                continue

            # update index
            index = index + 1

        elif commands[index][0] == "\"": # Test if a string is entered(with quotation marks)

            file_given = False # update file_given

            # Try to read the string data
            try:
                data = statement[statement.index("\"") + 1: statement.rindex("\"")]
            except ValueError:
                statement = input("The string was impromperly formatted! Try again: ")
                continue

            # update index(it should be the last one containing a quotation mark plus 1)
            for i in range(len(commands) - 1, 0, -1):
                if "\"" in commands[i]:
                    index = i + 1
                    break


        # Otherwise, a file is given
        else:

            file_given = True                           # update file_given
            file_name = commands[index]                 # The name of the file



            #  Try to open the file as is (the literal file path)
            try:
                my_file = open(file_name, "r", encoding="utf-8")
                data = my_file.read()
                my_file.close()

            except IOError: # Search within Resources/Library, Resources/Files_Encrypted, and Resources/Files_Decrypted
                try:                                                                  # Search Resources/Library
                    my_file = open("Resources/Library/" + file_name, "r", encoding="utf-8")
                    data = my_file.read()
                    my_file.close()

                except IOError:
                    try:                                                              # Search Resources/Files_Encrypted
                        my_file = open("Resources/Files_Encrypted/" + file_name, "r", encoding="utf-8")
                        data = my_file.read()
                        my_file.close()

                    except IOError:
                        try:                                                          # Search Resources/Files_Decrypted
                            my_file = open("Resources/Files_Decrypted/" + file_name, "r", encoding="utf-8")
                            data = my_file.read()
                            my_file.close()

                        except IOError:                                               # File not found
                            # File could not be found, inform the user of the error
                            statement = input("No such file or directory! Try again: ")
                            continue

            # update index
            index = index + 1

        # if the input was empty, return an error
        if len(data) == 0:
            statement = input("There is no data to process! Try again: ")
            continue
            # END OF PROCESSING DATA INPUT



        # PROCESS THE NEXT PART OF THE STATEMENT(THE CIPHER) CHECK FOR NO ARGUMENTS FIRST
        cipher = "" # create variable to hold cipher (Nothing by default)
        if index >= len(commands):
            statement = input("No cipher given! Try again: ")
            continue
        # otherwise an argument is given
        else:
            given_cipher = commands[index]

            #  make sure that the given cipher is a valid type for encryption
            if encrypt:
                if given_cipher in misc.ENCRYPTION_SET:
                        cipher = given_cipher

            # if in decryption mode, make sure a valid decryption cipher is chosen
            else:
                if given_cipher in misc.DECRYPTION_SET:
                        cipher = given_cipher

            # if there is no valid cipher, return error
            if cipher == "":
                statement = input("Cipher was invalid! Try again: ")
                continue

        index = index + 1 # update the index for parsing through commands
        # END OF PROCESSING CIPHER





        # FIGURE OUT THE LOCATION FOR THE NEW GENERATED FILE. CREATE A DEFAULT LOCATION FIRST
        now = datetime.datetime.now()
        if encrypt:
            #  if file given, use the original name of the file as part of the new name, otherwise end it in
            # encrypted.txt
            if file_given:
                try:
                    output_location = "Resources/Files_Encrypted/" + now.strftime("%Y-%m-%d_h%Hm%Ms%S") + "_" \
                                        + cipher + "_encrypted_" \
                                        + commands[1][commands[1].rindex("/") + 1:]
                except ValueError:
                    output_location = "Resources/Files_Encrypted/" + now.strftime("%Y-%m-%d_h%Hm%Ms%S") + "_" \
                                        + cipher + "_encrypted_" \
                                        + commands[1]
            else:
                output_location = "Resources/Files_Encrypted/" + now.strftime("%Y-%m-%d_h%Hm%Ms%S") \
                                    + "_" + cipher + "_encrypted"

        # else decrypt
        else:
            #  if file given, use the original name of the file as part of the new name, otherwise end it in
            # decrypted.txt
            if file_given:
                try:
                    output_location = "Resources/Files_Decrypted/" + now.strftime("%Y-%m-%d_h%Hm%Ms%S") \
                                        + "_DECRYPTED_" \
                                        + commands[1][commands[1].rindex("/") + 1:]
                except ValueError:
                    output_location = "Resources/Files_Decrypted/" + now.strftime("%Y-%m-%d_h%Hm%Ms%S") \
                                        + "_DECRYPTED_" \
                                        + commands[1]
            else:
                output_location = "Resources/Files_Decrypted/" + now.strftime("%Y-%m-%d_h%Hm%Ms%S") \
                                    + "_DECRYPTED"

        # take input for the location of the output(if there is one)
        if index < len(commands):
            output_location = commands[index]


        break # break out of forever while loop because everything ran fine

    # End of while loop to take user command

    return cipher, encrypt, data, output_location
    """



# Print data and the output location
def print_data_and_location(data, output_location):

    print("\nTHIS IS THE DATA: \n" + data)
    print("*******************************************************")
    print("\nNEW FILE LOCATED HERE: " + output_location)
    print("TYPE \"info\" FOR MORE INFORMATION ON FURTHER PROMPTS.\n")


# execute encryption/decryption on the data, save the output, and print out the output
def execute_encryption_or_decryption( encrypt, cipher, data, output_location ):


    if encrypt:
        exec("from Encryption import " + cipher)
        output = eval(cipher + ".execute(data, output_location)")
    else:
        exec("from Decryption import " + cipher)
        output = eval(cipher + ".execute(data, output_location)")










# Call the main function
if __name__ == "__main__":
    main()