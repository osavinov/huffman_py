from coders import Encoder
from writers import BytesBufferWriter, WriteBuffer
from readers import ReadBuffer

import time
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="enc/dec for encoding/decoding", default="dec")
    parser.add_argument("--source", help="Source file", default="test.huf")
    parser.add_argument("--dest", help="Destination file", default="result.log")
    args = parser.parse_args()

    # encoding
    if args.mode == "enc":
        start_time = time.time()
        input_file = ReadBuffer(buffer_size=1024 * 1024, filename=args.source)
        freq = input_file.scan_file()
        print("File scanning: --- %s seconds ---" % (time.time() - start_time))

        start_time = time.time()
        encoder = Encoder(freq)
        encoder.generate_codes()
        codes = encoder.get_codes()
        encoder.check_codes()
        print("Codes generation: --- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        output_archive = BytesBufferWriter(filename=args.dest)
        input_file.open()
        output_archive.write_header(input_file.filesize, codes)
        portion = input_file.read()
        while portion:
            for c in portion:
                output_archive.add(codes[c])
            portion = input_file.read()
        output_archive.close()
        input_file.close()
        print("Encoding: --- %s seconds ---" % (time.time() - start_time))
    elif args.mode == "dec":
        # decoding
        start_time = time.time()
        input_archive = ReadBuffer(filename=args.source)
        input_archive.open()
        file_size, code_table = input_archive.read_header()
        output_file = WriteBuffer(filename=args.dest)
        bytes_counter = 0
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
            portion = input_archive.read()
        output_file.close()
        print("Decoding: --- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
