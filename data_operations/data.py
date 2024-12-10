import csv
import os
from typing import List, Dict

from paramiko import SSHClient, AutoAddPolicy, RSAKey, Ed25519Key
from scp import SCPClient


class FileTransfer:
    def __init__(self, name, surname, file_path, save_path=None):
        self.__ed_key = self.__load_ed_key()
        self.__connection_credentials = self.__load_credentials()
        self.__default_save_path = self.__load_default_save_path()

        self.__ssh = SSHClient()
        self.__connection_established = False

        self.__host = self.__connection_credentials["host"].strip()
        self.__username = self.__connection_credentials["username"].strip()

        if save_path is not None:
            self.__save_path = save_path.strip()
        else:
            self.__save_path = self.__default_save_path["path"].strip()

        self.__temp_dir = self.__save_path + "/tmp/"

        # create a dir with user name and surname
        self.__user_dir = self.__save_path + f"/{name}_{surname}/"

        if file_path is not None:
            self.__file_path = file_path.strip()
        else:
            self.__file_path = ""

        self.__number_of_files = 1
        if os.path.isdir(self.__file_path):
            self.__number_of_files = len(os.listdir(self.__file_path))

    @classmethod
    def __load_ed_key(cls) -> Ed25519Key:
        """
        Load the RSA key from the specified file.

        :return: The loaded RSA key.
        :raises ValueError: If failed to load the RSA key.
        """
        try:
            with open("./resources/ssh_info/id_ed25519") as key_file:
                return Ed25519Key.from_private_key(key_file)
        except Exception as e:
            raise ValueError(f"Failed to load RSA key: {e}")

    @classmethod
    def __load_credentials(cls) -> str:
        """
        Load SSH credentials from credentials.csv file.

        :return: A dictionary containing the host and username from the credentials.csv file.
        :raises ValueError: If there is an error loading the SSH credentials.
        """
        try:
            with open("./resources/ssh_info/credentials.csv") as credentials_file:
                reader = csv.DictReader(credentials_file, fieldnames=["host", "username"])
                return next(reader)
        except Exception as e:
            raise ValueError(f"Failed to load SSH credentials: {e}")

    @classmethod
    def __load_default_save_path(cls) -> str:
        """
        Load the default save path from a CSV file.

        :return: The default save path.
        :raises ValueError: If the default save path fails to load.
        """
        try:
            with open("./resources/ssh_info/default_save_path.csv") as default_save:
                reader = csv.DictReader(default_save, fieldnames=["path"])
                return next(reader)
        except Exception as e:
            raise ValueError(f"Failed to load Default Save Path: {e}")

    def __getattr__(self, attr):
        match attr:
            case 'number_of_files':
                return self.__number_of_files
        raise AttributeError(f'{self.__class__.__name__} object has no attribute {attr}')

    def __connect(self) -> None:
        """
        Connects to the server using SSH.

        :return: None
        :raises ConnectionError: if the connection to the server fails
        """
        try:
            self.__ssh.set_missing_host_key_policy(AutoAddPolicy())
            self.__ssh.connect(hostname=self.__host, username=self.__username, pkey=self.__ed_key)
            self.__connection_established = True
        except Exception as e:
            raise ConnectionError(f"Could not connect to the server: {e}")

    def __find_existing_files(self) -> (bool, List):

        """
        TODO: Please chnage the behaviour of the function to just check weather the directory
              with the persona's name and surname already exists.
        """
        if not self.__connection_established:
            try:
                self.__connect()
            except ConnectionError:
                return False

        try:
            sftp = self.__ssh.open_sftp()

            if os.path.isdir(self.__file_path):
                existing_files = []
                for y in os.listdir(self.__file_path):
                    file = os.path.join(self.__save_path, y)
                    linux_path = file.replace('\\', '/')
                    try:
                        sftp.stat(linux_path)
                        existing_files.append(y)
                    except IOError:
                        # if sftp.stat() throws an exception the file does not exist, so we continue checking
                        continue

                if len(existing_files) == 0:
                    return False, None
                else:
                    return True, existing_files
            else:
                try:
                    file_name = os.path.basename(self.__file_path)
                    file = os.path.join(self.__save_path, file_name)
                    linux_path = file.replace('\\', '/')
                    sftp.stat(linux_path)
                    return True, [file_name]
                except IOError:
                    # if sftp.stat() throws an exception the file does not exist
                    return False, None

        except ConnectionError:
            raise ConnectionError("Could not connect to the server to check if file exists")

    def file_transfer(self) -> (bool, Dict):
        """
        Transfer files from local machine to a remote server. It also automatically registers images in the
        ImageIndex DB. It keeps track of the IDs by storing them locally in the class variable, and it also
        logs the IDs to .log file in `logs/image_index.log`

        :return: A tuple containing a boolean indicating whether the transfer was successful or not,
                 and a dictionary with information about any existing files on the server.
        """
        if not self.__connection_established:
            try:
                self.__connect()
            except ConnectionError:
                return False

        existing_files = []
        try:
            exists, existing_files = self.__find_existing_files()
            if exists:
                raise IOError("Some of the files already exist on the server")
        except ConnectionError:
            return False
        except IOError:
            return False, {"existing_files": existing_files}

        try:
            # make a temporary directory which used for rollback functionality
            # the tmp directory is created inside the  __save_path directory
            self.__ssh.exec_command(f"mkdir {self.__temp_dir}")
            self.__ssh.exec_command(f"mkdir {self.__user_dir}")
            scp = SCPClient(self.__ssh.get_transport())
            if os.path.isdir(self.__file_path):
                for x in os.listdir(self.__file_path):
                    # transfer image to the server via SSH
                    file = os.path.join(self.__file_path, x)
                    scp.put(file, recursive=False, remote_path=self.__temp_dir)
            else:
                # transfer image to the server via SSH
                scp.put(self.__file_path, recursive=False, remote_path=self.__temp_dir)

            scp.close()
            # if transfer was fine and not aborted unpack the files to the main __save_path
            self.__unpack_temp_dir()
            self.__remove_temp_dir()
            return True
        except Exception:
            self.__remove_temp_dir()
            return False

    def __remove_temp_dir(self) -> None:
        """
        Remove the temporary directory on the server.

        :return: None
        """
        self.__ssh.exec_command(f"rm -rf {self.__temp_dir}")

    def __remove_user_dir(self) -> None:
        self.__ssh.exec_command(f"rm -rf {self.__user_dir}")

    def __unpack_temp_dir(self) -> None:
        """
        Unpacks the contents of a temporary directory to a specified save path.

        :return: None
        """
        self.__ssh.exec_command(f"mv {self.__temp_dir}/* {self.__user_dir}")


    # def delete_file(self, resource: str, id_to_be_deleted: int) -> bool:
    #     """
    #     Delete a file from the specified path(resource). It also deletes a pointer to the resource form ImageIndex DB.
    #
    #     :param resource: The resource path of the file.
    #     :param id_to_be_deleted: The ID of the file to be deleted.
    #     :return: True if the file is successfully deleted, False otherwise.
    #     :raises UserWarning: If authentication is required before continuing.
    #     :raises Exception: If an error occurs while deleting the file.
    #     """
    #     if not self.__connection_established:
    #         try:
    #             self.__connect()
    #         except ConnectionError:
    #             return False
    #
    #     if self.__auth_payload is None:
    #         raise UserWarning("Please login with Google before continuing.")
    #
    #     try:
    #         file_name = os.path.basename(resource)
    #         file = os.path.join(self.__save_path, file_name)
    #         linux_path = file.replace('\\', '/')
    #         self.__ssh.exec_command(f"rm {linux_path}")
    #         # delete image from image index
    #         self.__transfer.delete_image_index(id_to_be_deleted)
    #
    #         return True
    #     except Exception as e:
    #         raise e

    def abort(self) -> bool:
        """
        Close the connection and abort the operation.

        :return: True if the connection was successfully closed, False otherwise.
        """
        if self.__connection_established:
            try:
                self.__remove_temp_dir()
                self.__remove_user_dir()
                self.__ssh.close()
                self.__connection_established = False
                return True
            except ConnectionResetError:
                return False

    def close_connection(self) -> bool:
        """
        Closes the connection.

        :return: True if the connection is successfully closed, False otherwise.
        """
        try:
            self.__ssh.close()
            self.__connection_established = False
            return True
        except ConnectionResetError:
            return False
