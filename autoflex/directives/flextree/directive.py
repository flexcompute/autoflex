from __future__ import annotations

import re
from typing import TYPE_CHECKING

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.addnodes import toctree
from sphinx.domains.changeset import VersionChange  # NoQA: F401  # for compatibility
from sphinx.domains.std import StandardDomain
from sphinx.locale import _, __
from sphinx.util import docname_join, logging, url_re
from sphinx.util.docutils import SphinxDirective
from sphinx.util.matching import Matcher, patfilter
from sphinx.util.nodes import explicit_title_re

if TYPE_CHECKING:
    from docutils.nodes import Node


glob_re = re.compile(r'.*[*?\[].*')
logger = logging.getLogger(__name__)


def int_or_nothing(argument: str) -> int:
    if not argument:
        return 999
    return int(argument)


class FlexTreeDirective(SphinxDirective):
    # Note most of the source code is just a modified version of the toctree
    # Only valid from sphinx 7+
    # TODO maybe make a PR to sphinx directly.
    """
    Extension of the ``.. toctree::`` sphinx directive used to notify Sphinx about the hierarchical structure of the docs,
    and to include a table-of-contents like tree in the current document.

    Notes
    -----

    A customizable toctree directive with options to create
     links with descriptions, custom formatting, and interactive features. Ideally this feature should be developed
    in an extensible way building on top of the existing ``toctree`` directive.

    Usage
    -----

    The usage should be broadly compatible with the existing ``.. toctree::`` directive in the structures they represent.
    However, there is more flexibility in the way the tree is generated and the parameters that can be passed.

    To add descriptions below the given generated links, the following syntax can be used:

    .. code::

        .. flextree::
            :maxdepth: 2

            mypage1/
                :description: This is the description of the page.
            mypage2/
                :description: This is the description of the page.

    If we want to add an image thumbnail when this is generated accordingly:

    .. code::

        .. flextree::
            :maxdepth: 2

            mypage1/
                :image: path/to/image.png
            mypage2/
                :image: path/to/image.png

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

    def run(self) -> list[Node]:
        subnode = FlexTreeNode()
        subnode['parent'] = self.env.docname

        # (title, ref) pairs, where ref may be a document, or an external link,
        # and title may be None if the document's title is to be used
        subnode['entries'] = []
        subnode['descriptions'] = []
        subnode['images'] = []
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

        logger.info("ret")
        logger.info(ret)

        return ret

    def parse_content(self, toctree: FlexTreeNode) -> list[Node]:
        """
        The way this works is that each toctree entry is parsed and added to the toctree node. We consider the entry
        as the main top level. Based on the directive content, we can add descriptions, images, and other customizations.
        Each previous entry is stored until the next entry is found.

        The main goal is to extend the toctree directive to allow for more flexibility in the way the tree is generated.
        """
        generated_docnames = frozenset(StandardDomain._virtual_doc_names)
        suffixes = self.config.source_suffix
        current_docname = self.env.docname

        glob = toctree['glob']

        # glob target documents
        all_docnames = self.env.found_docs.copy() | generated_docnames
        all_docnames.remove(current_docname)  # remove current document
        frozen_all_docnames = frozenset(all_docnames)

        ret: list[Node] = []
        excluded = Matcher(self.config.exclude_patterns)
        previous_entry = None
        for entry in self.content:
            if not entry:
                continue

            # Here we need to add the extended parsing, whilst maintaining the existing titles, and being flexible
            # enough for the descriptions and images

            # If a :description: is found, we generate the content accordingly
            # We want to generate the content under the title link of the entry
            if ':description:' in entry:
                parts = entry.split(':description:')
                description = parts[1].strip() if len(parts) > 1 else ""
                toctree['descriptions'].append((previous_entry, description))
                continue

            # If an :image: is found, we generate the content accordingly
            # We want to generate the content under the title link of the entry
            if ':image:' in entry:
                parts = entry.split(':image:')
                image = parts[1].strip() if len(parts) > 1 else ""
                toctree['images'].append((previous_entry, image))
                continue

            # TODO here
            logger.info("entry")
            logger.info(entry)

            # look for explicit titles ("Some Title <document>")
            explicit = explicit_title_re.match(entry)
            url_match = url_re.match(entry) is not None
            if glob and glob_re.match(entry) and not explicit and not url_match:
                pat_name = docname_join(current_docname, entry)
                doc_names = sorted(patfilter(all_docnames, pat_name))
                for docname in doc_names:
                    if docname in generated_docnames:
                        # don't include generated documents in globs
                        continue
                    all_docnames.remove(docname)  # don't include it again
                    toctree['entries'].append((None, docname))
                    toctree['includefiles'].append(docname)
                if not doc_names:
                    logger.warning(__("toctree glob pattern %r didn't match any documents"),
                                   entry, location=toctree)
                continue

            if explicit:
                ref = explicit.group(2)
                title = explicit.group(1)
                docname = ref
            else:
                ref = docname = entry
                title = None

            # remove suffixes (backwards compatibility)
            for suffix in suffixes:
                if docname.endswith(suffix):
                    docname = docname.removesuffix(suffix)
                    break

            # absolutise filenames
            docname = docname_join(current_docname, docname)
            if url_match or ref == 'self':
                toctree['entries'].append((title, ref))
                continue

            if docname not in frozen_all_docnames:
                if excluded(self.env.doc2path(docname, False)):
                    message = __('toctree contains reference to excluded document %r')
                    subtype = 'excluded'
                else:
                    message = __('toctree contains reference to nonexisting document %r')
                    subtype = 'not_readable'

                logger.warning(message, docname, type='toc', subtype=subtype,
                               location=toctree)
                self.env.note_reread()
                continue

            if docname in all_docnames:
                all_docnames.remove(docname)
            else:
                logger.warning(__('duplicated entry found in toctree: %s'), docname,
                               location=toctree)

            toctree['entries'].append((title, docname))
            toctree['includefiles'].append(docname)
            previous_entry = entry

        # entries contains all entries (self references, external links etc.)
        if 'reversed' in self.options:
            toctree['entries'] = list(reversed(toctree['entries']))
            toctree['includefiles'] = list(reversed(toctree['includefiles']))

        logger.info("toc entries")
        logger.info(toctree["entries"])

        logger.info("ret at parse content")
        logger.info(ret)

        return ret


class FlexTreeNode(nodes.General, nodes.Element, addnodes.translatable):
    """
    Note that the node generated by a ``toctree`` is simply a ``compound`` class
    in ``docutils.nodes`` in the form:

    .. code::

        compound(General, Element)

    This is the type of class we want to overwrite in order to add the custom styling we are more keen on implementing.
    """
    # Flextree Node for inserting a "TOC tree"

    def preserve_original_messages(self) -> None:

        # toctree entries
        logger.info("flexnode entries")
        logger.info(self)
        logger.info(self['entries'])
        logger.info(self["descriptions"])
        logger.info(self["images"])

        rawentries: list[str] = self.setdefault('rawentries', [])

        for title, _docname in self['entries']:
            if title:
                rawentries.append(title)

        # :caption: option
        if self.get('caption'):
            self['rawcaption'] = self['caption']

    def apply_translated_message(self, original_message: str, translated_message: str) -> None:
        # toctree entries
        for i, (title, docname) in enumerate(self['entries']):
            if title == original_message:
                self['entries'][i] = (translated_message, docname)

        logger.info("flexnode entries")
        logger.info(self)
        logger.info(self['entries'])

        # :caption: option
        if self.get('rawcaption') == original_message:
            self['caption'] = translated_message

    def extract_original_messages(self) -> list[str]:
        messages: list[str] = []

        # toctree entries
        messages.extend(self.get('rawentries', []))

        # :caption: option
        if 'rawcaption' in self:
            messages.append(self['rawcaption'])

        return messages
