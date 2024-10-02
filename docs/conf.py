# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
from autoflex.directives.flextree.directive import logger

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'autoflex'
copyright = '2024, Flexcompute Inc.'
author = 'daquintero'
release = '0.0.1'
master_doc = "index"  # The master toctree document.

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "autoflex",
]

templates_path = [
    '_templates'
]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = []


import logging
logger.setLevel(logging.DEBUG)


from docutils.parsers.rst import directives
from sphinx.directives.other import TocTree
from sphinx import addnodes

class CustomTocTree(TocTree):
    option_spec = TocTree.option_spec.copy()
    option_spec['descriptions'] = directives.unchanged
    option_spec['images'] = directives.unchanged

    def run(self):
        toctree_nodes = super().run()
        # Parse descriptions and images from options
        descriptions = {}
        images = {}
        if 'descriptions' in self.options:
            desc_list = self.options['descriptions'].split('\n')
            for entry in desc_list:
                key, value = entry.strip().split('=', 1)
                descriptions[key.strip()] = value.strip()
        if 'images' in self.options:
            img_list = self.options['images'].split('\n')
            for entry in img_list:
                key, value = entry.strip().split('=', 1)
                images[key.strip()] = value.strip()
        # Attach descriptions and images to the toctree node
        for node in toctree_nodes:
            if isinstance(node, addnodes.toctree):
                node['descriptions'] = descriptions
                node['images'] = images
        return toctree_nodes

def setup(app):
    app.add_directive('customtoctree', CustomTocTree)

