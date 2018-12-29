import os
import sys
import io
import tempfile


def main():
    file_out = open(sys.argv[2], "wb")
    header_stream = io.BytesIO()
    header_stream.write(int(0).to_bytes(4, byteorder="little"))
    files_stream = tempfile.TemporaryFile()

    for root, dirs, files in os.walk(sys.argv[1], topdown=True):
        for name in files:
            filename = "\""+os.path.join(root, name)[len(sys.argv[1]):]+"\""
            size = os.path.getsize(os.path.join(root, name))

            header_stream.write(filename.encode("ascii"))
            header_stream.write(int(size).to_bytes(4, byteorder="little"))
            print("Processing : " + filename)

            with open(os.path.join(root, name), "rb") as f:
                files_stream.write(f.read())


    print("Writing into file")
    header_stream.write(b"\x65")
    header_size = header_stream.tell()
    header_stream.seek(0, 0)
    header_stream.write(int(header_size).to_bytes(4, byteorder="little"))
    header_stream.seek(0, 0)

    file_out.write(header_stream.read())
    header_stream.close()

    files_stream.seek(0,0)
    file_out.write(files_stream.read())
    files_stream.close()
    file_out.close()




if __name__ == "__main__":
    main()