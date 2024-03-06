# cache_simulator

Cache simulator for MIPS like architecture in backend with Rust and Frontend with Python/Flask

### Requirements to run

* Python 3+ ([Python download](https://www.python.org/downloads/))
* Flask (Use Pip install flask)

### How to run


If you are in any linux/Windows distro and want to run the Web Interface:

* pip install -r requirements.txt
* python ./src/app.py  or better just run on visual studio code

If you are or in windows/linux and want to run just the console interface do the following:

* pip install -r requirements.txt
* python ./src/cache_simulator.py (cache_sets) (block_size) (ways) (replacement_policy) (output_flag) (input_file)

### Observations

* `cache_simulator`: The name of the main execution file of the simulator (all should use this name, regardless of the chosen language).
* `nsets`: Number of sets in the cache (total number of "lines" or "entries" in the cache).
* `bsize`: Block size in bytes.
* `assoc`: Associativity degree (number of ways or blocks each set has).
* `substitution`: Replacement policy, which can be Random (R), FIFO (F), or LRU.
* `output_flag`: Flag that activates the default data output mode.
* `input_file`: File containing the addresses for cache access.
