import sys
import os
import binascii
import errno

class FileEntry:
    filename = ""
    size = 0
    start = 0

    def __init__(self, filename, size, start):
        self.filename = filename
        self.size = size
        self.start =  start

    def write_out(self, file_in):
        mkdir_p(os.path.dirname(self.filename))
        
        file_in.seek(self.start)
        file_out = open(self.filename, "wb")

        i = self.size
        while i > 0:

            if(i > 1024):
                file_out.write(file_in.read(1024))
                i-=1024
            else:
                file_out.write(file_in.read(i))
                i=0

        file_out.close()

    def info(self):
        print(self.filename + " size=" + '0x{:08x}'.format(self.size) + " start=" + '0x{:08x}'.format(self.start))



def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def main():
    file_ns = open(sys.argv[1], "rb")

    add_start = int.from_bytes(file_ns.read(4), byteorder="little")

    file_ns.seek(5, 0)

    byte_read = b'\x00'
    byte_array = []
    list_files = []

    while file_ns.tell() < add_start:
        while byte_read != b"\x22":
            byte_read = file_ns.read(1)

            if(byte_read != b"\x22"):
                byte_array.append(byte_read)

        file_size = int.from_bytes(file_ns.read(4), byteorder="little")
        filename = b''.join(byte_array).decode("ascii")
        byte_array.clear()
        file_ns.seek(1, 1)
        byte_read = b'\x00'

        if len(list_files) >= 1:
            prev_file = list_files[len(list_files)-1]
            file_entry = FileEntry(filename, file_size, prev_file.start + prev_file.size)
            list_files.append(file_entry)
        else:
            file_entry = FileEntry(filename, file_size, add_start)
            list_files.append(file_entry)

    for file_entry in list_files:
        file_entry.info()
        file_entry.write_out(file_ns)

    file_ns.close()

if __name__ == "__main__":
    main()