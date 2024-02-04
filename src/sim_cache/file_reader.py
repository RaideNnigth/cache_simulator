"""
File: file_reader.py
Author: Gustavo Pereira
Date: February 3, 2024
Description: File reader for binary files. It can read the file and return the data in a list of integers.
             It can compare with other txt files to see if the data is correct.
             You can set some flags as: --file_input, --file_output, --file_compare, --abs_path.
             example: python file_reader.py --file_input "file_input.bin" --file_output "file_output.txt" --file_compare "file_compare.txt" --abs_path "y"
"""

import argparse
import os
import time

def read_file(file_input: str, file_output: str = None, file_compare: str = None, abs_path: str = "n") -> tuple[list[bytes], list[int]]:
    """
    Read a binary file and return the data in a list of integers.

    Args:
        file_input (str): Path to the file to read. REQUIRED.
        file_output (str): Path to the file to write the data. OPTIONAL. Default is None.
        file_compare (str): Path to the file to compare the data. OPTIONAL. Default is None.
        abs_path (str): Absolute path for the files. OPTIONAL. Default is "n".

    Returns:
        tuple[list[bytes], list[int]]: Tuple with the data in a list of bytes and a list of integers.
    """
    if abs_path.upper().strip() == "Y" or abs_path.upper().strip() == "YES" or abs_path.upper().strip() == "TRUE" or abs_path.upper().strip() == "1" :
        file_input = os.path.abspath(file_input)
        if file_output:
            file_output = os.path.abspath(file_output)
        if file_compare:
            file_compare = os.path.abspath(file_compare)
    
    if not os.path.exists(file_input):
        out_message = "File input: {} path does not exist."
        raise Exception(out_message.format(file_input))
    
    if not file_input.endswith(".bin"):
        out_message = "File input: {} is not a binary file."
        raise Exception(out_message.format(file_input))
        
    data = []
    data_int = []
    with open(file_input, "rb") as file:
        byte = file.read(4)
        while byte:
            data.append(byte)
            data_int.append(int.from_bytes(byte, byteorder="big", signed="False"))
            byte = file.read(4)

    if file_output:
        with open(file_output, "w") as file:
            for i in data:
                file.write(str(i) + "\n")

    if file_compare:
        if not os.path.exists(file_compare):
            out_message = "File compare: {} path does not exist."
            raise Exception(out_message.format(file_compare))
        with open(file_compare, "r") as file:
            compare_data = [int(line) for line in file]
        if data == compare_data:
            print("Data is correct.")
        else:
            print("Data is incorrect.")

    return data, data_int

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File reader for binary files.")
    parser.add_argument("--file_input", help="Input file to read.", required=True)
    parser.add_argument("--file_output", help="Output file to write.", required=False)
    parser.add_argument("--file_compare", help="File to compare with.", required=False)
    parser.add_argument("--abs_path", help="Absolute path for the files.", required=True)
    args = parser.parse_args()

    print("Arguments---------------------------------")
    print("File input: ", args.file_input)
    print("File output: ", args.file_output)
    print("File compare: ", args.file_compare)
    print("Absolute path: ", args.abs_path)
    print("------------------------------------------")

    start_time = time.time()
    data = read_file(args.file_input, args.file_output, args.file_compare, args.abs_path)
    end_time = time.time()
    print("Time to read the file: ", end_time - start_time, " seconds.")
