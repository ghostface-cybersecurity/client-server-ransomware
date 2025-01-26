 ######     ##     ##   ##   #####    #####   ##   ##  ##   ##    ##     ######   #######
  ##  ##   ####    ###  ##  ##   ##  ##   ##  ### ###  ##   ##   ####     ##  ##   ##   #
  ##  ##  ##  ##   #### ##  #        ##   ##  #######  ##   ##  ##  ##    ##  ##   ## #
  #####   ##  ##   ## ####   #####   ##   ##  #######  ## # ##  ##  ##    #####    ####
  ## ##   ######   ##  ###       ##  ##   ##  ## # ##  #######  ######    ## ##    ## #
  ##  ##  ##  ##   ##   ##  ##   ##  ##   ##  ##   ##  ### ###  ##  ##    ##  ##   ##   #
 #### ##  ##  ##   ##   ##   #####    #####   ##   ##  ##   ##  ##  ##   #### ##  #######

_________________________________________________________________________________________
                                          ABOUT
_________________________________________________________________________________________
Description: A ransomware that encrypts one file and contacts the server for decryption. 
             Prototype of a modern ransomware. 
Program: Ransomware (client-server) / A prototype of a modern ransomware
Languages: Python 3.12.7
Tested on: Linux 6.11.2
Author: ghostface-cybersecurity

_________________________________________________________________________________________
                                        PROGRAM LAUNCH
_________________________________________________________________________________________
// First, start a server that will decrypt files
python3 ransomware_server.py
// Then create a simple text file that will be encrypted
echo "hello ransomware" > file.txt
// Then you can run a client that will encrypt the file
// Examle: python3 ransomware.py <host server> <port server> <file>
python3 ransomware.py 0.0.0.0 8000 file.py

_________________________________________________________________________________________
                                        LEGAL STATEMENT
_________________________________________________________________________________________
By downloading, modifying, redistributing, and/or executing client-server-ransomware, the
user agrees to the contained LEGAL.txt statement found in this repository.

I, ghostface-cybersecurity, the creator, take no legal responsibility for unlawful actions
caused/stemming from this program. 

Use responsibly and ethically!
