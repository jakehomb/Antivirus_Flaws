### To view the README for this repository, please click [here.][1]
 
## Disclaimer:
 
The code and content of this repository are intended for strictly educational purposes. If you decide to do something unethical with it or with any of the ideas from it, I am not responsible for any legal consequences. You are responisble for your own actions.
 
## Table of Contents:
 
- Goal of project
- Reason for writing this article
- Targeted Anti-Virus systems explained
- My (Simplified) understanding of how they work
- Typical means of obfuscation
- Background information for my approach
- Source files explained
- Results
- Credits

## Goal of the project:

The goal of this project was to create a simple method of taking known bad shellcode and storing it on disk in a way that disrupts the "signature" that modern antivirus systems search for. Using the python script and .cpp file in the repository, we are able to show how trivial it is to accomplish this by leveraging a base understanding of variables and how they are stored in a PE file.

## Reason for writing:

This project was done as a topic for my Information Security course at Western Connecticut State University. This particular topic was chosen after taking the [Cracking the Perimeter course from Offensive Security][2]. Using information gained from their courses in addition to some basic work with anti-virus in the IT field, I was able to come up with an idea on what doesn't get caught and why. This led me to a system of automating the generation of what doesnt work for anti-virus and a proof of concept on how to implement it. 

## Signature-based AV Definition:

## My simplified understanding of how Anti-virus works:

### Python styled pseudo code to illustrate:

## Typical means of obfuscation:

## Background information for my approach:

## Source files explained:

## Results:

## Credits:

## Links:
[1]: https://www.github.com/jakehomb/Antivirus_Flaws/blob/master/README.md
[2]: https://www.offensive-security.com/information-security-training/cracking-the-perimeter/
