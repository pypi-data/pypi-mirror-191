import argparse
import os 
import shutil
import hashlib
import time
import datetime


"""sync2folders - Synchronizes two folders: source and replica.

    Author: Ivan Santos
    
    This module provides synchronisation process methods for synchronizing two folders: source and replica.
    sync2folders maintains a full, identical copy of source folder at replica folder. It implements the following features:
    - synchronisation is one-way: after the synchronisation content of the replica folder is modified to exactly match content of the source folder;
    - synchronisation is performed periodically;
    - File creation/copying/removal operations are logged to a file and to the console output;
    - Folder paths, synchronisation interval and log file path are provided using the command line arguments;

    This file can also be imported as a module and contains the following functions:
        * check_path_replica_folder - checks if the replica folder path exists
        * check_path_source_folder - checks if the source folder path exists
        * copyFile - copies a file from source folder to replica folder
        * createFile - creates a file in replica folder
        * deleteFile - deletes a file from replica folder
        * deleteFolder - deletes a folder from replica folder
        * getFileHash - gets the hash of a file
        * getFileSize - gets the size of a file
        * getFileStamp - gets the stamp of a file
        * saveLogs - saves logs to a file and to the console output
        * syncFile - synchronizes a file
        * syncFolder - synchronizes a folder
        * main - the main function of the script
"""
def main():
    parser = argparse.ArgumentParser(description='Synchronizes two folders: source and replica')
    parser.add_argument('-s', '--source', help='Source folder path', type=str, required=True)
    parser.add_argument('-r', '--replica', help='Replica folder path', type=str, required=True)
    parser.add_argument('-p', '--period', help='Period of time in seconds between each synchronisation', type=int, required=True)
    parser.add_argument('-l', '--logs', help='Logs file path', type=str, required=True)
    args = parser.parse_args()
    synchronisation(args.source, args.replica, args.period, args.logs)

def synchronisation(source_folder_path: str, replica_folder_path: str, period: int, logs_path: str):
    '''
    synchronisation: starts the synchronisation process and calls the necessary methods.
    
    Args:
        source_folder_path (string): source folder path.
        replica_folder_path (string): replica folder path.
        period (int): period of time in seconds between each synchronisation.
        logs_path (string): logs file path.
    
    Return:
        Synchronized two folders: source and replica. Raises an exception if the source folder path is not a folder. 
    '''

    check_path_source_folder(source_folder_path)
    check_path_replica_folder(source_folder_path, replica_folder_path, logs_path)

    if os.path.isdir(source_folder_path):
        while True:
            syncFolder(source_folder_path, replica_folder_path, logs_path)
            time.sleep(period)
    else:
        raise Exception('#ERROR#: {} IS NOT A FOLDER!'.format(source_folder_path))


def syncFolder(source_folder_path: str, replica_folder_path: str, logs_path: str):
    """
    syncFolder: synchronizes two folders: source and replica.

    Args:
        source_folder_path (string): source folder path.
        replica_folder_path (string): replica folder path.
        logs_path (string): logs file path.
    
    Raises an exception if the source folder path is not a folder or a file.

    """

    for item in os.listdir(replica_folder_path):
        source_folder_item_path = os.path.join(source_folder_path, item)
        replica_folder_item_path = os.path.join(replica_folder_path, item)

        if os.path.isdir(replica_folder_item_path):
            if not os.path.exists(source_folder_item_path):
                deleteFolder(replica_folder_item_path, logs_path)
        if os.path.isfile(replica_folder_item_path):
            if not os.path.exists(source_folder_item_path):
                deleteFile(replica_folder_item_path, logs_path)

    for item in os.listdir(source_folder_path):
        source_folder_item_path = os.path.join(source_folder_path, item)
        replica_folder_item_path = os.path.join(replica_folder_path, item)

        if os.path.isdir(source_folder_item_path):

            if not os.path.exists(replica_folder_item_path):
                os.mkdir(replica_folder_item_path)
            elif os.path.isfile(replica_folder_item_path):
                os.remove(replica_folder_item_path)

            syncFolder(source_folder_item_path, replica_folder_item_path, logs_path)
        elif os.path.isfile(source_folder_item_path):

            if os.path.exists(replica_folder_item_path):
                if os.path.isdir(replica_folder_item_path):
                    os.removedirs(replica_folder_item_path)

            syncFile(source_folder_item_path, replica_folder_item_path, logs_path)
        else:
            raise Exception('#ERROR#: {} IS NEITHER A FILE NOR A FOLDER!'.
                            format(source_folder_item_path))

def syncFile(source_file_path: str, replica_file_path: str, logs_path: str):
    """
    syncFile: synchronizes two files and logs the operations performed to log file and console output.

    Args:
        source_file_path (string): source file path.
        replica_file_path (string): replica file path.
        logs_path (string): logs file path.
    
    """
    sourceFileTime = getFileStamp(source_file_path)
    
    if not os.path.exists(replica_file_path):
        createFile(source_file_path, replica_file_path, logs_path, sourceFileTime)
        return
    
    replicaFileTime = getFileStamp(replica_file_path)
    
    sourceFileSize = getFileSize(source_file_path)
    replicaFileSize = getFileSize(replica_file_path)
    
    sourceFileHash = getFileHash(source_file_path)
    replicaFileHash = getFileHash(replica_file_path)

    if (sourceFileTime != replicaFileTime
            or sourceFileSize != replicaFileSize or sourceFileHash != replicaFileHash):
        copyFile(source_file_path, replica_file_path, logs_path, sourceFileTime)
        return

