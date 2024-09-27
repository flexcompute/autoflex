from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, List, Dict, Tuple

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.domains.changeset import VersionChange  # NoQA: F401  # for compatibility
from sphinx.domains.std import StandardDomain
from sphinx.locale import _, __
from sphinx.util import docname_join, logging, url_re
from sphinx.util.docutils import SphinxDirective
from sphinx.util.matching import Matcher, patfilter
from sphinx.util.nodes import explicit_title_re

if TYPE_CHECKING:
    from docutils.nodes import Node

logger = logging.getLogger(__name__)

glob_re = re.compile(r'.*[*?\[].*')

def int_or_nothing(argument: str) -> int:
    if not argument:
        return 999
    return int(argument)

class FlexTreeDirective(SphinxDirective):
    """
    Extension of the ``.. toctree::`` sphinx directive used to notify Sphinx about the hierarchical structure of the docs,
    and to include a table-of-contents like tree in the current document with descriptions and images.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'maxdepth': int,
        'name': directives.unchanged,
        'class': directives.class_option,
        'caption': directives.unchanged_required,
        'glob': directives.flag,
        'hidden': directives.flag,
        'includehidden': directives.flag,
        'numbered': int_or_nothing,
        'titlesonly': directives.flag,
        'reversed': directives.flag,
    }

    def run(self) -> List[Node]:
        subnode = FlexTreeNode()
        subnode['parent'] = self.env.docname

        # Initialize entries as a list of dictionaries
        subnode['entries'] = []  # List of dicts with keys: title, ref, description, image
        subnode['includefiles'] = []
        subnode['maxdepth'] = self.options.get('maxdepth', -1)
        subnode['caption'] = self.options.get('caption')
        subnode['glob'] = 'glob' in self.options
        subnode['hidden'] = 'hidden' in self.options
        subnode['includehidden'] = 'includehidden' in self.options
        subnode['numbered'] = self.options.get('numbered', 0)
        subnode['titlesonly'] = 'titlesonly' in self.options
        self.set_source_info(subnode)
        wrappernode = nodes.compound(
            classes=['toctree-wrapper flextree-wrapper', *self.options.get('class', ())],
        )
        wrappernode.append(subnode)
        self.add_name(wrappernode)

        ret = self.parse_content(subnode)
        ret.append(wrappernode)

        return ret

    def parse_content(self, toctree: FlexTreeNode) -> List[Node]:
        """
        Parses the content of the directive, extracting entries and their associated descriptions and images.
        """
        current_docname = self.env.docname
        glob = toctree['glob']
        all_docnames = self.env.found_docs.copy()
        all_docnames.discard(current_docname)

        included = Matcher(self.config.include_patterns)
        excluded = Matcher(self.config.exclude_patterns)

        entries: List[Dict[str, Any]] = []

        lines = self.content
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            # Check for explicit titles ("Some Title <document>")
            explicit = explicit_title_re.match(line)
            url_match = url_re.match(line) is not None

            if glob and glob_re.match(line) and not explicit and not url_match:
                # Handle glob patterns
                pat_name = docname_join(current_docname, line)
                doc_names = sorted(patfilter(all_docnames, pat_name))
                if not doc_names:
                    logger.warning(__("toctree glob pattern %r didn't match any documents"),
                                   line, location=toctree)
                for docname in doc_names:
                    entries.append({
                        'title': None,
                        'ref': docname,
                        'description': '',
                        'image': '',
                    })
                    toctree['includefiles'].append(docname)
                i += 1
                continue

            if explicit:
                ref = explicit.group(2)
                title = explicit.group(1)
            else:
                ref = line
                title = None

            # Collect description and image options
            description = ''
            image = ''
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith(':description:'):
                    description = next_line[len(':description:'):].strip()
                elif next_line.startswith(':image:'):
                    image = next_line[len(':image:'):].strip()
                elif next_line.startswith(':') and not next_line.startswith('::'):
                    # Skip other options (if any)
                    pass
                else:
                    break
                i += 1

            # Remove suffixes (backwards compatibility)
            for suffix in self.config.source_suffix:
                if ref.endswith(suffix):
                    ref = ref[:-len(suffix)]
                    break

            # Absolutize filenames
            ref = docname_join(current_docname, ref)

            if url_match or ref == 'self':
                entries.append({
                    'title': title,
                    'ref': ref,
                    'description': description,
                    'image': image,
                })
                i += 1
                continue

            if ref not in self.env.found_docs:
                if excluded(self.env.doc2path(ref, False)):
                    message = __('toctree contains reference to excluded document %r')
                    subtype = 'excluded'
                else:
                    message = __('toctree contains reference to nonexisting document %r')
                    subtype = 'not_readable'
                logger.warning(message, ref, type='toc', subtype=subtype,
                               location=toctree)
                self.env.note_reread()
                i += 1
                continue

            entries.append({
                'title': title,
                'ref': ref,
                'description': description,
                'image': image,
            })
            toctree['includefiles'].append(ref)
            i += 1

        if 'reversed' in self.options:
            entries.reverse()
            toctree['includefiles'].reverse()

        toctree['entries'] = entries

        return []

class FlexTreeNode(addnodes.toctree):
    """
    FlexTree Node for inserting a "TOC tree" with descriptions and images.
    """
    def preserve_original_messages(self) -> None:
        # Preserve original messages for translation
        rawentries: List[str] = self.setdefault('rawentries', [])

        for entry in self['entries']:
            title = entry['title']
            if title:
                rawentries.append(title)

        # :caption: option
        if self.get('caption'):
            self['rawcaption'] = self['caption']

    def apply_translated_message(self, original_message: str, translated_message: str) -> None:
        # Apply translated messages
        for entry in self['entries']:
            if entry['title'] == original_message:
                entry['title'] = translated_message

        # :caption: option
        if self.get('rawcaption') == original_message:
            self['caption'] = translated_message

    def extract_original_messages(self) -> List[str]:
        messages: List[str] = []

        # toctree entries
        messages.extend(self.get('rawentries', []))

        # :caption: option
        if 'rawcaption' in self:
            messages.append(self['rawcaption'])

        return messages

def visit_flex_treenode(self, node: FlexTreeNode) -> None:
    """
    Visitor function to process the FlexTreeNode during the build phase.
    """
    from sphinx.environment.adapters.toctree import TocTree

    # Resolve the toctree entries
    toctree = TocTree(self.builder.env).resolve(
        node['parent'],
        self.builder,
        node,
        prune=True,
        maxdepth=node['maxdepth'],
        titles_only=node['titlesonly'],
        collapse=False,
        includehidden=node['includehidden'],
    )

    if toctree:
        # Modify the toctree to include descriptions and images
        for entry_dict in node['entries']:
            title = entry_dict['title']
            ref = entry_dict['ref']
            description = entry_dict['description']
            image = entry_dict['image']

            # Find the corresponding list_item in the toctree
            for list_item in toctree.traverse(nodes.list_item):
                reference = list_item.traverse(nodes.reference)
                if reference and reference[0]['refuri'] == ref:
                    para = list_item.children[0]
                    # Add description if provided
                    if description:
                        desc_node = nodes.paragraph('', '', nodes.Text(description))
                        para += desc_node

                    # Add image if provided
                    if image:
                        image_node = nodes.image(uri=image)
                        para += image_node
                    break

        self.body.append(self.starttag(node, 'div', CLASS='toctree-wrapper flextree-wrapper'))
        self.body.append(self.starttag(toctree, 'ul', CLASS='simple'))
        for item in toctree.children:
            self.body.append(self.starttag(item, 'li'))
            self.body.append(item.astext())
            self.body.append('</li>')
        self.body.append('</ul></div>')
    else:
        # If no toctree could be resolved, render nothing
        pass

    raise nodes.SkipNode

def depart_flex_treenode(self, node: FlexTreeNode) -> None:
    pass

def setup(app):
    app.add_node(FlexTreeNode, html=(visit_flex_treenode, depart_flex_treenode))
    app.add_directive('flextree', FlexTreeDirective)

