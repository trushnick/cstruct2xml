# About
Converts C structures into XML-output.

# Usage
Used to convert structure definitions from C/C++ into xml format. After generating xml, 
you can use XSLT to transform xml from output format to any other format you need.  
Originally was made for specific tasks at work.  

You can use script from `example` folder to convert structures to xml format.
Use `-h` option to see script usage.

# Not implemented
- array size resolving
- pointers  
I don't think that pointers will be supported since this utility made for
descriptive structures (parameters) that don't have any pointers at all.
- type resolving
- binary, octal and hex numbers in array size

# Tests
To run tests you can use bash script `run_tests.sh`.  
Another way to run tests is to use following command from root directory of project:  
`python3 -m unittest discover -v` or similar (e.g. with other parameters).
