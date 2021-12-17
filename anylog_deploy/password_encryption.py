import os
import time

from cryptography.fernet import Fernet


class EncryptPasswords:
    def __init__(self):
        """
        The following class is intended to provide support for encrypting password credentials
        :based on:
            https://www.geeksforgeeks.org/how-to-encrypt-and-decrypt-strings-in-python/
        :params:
            config_dir_path:str - path that'll contain public and private keys
            self.config_file_path:str - path for encryption key file
        """
        config_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys')
        if not os.path.isdir(config_dir_path):
            os.makedirs(config_dir_path)
        self.config_file_path = os.path.join(config_dir_path, 'encryption_key.txt')

    def __read_file(self)->(bytes, str):
        """
        Read content in self.config_file_path
        :params:
            output:bytes - content in self.config_file
            error_msg:str - if fails, generated error message
        :return:
            output, error_msg
        """
        output = ""
        error_msg = None
        if os.path.isfile(self.config_file_path):
            try:
                with open(self.config_file_path, 'rb') as f:
                    try:
                        output = f.read()
                    except Exception as e:
                        error_msg = "Failed to read content in '%s' (Error: %s)" % (self.config_file_path, e)
            except Exception as e:
                error_msg = "Failed to open '%s' (Error: %s)" % (self.config_file_path, e)

        return output, error_msg

    def create_keys(self)->str:
        """
        Generate encryption key and store in self.config_file_path
        :params:
            key:bytes - encryption key
            error_msg:str - if fails, generated error message
        :return:
            error_msg
        """
        error_msg = None
        try:
            key = Fernet.generate_key()
        except Exception as e:
            error_msg = "Failed to generate key (Error: %s)" % e

        if error_msg is None:
            try:
                with open(self.config_file_path, 'wb') as f:
                    try:
                        f.write(key)
                    except Exception as e:
                        error_msg = "Failed to write encryption key into file '%s' (Error: %s)" % (self.config_file_path, e)
            except Exception as e:
                error_msg = "Failed to open file '%s' (Error: %s)" % (self.config_file_path, e)

        return error_msg

    def encrypt_string(self, value:str)->(str, str):
        """
        Using the self.config_file_path encrypt a given value
        :args:
            value:str - string to encrypt
        :params:
            key:bytes - encryption key
            encrypted_value:str - encrypted string
            error_msg:str - if fails, generated error message
        :return:
            encrypted valued & error message
        """
        status = True
        key, error_message = self.__read_file()
        if error_message is not None:
            return "", error_message
        encrypted_value = value
        try:
            fernet = Fernet(key)
        except Exception as e:
            error_message = "Failed to initiate the Fernet class (Error: %s)" % e

        if error_message is None:
            try:
                encrypted_value = fernet.encrypt(value.encode()).decode()
            except Exception as e:
                error_message = "Failed to encrypt given value (Error %s)" % e

        return encrypted_value, error_message

    def decrypt_string(self, encrypted_value:str)->str:
        status = True
        key = self.__read_file()
        value = encrypted_value

        try:
            fernet = Fernet(key)
        except Exception as e:
            print("Failed to initiate the Fernet class (Error: %s)" % e)
            status = False

        if status is True:
            try:
                value = fernet.decrypt(encrypted_value.encode()).decode()
            except Exception as e:
                print("Failed to decrypt given value (Error %s)" % e)

        return value

