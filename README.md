# About
Converts C structures into XML-output.

# Usage
Used to convert structure definitions from C/C++ into xml format.
This "xml-generator" is made for descriptive structures, so no pointers, vectors, etc. supported.
After generating xml, you can use XSLT to transform xml from output format to any other format you need.

You can use script from `example` folder to convert structures to xml format.
Use `-h` option to see script usage.

# Not implemented
- array size interpretation
- pointers, vectors, bit fields, dynamic data structures, etc. (Probably will never support this: see usage)
- binary, octal and hex numbers in array size
- look-up includes for type resolving

# Tests
To run tests you can use bash script `run_tests.sh`.  
Another way to run tests is to use following command from root directory of project:  
`python3 -m unittest discover -v` or similar (e.g. with other parameters).
