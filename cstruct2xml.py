import re


_pattern = re.compile(r'(?:(?:(?://[^\n]*\n)|(?:/\*(?:[^*]|(?:\*[^/]))*\*/))\s*)*'
                      r'typedef\s+struct\s+(?:[\w_][\w\d_]*)?\s*\{')


def extract(string):
    pass


def lex(definition):
    pass


def parse(lexed_definition):
    pass


def main():
    import optparse
    opt_parser = optparse.OptionParser()
    opt_parser.add_option('-e', "--encoding", dest="encoding",
                          help="Use specific encoding for files. Default is utf-8.", metavar="ENCODING")
    options, args = opt_parser.parse_args()
    print(options, args)

if __name__ == '__main__':
    main()
