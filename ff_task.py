#TEST TASK - VEEAM SOFTWARE - FABIAN ALBORNOZ

#GOAL

# I need to synchronise two folders. A SOURCE folder an a replica FOLDER. 
# If a file/folder exists in the SOURCE folder, it should also exist in the REPLICA folder.

# PROGRAMMING LANGUAGE: 
# The language I will be using is Python. It is high-level, easy to read and has a rich library.

#SYNCHRONISATION IS ONE WAY:
# Since synchronisation is from the SOURCE to the REPLICA folder only, if a file/folder exists in the REPLICA folder but does not exist in the SOURCE folder, it should be deleted from the REPLICA folder

#SYNCHRONISATION SHOULD BE PERIODIC
# This verification should be performed regularly

#FILE OPERATIONS SHOULD BE LOGGED TO A FILE AND TO THE CONSOLE

#FOLDER PATH, SYNCHRONISATION INTERVAL AND LOG FILE PATH SHOUDLE BE PROVIDEDE USING THE COMMAND-LINE ARGUMENTS

#IT IS UNDESIRABLE TO USE THIRD-PARTY LIBRARIES THAT IMPLEMENT FOLDER SYNCHRONIZATION

#IT IS ALLOWED (AND RECOMMENDED) TO USE EXTERNAL LIBRARIES IMPLEMENTING OTHER WELL-KNOWN ALGORITHMS. FOR EXAMPLE, THERE IS NO POINT IN IMPLEMENTING YET ANOTHER FUNCTION THAT CALCULATES MD5

#----------------------------------------------------------------#

# STEP 1: ARGPARSE

# First step would be to use argparse library to handle input folders, intervals and log file paths. The goal is to parse command line arguments. First thing I do is to import the argparse module.

import argparse

#Then I create a "parse" object of the ArgumentParser class. This will handle all parsing commands. 

parser = argparse.ArgumentParser(description="Synchronise SOURCE and REPLICA folders.") #The description content is purely descriptive. 

#Then I define the command line arguments. Example: The "source" argument expects a string and represents the source folder. The "help" paramenter provides a brief description of the argument. You can access it by using the --help option.

parser.add_argument("source", type=str, help="This is the SOURCE folder path")
parser.add_argument("replica", type=str, help="This is the REPLICA folder path")
parser.add_argument("interval", type=int, help="This is the synchronisation INTERVAL defined in seconds")
parser.add_argument("log_file", type=str, help="This is the LOG FILE path")

#Then I parse the arguments and I can access the values using, for example arg.source.

args = parser.parse_args()

#STEP 2: MAIN FUNCTION (Synchronisation)

#I import the necessary libraries to interacting with the OS, for copying and deleting files and for time functions. 

import os # To navigate the OS
import shutil # To copying and removing files and directories
import time # To set time intervals
import filecmp #To compare files and directories

#Then I define the main function called "synchonise_folders" that takes three arguments, the source path, the replica path and the logfile. This is the function that goes thru the source directory and replicates its structure and contents in the replica directory. It should also remove files from replica that are no longer present in Source directory.

def sync_folders(source, replica, log_file):
     #Now I iterate thru the directory tree rooted at the source folder. Then os.walk generates a list of all the elements in the source folder (files and folders).  
     for root, dirs, files in os.walk(source):
          #Here it computes the relative path of the currency directory in the source folder.
          relative_path = os.path.relpath(root, source)
          #Now it creates the path for the corresponding directory in the replica folder by joining replica and the relative_path.
          replica_root = os.path.join(replica, relative_path)
          #Now the function creates a directory in the replica_root if it is does not exist
          if not os.path.exists(replica_root):
              os.makedirs(replica_root)
              #Then it logs the creation of the directory
              log_operation(f"Created directory: {replica_root}", log_file)

          #Now I need to create a loop that iterates over each file in the files list."Files" contains the files found in the current directory. 
          for file in files:
               #Here I construct the full path for the source and replica files. 
               source_file = os.path.join(root, file)
               replica_file = os.path.join(replica_root, file)
               
               #Here I check whether the file does not exist in replica or if it is different from the source file. 
               if not os.path.exists(replica_file) or not filecmp.cmp(source_file, replica_file):
                #Here I copy copy source to replica.
                shutil.copy2(source_file, replica_file)
                #Here I log the operation
                log_operation(f"Copied file: {source_file} to {replica_file}", log_file)
    #Since this is a one way synchronisation, I need to make sure that if a folder/file exists in the replica but not in the source folder, it should be deleted from the replica folder.
    #I start by iterating thru the tree in replica. 
     for root, dirs, files in os.walk(replica):
            #I compute the relative path in replica folder and again create a path for the correspondinf directory un the source folder.
            relative_path = os.path.relpath(root, replica)
            source_root = os.path.join(source, relative_path)
            #Iterate thru each file.
            for file in files:
                #Construct the full path for replica and source files.
                replica_file = os.path.join(root, file)
                source_file = os.path.join(source_root, file)
                #If file does not exist in source, delete it from replica and log the operation.
                if not os.path.exists(source_file):
                    os.remove(replica_file)
                    log_operation(f"Removed file: {replica_file}", log_file)
            #Iterative thru every directory. 
            for dir in dirs:
                #Construct full path for both.
                replica_dir = os.path.join(root, dir)
                source_dir = os.path.join(source_root, dir)
                #If dir does not exist in source, delete it from replica and log the operation.
                if not os.path.exists(source_dir):
                    shutil.rmtree(replica_dir)
                    log_operation(f"Removed directory: {replica_dir}", log_file)

#Here I define the log operation. It logs messages to both the log_file and the console.
def log_operation(message, log_file):
     with open(log_file, "a") as log:
          log.write(message + "\n")
          print(message)

#Here the script runs the syn_folders in a loop, pausing for the interval time between interations by time.sleep() function to wait for the interval.
while True:
     sync_folders(args.source, args.replica, args.log_file)
     time.sleep(args.interval)

#To run the program, I need to open a command prompt in the directory where the script is and type: python + program.py + (4 parameters: source location, replica location, interval and logfile) in the command-line.

#Example: python ff_task.py (source location) (replica location) (interval time) (logfile location)