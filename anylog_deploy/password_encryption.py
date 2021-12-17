import os
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

    def __read_file(self)->bytes:
        """
        Read content in self.config_file_path
        :params:
            output:bytes - content in self.config_file
        :return:
            output
        """
        output = ""
        if os.path.isfile(self.config_file_path):
            try:
                with open(self.config_file_path, 'rb') as f:
                    try:
                        output = f.read()
                    except Exception as e:
                        print("Failed to read content in '%s' (Error: %s)" % (self.config_file_path, e))
            except Exception as e:
                print("Failed to open '%s' (Error: %s)" % (self.config_file_path, e))
        return output

    def create_keys(self)->bool:
        """
        Generate encryption key and store in self.config_file_path
        :params:
            status:bool
            key:bytes - encryption key
        :return:
            status
        """
        status = True
        try:
            key = Fernet.generate_key()
        except Exception as e:
            print("Failed to generate key (Error: %s)" % e)
            status = False

        if status is True:
            try:
                with open(self.config_file_path, 'wb') as f:
                    try:
                        f.write(key)
                    except Exception as e:
                        print("Failed to write encryption key into file '%s' (Error: %s)" % (self.config_file_path, e))
                        status = False
            except Exception as e:
                print("Failed to open file '%s' (Error: %s)" % (self.config_file_path, e))
                status = False

        return status

    def encrypt_string(self, value:str)->str:
        """
        Using the self.config_file_path encrypt a given value
        :args:
            value:str - string to encrypt
        :params:
            status:bool
            key:bytes - encryption key
            encrypted_value:str - encrypted string
        :return:
            encrypted valued
        """
        status = True
        key = self.__read_file()
        encrypted_value = value
        try:
            fernet = Fernet(key)
        except Exception as e:
            print("Failed to initiate the Fernet class (Error: %s)" % e)
            status = False

        if status is True:
            try:
                encrypted_value = fernet.encrypt(value.encode()).decode()
            except Exception as e:
                print("Failed to encrypt given value (Error %s)" % e)

        return encrypted_value

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

