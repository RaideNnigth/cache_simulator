"""
File: block.py
Author: Gustavo Pereira
Date: February 3, 2024
Description: Block class for processing data and saving data structure.
"""
from collections import deque

class Block:
    def __init__(self, bsize: int, ways: int = 0, subs_method: str = "R", debug: bool = False) -> None:
        # Custom flags
        self.debug = debug

        # Block props
        self.ways = ways
        self.subs_method = subs_method
        self.bsize = bsize

        # Block structure
        self.block_tag: deque[int] = deque([], maxlen= self.ways)                # Create a deque with the max length of the ways
        self.block_valid: deque[int] = deque([], maxlen= self.ways)              # Create a deque with the max length of the ways

        # Startup
        self.start_block()

    def start_block(self) -> None:
        """
        Start the block with the initial values.
        """
        # Start values
        tag = -1
        valid_bit = 0

        # Write the block props
        for way in range(self.ways):
            self.block_tag.append(tag)
            self.block_valid.append(valid_bit)

    def update(self, way: int, tag: int) -> None:
        """
        Update the block.

        Args:
            way (int): Way to update the block.
            tag (int): Tag to update the block.
        """
        self.block_tag[way] = tag
        self.block_valid[way] = 1

    def update_fifo(self, tag) -> None:
        """
        Update the block with FIFO.

        Args:
            tag (int): Tag to update the block.
        """
        # append left the tag and valid bit
        self.block_tag.appendleft(tag)
        self.block_valid.appendleft(1)

    def update_lru(self, tag) -> None:
        """
        Update the block with LRU.

        Args:
            tag (int): Tag to update the block.
        """

        # Update LRU
        pass