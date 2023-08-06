import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import pygammon  # noqa: E402

project = "pygammon"
copyright = "2023, Aristotelis Mikropoulos"
author = "Aristotelis Mikropoulos"
release = pygammon.__version__
extensions = ["sphinx.ext.autodoc", "sphinx.ext.intersphinx", "sphinx.ext.napoleon"]
autodoc_member_order = "bysource"
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "sphinx_rtd_theme"
