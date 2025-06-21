import generators.search as search
import math
import os

import numpy as np

class Generator:
    def __init__(self, env):
        print("Initializing generator")
        self._env = env
        self._random = np.random.default_rng()

    def reset(self, **kwargs):
        print("Resetting generator")
        # Get parameters from kwargs or set defaults (as needed)
        self._current = 0
        self._random = np.random.default_rng(kwargs.get('seed'))

        # Load the input file (input/message.txt)
        file_contents = ""
        with open("input/message.txt", "r") as file:
            file_contents = file.read()

        # parse the contents by new lines
        # and store them in a list
        self._messages = file_contents.splitlines()
        self._messages = [msg.strip() for msg in self._messages if msg.strip()]
        print(f"Loaded {len(self._messages)} messages from input/message.txt")

            
    def update(self):
        print("Updating generator")
        # This function is expected to be implemented in subclasses
        self._current += 1

    def best(self):
        return 0.0
    
    def save(self, folderpath):
        print("Saving generator state")

        # Ensure the folder exists
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)
            print(f"Created folder: {folderpath}")

        # just save the current message to a file
        with open(f"{folderpath}/info.json", "w") as f:
            message = self._messages[self._current % len(self._messages)]
            f.write(f'{{"content": "{message}"}}')
        print(f"Saved message: {message} to {folderpath}/info.json")

    def load(self, folderpath):
        print("Saving generator state, but the save function is not implemented.")
        return NotImplementedError("The load function is not implemented, please make sure to implment it.")