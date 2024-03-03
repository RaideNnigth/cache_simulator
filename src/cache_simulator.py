"""
File: cache_simulator.py
Author: Gustavo Pereira
Date: February 3, 2024
Description: Cache simulator for binary files. It can simulate the cache and return some statistics.
             You need to pass the following parameters: 
                nsets (Number of sets for the cache)
                bsize (Block size for the cache)
                assoc (Associativity for the cache)
                subs_method (Replacement policy for the cache)
                output_flag 
                    ( 
                    Flag that defines how the output will look like, flag=0 for free format,
                    flag=1 The default output format should adhere to the following order:
                    Total accesses, Hit rate, Miss rate, Compulsory miss rate, Capacity miss rate, Conflict miss rate.Example: 100000, 0.95, 0.06, 0.01, 0.02, 0.03.
                    )
                input_file (Path to the file to read, needs to be a binary file)
                --debug (Debug mode, just for testing purposes. OPTIONAL. Default is False.)
             Example: python cache_simulator.py 256 4 1 R 1 bin_100.bin
"""

import argparse
import time
import sys
from sim_cache.file_reader import read_file
from sim_cache.cache import Cache

def simulate_cache(nsets: int, bsize: int, assoc: int, subs_method: str, output_flag: int, input_file: str, debug: bool=False) -> str:
    """
    Simulate the cache and return some statistics.

    Args:
        nsets (int): Number of sets for the cache
        bsize (int): Block size for the cache
        assoc (int): Associativity for the cache
        subs_method (str): Replacement policy for the cache
        output_flag (int): Flag that defines how the output will look like
        input_file (str): Path to the file to read, needs to be a binary file
        debug (bool): Debug mode, just for testing purposes
    Returns:
        str: Statistics from the cache simulation
    """

    if (debug):
        print("--------------------------------------------")
        print("Debug mode set to True. Parameters:")
        print("nsets: ", nsets)
        print("bsize: ", bsize)
        print("assoc: ", assoc)
        print("subs_method: ", subs_method)
        print("output_flag: ", output_flag)
        print("input_file: ", input_file)
        print("--------------------------------------------")

    memory_address_byte, memory_address_int = read_file(input_file)
    cache = Cache(nsets, bsize, assoc, subs_method, output_flag, input_file, debug)
    return cache.simulate_cache(memory_address_byte, memory_address_int)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Cache simulator for binary files.")
    parser.add_argument("nsets", type=int, help="Number of sets for the cache")
    parser.add_argument("bsize", type=int, help="Block size for the cache")
    parser.add_argument("assoc", type=int, help="Associativity for the cache")
    parser.add_argument("subs_method", type=str, help="Replacement policy for the cache")
    parser.add_argument("output_flag", type=int, help="Flag that defines how the output will look like, flag=0 for free format, flag=1 The default output format should adhere to the following order: Total accesses, Hit rate, Miss rate, Compulsory miss rate, Capacity miss rate, Conflict miss rate.Example: 100000, 0.95, 0.06, 0.01, 0.02, 0.03.")
    parser.add_argument("input_file", type=str, help="Path to the file to read, needs to be a binary file")
    parser.add_argument("--debug", type=bool, help="Debug mode", default=False, required=False)
    args = parser.parse_args()

    try:
        start = time.time()
        result = simulate_cache(args.nsets, args.bsize, args.assoc, args.subs_method, args.output_flag, args.input_file, args.debug)
        #result = simulate_cache(1, 4, 32, "L", 1, 
        #"C:\\Users\\gusta\\OneDrive\\Documents\\GitHub\\cache_simulator\\example_files\\address\\vortex.in.sem.persons.bin", True)
        end = time.time()
        print(result)
        print("Execution time: {:.6f} seconds".format(end - start))
    except Exception as e:
        print(e)
        sys.exit(1)
