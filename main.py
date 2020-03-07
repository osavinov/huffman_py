from coders import Encoder
from writers import BytesBufferWriter, WriteBuffer
from readers import ReadBuffer

import time
import argparse


def encode(source_file: str, archive_file: str):
    start_time = time.time()
    input_file = ReadBuffer(buffer_size=1024*1024, filename=source_file)
    freq = input_file.scan_file()
    print("File scanning: --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    encoder = Encoder(freq)
    encoder.generate_codes()
    codes = encoder.get_codes()
    encoder.print_codes()
    print("Codes generation: --- %s seconds ---" % (time.time() - start_time))
    #start_time = time.time()
    #output_archive = BytesBufferWriter(filename=archive_file)
    #input_file.open()
    #output_archive.write_header(input_file.filesize, codes)
    #portion = input_file.read()
    #while portion:
    #    for c in portion:
    #        output_archive.add(codes[c])
    #    portion = input_file.read()
    #output_archive.close()
    #input_file.close()
    #print("Encoding: --- %s seconds ---" % (time.time() - start_time))


def decode(archive_file: str, dest_file: str):
    start_time = time.time()
    input_archive = ReadBuffer(filename=archive_file)
    input_archive.open()
    file_size, code_table = input_archive.read_header()
    output_file = WriteBuffer(filename=dest_file)
    bytes_counter = 0
    percent = file_size // 100
    percents_counter = 0
    new_percent = 0
    portion = input_archive.read()
    while portion:
        buffer = input_archive.convert_from_bytes()
        code = ""
        for c in buffer:
            if bytes_counter == file_size:
                break
            code += c
            if code in code_table:
                output_file.add(code_table[code])
                code = ""
                bytes_counter += 1
                new_percent += 1
                if new_percent == percent:
                    new_percent = 0
                    percents_counter += 1
                    print(percents_counter, "% processed")
        portion = input_archive.read()
    output_file.close()
    print("Decoding: --- %s seconds ---" % (time.time() - start_time))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="enc/dec for encoding/decoding", default="enc")
    parser.add_argument("--source", help="Source file", default="test.txt")
    parser.add_argument("--dest", help="Destination file", default="test.huf")
    args = parser.parse_args()

    if args.mode == "enc":
        encode(args.source, args.dest)
    elif args.mode == "dec":
        decode(args.source, args.dest)


if __name__ == "__main__":
    main()
