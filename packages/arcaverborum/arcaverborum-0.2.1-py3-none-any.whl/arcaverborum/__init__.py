# __init__.py

# Set the metadata for the package
__author__ = "Tiago Tresoldi"
__email__ = "tiago.tresoldi@lingfil.uu.se"
__version__ = "0.2.1"

# Local imports
from .common import read_splitstree_matrix, read_default_matrix, read_triangle_matrix
from .sampling import GLED_Sampler

# Expose the functions
all = ["read_matrix", "read_default_matrix", "read_triangle_matrix", "GLED_Sampler"]
