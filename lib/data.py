'''Simple data loader module.

Loads data files from the "data" directory shipped with a game.

Enhancing this to handle caching etc. is left as an exercise for the reader.
'''

import os
import pygame

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))

# The following is only used when packaging for .app
#data_dir = os.path.normpath(os.path.join(data_py, '..', '..', '..', 'data'))


def filepath(filename):
    '''Determine the path to a file in the data directory.
    '''
    return os.path.join(data_dir, filename)

def load_image(filename):
    # Open a file in the data directory.
    return pygame.image.load(os.path.join(data_dir, filename))
    #return open(os.path.join(data_dir, filename), mode)

