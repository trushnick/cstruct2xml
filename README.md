# About
Converts C structures into XML-output.

# Usage
Used to convert structure definitions from C/C++ into xml format.
This "xml-generator" is made for descriptive structures, so no pointers, vectors, etc. supported.
After generating xml, you can use XSLT to transform xml from output format to any other format you need.

# Not implemented
- array size interpretation
- pointers, vectors, bit fields, dynamic data structures, etc. (Probably will never support this: see usage)
- binary, octal and hex numbers in array size
- look-up includes for type resolving
