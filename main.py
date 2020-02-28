from coders import Encoder
from writers import BytesBufferWriter, WriteBuffer
from readers import ReadBuffer

import time


def main():
    files = {"sourse": "Agents.pdf", "archive": "result.huf", "dest": "Agents1.pdf"}

    start_time = time.time()
    input_file = ReadBuffer(buffer_size=1024*1024, filename=files["sourse"])
    freq = input_file.scan_file()
    print("File scanning: --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    encoder = Encoder(freq)
    encoder.generate_codes()
    codes = encoder.get_codes()
    encoder.check_codes()
    print("Codes generation: --- %s seconds ---" % (time.time() - start_time))

    # encoding
    start_time = time.time()
    output_archive = BytesBufferWriter(filename=files["archive"])
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

    # decoding
    start_time = time.time()
    reversed_codes = encoder.get_reversed_codes()
    output_file = WriteBuffer(filename=files["dest"])
    input_archive = ReadBuffer(filename=files["archive"])
    input_archive.open()
    filesize = input_archive.read_sourcefile_size()
    bytes_counter = 0
    portion = input_archive.read()
    while portion:
        buffer = input_archive.convert_from_bytes()
        code = ""
        for c in buffer:
            if bytes_counter == filesize:
                break
            code += c
            if code in reversed_codes:
                output_file.add(reversed_codes[code])
                code = ""
                bytes_counter += 1
        portion = input_archive.read()
    output_file.close()
    print("Decoding: --- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
