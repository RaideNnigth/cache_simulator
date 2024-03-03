"""
File: cache_set.py
Author: Gustavo Pereira
Date: February 4, 2024
Description: Cache set class for processing data and saving data structure.
"""

from collections import deque
from random import randint

from math import log2, pow
from .block import Block

class CacheSet:
    def __init__(self, number_of_blocks: int, bsize:int, nsets: int, ways: int, subs_method: str ) -> None:
        # Cache parameters
        self.number_of_blocks = number_of_blocks
        self.nsets = nsets              # Number of sets for the cache (blocks)
        self.ways = ways                # Number of ways in the set (associativity)
        self.subs_method = subs_method
        self.cache_set: list[Block] = []
        self.bsize = bsize

        # Cache counters
        self.occupied_blocks = 0

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

        # Block being accessed
        block = self.cache_set[index]
        


        # Check if the block has any valid bit set to 1
        if block.block_valid.count(1) >= 1:
            # Check if the tag is in the block
            if tag in block.block_tag:
                # Record access for LRU
                block.record_access(block.block_tag.index(tag))
                return "Hit"

        # If there is any valid bit set to 0 in the block, we have a compulsory miss
        if block.block_valid.count(0) >= 1:
            # Get the first way with valid bit set to 0
            for i in range(self.ways):
                if block.block_valid[i] == 0:
                    block.block_valid[i] = 1
                    block.block_tag[i] = tag
                    self.occupied_blocks += 1
                    # Record access for LRU
                    block.record_access(i)
                    return "Compulsory miss"

        # Check if block is full (if all valid bits are set to 1, we have a capacity miss)
        if self.occupied_blocks == self.number_of_blocks:
            result = "Capacity miss"
        # If the block is not full, we have a conflict miss
        else:
            self.substitution(index, tag)
            result = "Conflict miss"
        
        # Replace the block with the substitution method
        self.substitution(index, tag)
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
            self.LRU_substitution(index, tag)
        elif self.subs_method == "F":
            self.FIFO_substitution(index, tag)
        
    
    def LRU_substitution(self, index: int, tag: int) -> None:
        """
        LRU substitution method.

        Args:
            index (int): Index of the block in the cache set.
            tag (int): Tag of the block in the cache set.
        """
        self.cache_set[index].update_lru(tag)
    
    def FIFO_substitution(self, index: int, tag: int) -> None:
        """
        FIFO substitution method.

        Args:
            tag (int): Tag of the block in the cache set.
        """

        # Update the block
        self.cache_set[index].update_fifo(tag)

    def random_substitution(self, index: int, tag: int) -> str:
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
    