# About
Converts C structures into XML-output.

# Not implemented
- array size resolving
- pointers
- type resolving
- type equations (e.g. signed int -> int, signed short int -> short)
- binary, octal and hex numbers in array size

# Tests
To run tests you can use bash script `run_tests.sh`.<br>
Another way to run tests is to use following command from root directory of project:<br>
`python3 -m unittest discover -v` or similar (e.g. with other parameters).

# Usage
Used to convert structure definitions from C/C++ into xml format. After generating xml, 
you can use XSLT to transform xml from output format to any other format you need.
Originally was made for specific tasks at work. 


