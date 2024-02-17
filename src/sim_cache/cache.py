"""
File: cache.py
Author: Gustavo Pereira
Date: February 3, 2024
Description: Cache core class for processing data and saving data structure.
"""

from collections import deque
from math import log2, pow
from cache_set import CacheSet

class Cache:
    def __init__(self, nsets: int, bsize: int, ways: int, subs_method: str, output_flag: int, input_file: str, debug_var: bool = False):
        # Cache parameters
        self.nsets = nsets
        self.bsize = bsize
        self.ways = ways
        self.subs_method = subs_method
        self.output_flag = output_flag
        self.input_file = input_file

        # Misses counters
        self.compulsory_misses = 0
        self.capacity_misses = 0
        self.conflict_misses = 0
        self.total_misses = 0

        # Memory access Hit counters
        self.memory_access_hit = 0

        # Total access counter
        self.total_accesses = 0

        # Cache Statistics
        self.total_accesses = 0
        self.hit_rate = 0
        self.miss_rate = 0
        self.compulsory_miss_rate = 0
        self.capacity_miss_rate = 0
        self.conflict_miss_rate = 0

        # Custom flags
        self.debug_var = debug_var

        # Cache calculated parameters
        self.number_of_blocks = self.nsets * self.ways
        self.n_bits_offset = int(log2(self.bsize))
        self.n_bits_indice = int(log2(self.nsets))
        self.n_bits_tag = 32 - (self.n_bits_offset + self.n_bits_indice)
        self.cache_size = self.nsets * self.bsize * self.ways

        # Calculating real cache size (in bytes)
        self.real_cache_size = ((self.n_bits_tag + 1 + (self.bsize * 8)) * self.nsets * self.ways) / 8

        # Cache structure
        self.cache_set: CacheSet = CacheSet(self.number_of_blocks, self.bsize, self.nsets, self.ways, self.subs_method)
    
    def simulate_cache(self, memory_address_byte: list[bytes], memory_address_int: list[int]) -> None:
        """
        Simulate the cache and return some statistics. (Can simulate direct-mapped, fully associative and multi-way set associative)

        Args:
            memory_address_byte (list[bytes]): List of bytes with the memory address.
            memory_address_int (list[int]): List of integers with the memory address.
        Returns:
            list[int]: List of integers with the cache request.
        """
        
        for address in memory_address_int:
            # Get the tag and index from the address
            tag = address >> int(self.n_bits_offset + self.n_bits_indice)
            index = (address >> self.n_bits_offset) & int(pow(2, self.n_bits_indice) -1)

            # Check the memory access and update the cache set
            result = self.cache_set.check_memory_access(index, tag)
            # Update the counters
            if result == "Hit":
                self.memory_access_hit += 1
            elif result == "Compulsory miss":
                self.compulsory_misses += 1
            elif result == "Conflict miss":
                self.conflict_misses += 1
            elif result == "Capacity miss":
                self.capacity_misses += 1
                  
            # Update the total accesses
            self.total_accesses += 1

            # Check for debug mode to log the address, tag and index
            if self.debug_var:
                self.save_on_log("Address: {}, tag: {}, index: {}, result: {}".format(address, tag, index, result))
        
        # Return the output
        return self.get_output()
    
    def save_on_log(self, message: str) -> None:
        """
        Save a message on a log file.

        Args:
            message (str): Message to save on the log file.
        Returns:
        """
        with open("log.txt", "a") as file:
            file.write(message + "\n")

    def get_output(self) -> str:
        """
        Get the output for the cache simulation.
        
        Args:
        Returns:
            str: Output for the cache simulation. Depends on the output_flag.
        """

        self.set_cache_statistics()

        if self.output_flag == 0:
            return "Total accesses: {}\nHit rate: {} %\nMiss rate: {} %\nCompulsory miss rate: {} %\nCapacity miss rate: {} %\nConflict miss rate: {} %\nConflict misses: {}\nCompulsory misses:{}\nCapacity misses: {}\nTotal misses: {}".format(
                self.total_accesses, 
                self.hit_rate * 100, 
                self.miss_rate * 100, 
                self.compulsory_miss_rate * 100, 
                self.capacity_miss_rate * 100, 
                self.conflict_miss_rate * 100,
                self.conflict_misses,
                self.compulsory_misses,
                self.capacity_misses,
                self.total_misses
            )
        elif self.output_flag == 1:
            return "{}, {}, {}, {}, {}, {}".format(
                self.total_accesses, 
                self.hit_rate, 
                self.miss_rate, 
                self.compulsory_miss_rate, 
                self.capacity_miss_rate, 
                self.conflict_miss_rate
            )
    
    def set_cache_statistics(self) -> None:
        """
        Set the cache statistics for the cache simulation.

        Args:
        Returns:
        """
        self.total_misses = self.compulsory_misses + self.capacity_misses + self.conflict_misses
        if (self.total_accesses != 0):
            self.hit_rate = round(self.memory_access_hit / self.total_accesses, 2)
        
        self.miss_rate = round(1 - self.hit_rate, 2)

        if (self.total_misses != 0):
            self.compulsory_miss_rate = round(self.compulsory_misses / self.total_misses, 2)
            self.capacity_miss_rate = round(self.capacity_misses / self.total_misses, 2)
            self.conflict_miss_rate = round(self.conflict_misses / self.total_misses, 2)

    def debug(self) -> None:
        """
        Print cache informations for debug purposes. Just when the debug flag is set to True.

        Args:
        Returns:
        """
        if self.debug:
            print("--------------------------------------------")
            print("Cache parameters:")
            print("nsets: ", self.nsets)
            print("bsize: ", self.bsize)
            print("assoc: ", self.assoc)
            print("subs_method: ", self.subs_method)
            print("output_flag: ", self.output_flag)
            print("input_file: ", self.input_file)
            print("Cache calculated parameters:")
            print("number_of_blocks: ", self.number_of_blocks)
            print("n_bits_offset: ", self.n_bits_offset)
            print("n_bits_indice: ", self.n_bits_indice)
            print("n_bits_tag: ", self.n_bits_tag)
            print("Cache structure:")
            #print("cache_tag: ", self.cache_tag)
            #print("cache_valid: ", self.cache_valid)
            print("Misses counters:")
            print("compulsory_misses: ", self.compulsory_misses)
            print("capacity_misses: ", self.capacity_misses)
            print("conflict_misses: ", self.conflict_misses)
            print("total_misses: ", self.total_misses)
            print("Memory access Hit counters:")
            print("memory_access_hit: ", self.memory_access_hit)
            print("Custom flags:")
            print("debug: ", self.debug_var)
            print("--------------------------------------------")
        else:
            print("Debug mode is not set to True.")
        