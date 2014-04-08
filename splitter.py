import os, re

input = "c:\\patenty\\ipg131224\\concated.xml"
dir = "c:\\patenty\\ipg131224\\concated"

def get_headers_and_filename(file):
    headers = []
    for i in range(3):
        line = file.readline()
        headers.append(line)
    print headers[2]
    return headers, re.match(r'.*file=.([^ ]*)\".*', headers[2]).group(1)

def split_file(input_file):
    fread = open(input_file)
    os.makedirs(dir)
    eof = os.fstat(fread.fileno()).st_size
    while fread.tell() < eof:
        headers, filename = get_headers_and_filename(fread)
        print filename
        fwrite = open(os.path.join(dir, filename), 'w')
        for line in headers: fwrite.write(line)
        while True:
            line = fread.readline()
            fwrite.write(line)
            if line.startswith('</us-patent-grant'): break

split_file(input)