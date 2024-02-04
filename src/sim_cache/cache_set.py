"""
File: cache_set.py
Author: Gustavo Pereira
Date: February 3, 2024
Description: Cache set class for processing data and saving data structure.
"""

from collections import deque
from random import randint

from math import log2, pow
from block import Block

class CacheSet:
    def __init__(self, bsize:int, nsets: int, ways: int, subs_method: str ) -> None:
        # Cache parameters
        self.nsets = nsets              # Number of sets for the cache (blocks)
        self.ways = ways                # Number of ways in the set (associativity)
        self.subs_method = subs_method
        self.cache_set: list[Block] = []
        self.bsize = bsize

        # Cache startup
        self.start_cache_set()

    def start_cache_set(self) -> None:
        """
        Start the cache set with the initial values.
        """
        for i in range(self.nsets):
            self.cache_set.append(Block(self.bsize, self.ways, self.subs_method))
    
    def check_memory_access(self, index: int, tag: int) -> str:
        """
        Check the memory access and update the cache set.
        
        Args:
            index (int): Index of the block in the cache set.
            tag (int): Tag of the block in the cache set.
        Return:
            str: Hit or Compulsory miss or Capacity miss or Conflict miss.
        """
        
        # Check if there is any valid bit set to 1 in the block(index)
        result:str
        if 1 in self.cache_set[index].block_valid:
            if tag in self.cache_set[index].block_tag:
                result = "Hit"
            elif 0 in self.cache_set[index].block_valid:
                self.substitution(index, tag)
                result = "Compulsory miss"
            else:
                self.substitution(index, tag)
                result = "Conflict miss"
        else:
            self.substitution(index, tag)
            result = "Compulsory miss"
        return result
    
    def substitution(self, index:int, tag: int) -> None:
        """
        Substitution method.

        Args:
            index (int): Index of the block in the cache set.
            tag (int): Tag of the block in the cache set.
        """
        if self.subs_method == "R":
            self.random_substitution(index, tag)
        elif self.subs_method == "L":
            self.LRU_substitution(tag)
        elif self.subs_method == "F":
            self.FIFO_substitution(tag)
    
    def LRU_substitution(self, tag: int) -> None:
        pass
    
    def FIFO_substitution(self, tag: int) -> None:
        """
        FIFO substitution method.

        Args:
            tag (int): Tag of the block in the cache set.
        """

        # Update the block
        self.cache_set[0].update_fifo(tag)

    def random_substitution(self, index: int, tag: int) -> None:
        """
        Random substitution method.

        Args:
            index (int): Index of the block in the cache set.
            tag (int): Tag of the block in the cache set.
        """

        # Get the random way in the block to update
        random_way = randint(0, self.ways-1)

        # Update the block
        self.cache_set[index].update(random_way, tag)