def check_path_source_folder(source_folder_path: str):
    """
    check_path_source_folder: checks if the source folder path is valid.

    Args:
        source_folder_path (string): source folder path.

    Raises an exception if the source folder path is not valid.
    """
    if not os.path.exists(source_folder_path):
        raise Exception('#ERROR#: {} NOT EXISTS!'.format(source_folder_path))

def check_path_replica_folder(source_folder_path: str, replica_folder_path: str, logs_path: str):
    """
    check_path_replica_folder: checks if the replica folder path is valid and creates a new folder if it does not exist. Calls the saveLogs method to log the operation performed.

    Args:
        source_folder_path (string): source folder path.
        replica_folder_path (string): replica folder path.
        logs_path (string): logs file path.

    Raises an exception if the replica folder path is not valid.
    """
    if not os.path.exists(replica_folder_path):
        new_dir = input('WARNING! {} not exists, do you want to make a new dir? yes(y) or exit(n): '.format(replica_folder_path)).strip()
        while len(new_dir) < 1:
            new_dir = input('WARNING! {} not exists, do you want to make a new dir? yes(y) or exit(n): '.format(replica_folder_path)).strip()

        if new_dir == 'y' or new_dir == 'yes':
            os.mkdir(replica_folder_path)
            saveLogs(datetime.datetime.now(), 'CREATE', source_folder_path, replica_folder_path, path=logs_path)
        else:
            print('Thanks for your visit!')
            time.sleep(2)
            os._exit(os.X_OK)

def getFileStamp(file: str) -> float:
    """
    getFileTime: gets the file last modification time.

    Args:
        file (string): file path.

    Return:
        Returns the file last modification time.
    """
    return os.path.getmtime(file)

def getFileSize(file: str) -> int:
    """
    getFileSize: gets the file size.

    Args:
        file (string): file path.

    Return:
        Returns the file size.
    """
    return os.path.getsize(file)

def getFileHash(file: str) -> str:
    """
    getFileHash: gets the file hash using md5 algorithm.

    Args:
        file (string): file path.

    Return:
        Returns the file hash.
    """
    return hashlib.md5(open(file,'rb').read()).hexdigest()

def deleteFolder(replica: str, logs_path: str):
    """
    deleteFolder: delete a folder and its content, and call the method to record the action performed in the logs.

    Args:
        replica (string): replica folder path.
        logs_path (string): logs file path.
    
    """
    os.rmdir(replica)
    saveLogs(datetime.datetime.now(), 'DELETE', replica=replica, path=logs_path)

def deleteFile(replica: str, logs_path: str):
    """
    deleteFile: delete a file and call the method to record the action performed in the logs.

    Args:
        replica (string): replica file path.
        logs_path (string): logs file path.
    
    """
    os.remove(replica)
    saveLogs(datetime.datetime.now(), 'DELETE', replica=replica, path=logs_path)

def createFile(source: str, replica: str, logs_path: str, src_modifitcationTime: float):
    """
    createFile: create a file from source to replica and call the method to record the action performed in the logs.
    Args:
        source (string): source file path.
        replica (string): replica file path.
        logs_path (string): logs file path.
        src_modifitcationTime (string): source file modification time.

    """
    if not os.path.exists(os.path.dirname(replica)):
        os.makedirs(os.path.dirname(replica))
    shutil.copy(source, replica)
    os.utime(replica, (datetime.datetime.now().timestamp(), src_modifitcationTime))
    saveLogs(datetime.datetime.now(), 'CREATE', source, replica, path=logs_path)

def copyFile(source: str, replica: str, logs_path: str, src_modifitcationTime: float):
    """
    copyFile: copy a file from source to replica and call the method to record the action performed in the logs.

    Args:
        source (string): source file path.
        replica (string): replica file path.
        logs_path (string): logs file path.
        src_modifitcationTime (string): source file modification time.

    """
    if not os.path.exists(os.path.dirname(replica)):
        os.makedirs(os.path.dirname(replica))
    shutil.copy(source, replica)
    os.utime(replica, (datetime.datetime.now().timestamp(), src_modifitcationTime))
    saveLogs(datetime.datetime.now(), 'COPY', source, replica, path=logs_path)

def saveLogs(timestamp: str, action: str, source=None, replica=None, user='ADMIN', path='logs/logs.txt'):
    """
    saveLogs: save logs in a file in the logs folder and print to the consolte the action performed.

    Args:
        timestamp (string): timestamp of the action.
        action (string): action to take. Can be: COPY, DELETE, CREATE.
        source (string): source file path.
        replica (string): replica file path.
        user (string): user.
        path (string): logs file path.

    """
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path))
    if action == 'DELETE':
        message = 'Timestamp: {} | Action: {} | From: {} | User: {} |'.format(timestamp, action, replica.replace("\\", "/" ), user)
    elif action == 'COPY':
        message = 'Timestamp: {} | Action: {} | From: {} | To: {} | User: {} |'.format(timestamp, action, source.replace("\\", "/" ), replica.replace("\\", "/" ), user)
    elif action == 'CREATE':
        message = 'Timestamp: {} | Action: {} | From: {} | To: {} | User: {} |'.format(timestamp, action, source.replace("\\", "/" ), replica.replace("\\", "/" ), user)
    with open(path, 'a') as f:
        f.write(message)
        f.write('\n')
    print("\n")
    print(message)
    print("\n")

if __name__ == "__main__":
    main()
