#!/usr/bin/python
from Bio import Phylo
from Bio import AlignIO, SeqIO
from itertools import chain 
import os.path

from Bio.Nexus import Nexus 
from Bio.Phylo import Newick, NewickIO, PhyloXML
from Bio.Phylo.BaseTree import BranchColor
import copy
import re


from check_input import *


UNKNOWN_STATE_COL = '#797D7F' # dark grey

COL_ATTRIB = "[&!color=%s]"
STATE_SUFFIX = "__site_%d__%s"

# Structure of a Nexus tree-only file 
NEX_TEMPLATE = """#NEXUS 
Begin Taxa; 
Dimensions NTax=%(count)d; 
TaxLabels %(labels)s; 
End; 
Begin Trees; 
%(trees)s 
End;""" 
# 'index' starts from 1; 'tree' is the Newick tree string 
TREE_TEMPLATE = "Tree tree%(index)d=%(tree)s" # TODO could have rooting information here

GENERIC_ERR_MSG = """Oops: an error occured, please check input settings and try again. Message:"""

def main(): # for running as a CLI app
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument( "tree", type=str, help="File containing the unannotated tree")
    parser.add_argument( "alignment", type=str, help="File containing an alignment of the molecular sequences, either amino acids or nucleotides")
    parser.add_argument( "-tf", metavar="<tree_format>", default="newick", type=str, help="Tree file format, 'newick' (default), 'nexus' or 'phyloxml'" )
    parser.add_argument( "-af", metavar="<alignment_format>", default="fasta", type=str, help="Alignment file format, 'fasta' (default) or 'nexus'" )
    parser.add_argument( "-b", action="store_true", help="Colour branches in addition to tip names")
    parser.add_argument( "-s", metavar="<sites>", default=None, type=str, help="Specify subrange of alignment sites to make trees for, e.g. '18', or '2,4-6,10' etc." )
    parser.add_argument( "-o", metavar="<output_path>", default=None, type=str, help="Output file name or path (default is 'col_' prefix added to file name, saved in working directory)" )
    parser.add_argument( "-of", metavar="<output_format>", default="figtree", type=str, help="Output tree format, either FigTree-compatible Nexus (default) or Phylo-XML" )
    parser.add_argument( "-c", metavar="<colour_file>", default=None, type=str, help="A plain text file specifying sequence states and their associated colours, expressed in RGB hexidecimal code (https://htmlcolorcodes.com). One state/colour pair per line, separated by a comma" )

    args = parser.parse_args()
    
    try:
        colour_file_path = args.c if args.c != None else os.path.join(os.path.split(__file__)[0], Input.DEFAULT_COL_FILE)
        usr = Input(args.tree, args.alignment, args.b, args.tf, args.af, colour_file_path, output_path=args.o, tree_out_format=args.of, sites_string=args.s)
    except InputError as e:
        parser.print_help()
        print ""
        print str(e)
        exit()
    except Exception as e:
        print GENERIC_ERR_MSG
        print ""
        print "Exception: %s" % str(e)
        exit()
    
    try:
        run(usr)
    except Exception as e:
        print GENERIC_ERR_MSG
        print ""
        print "Exception: %s" % str(e)
        exit()

def run(usr):
    tree, aln = usr.get_tree(), usr.get_align()
    
    taxon_dict = dict([ (aln[i].id, i) for i in range(len(aln)) ]) # maps taxon identifiers to their alignment indices 
    
    trees = []
    for site in usr.get_sites():
        tree_copy = copy.deepcopy(tree)
        states = usr.get_colours().keys()
        colour_tree(tree_copy.root, aln, taxon_dict, site, usr.get_colours(), states)
        annotate_site_state(tree_copy, aln, taxon_dict, site) # add site and state info
        trees.append(tree_copy)
    
    if usr.get_tree_out_format() == "xml":
        output_xml(trees, usr.get_output_path(), usr.get_branches())
    else:
        output_figtree(trees, usr.get_output_path(), usr.get_branches(), usr.get_colours())




def output_xml(coloured_trees, path, colour_branches):
    
    # adding font as a property of each tip clade, to show colour
    coloured_trees = [ PhyloXML.Phylogeny.from_tree(tree) for tree in coloured_trees ]# convert to PhyloNexus
    for tree in coloured_trees:
        for clade in tree.get_terminals():
            value = BranchColor.to_hex(clade.color) # value of the property (ie the colour)
            clade.properties = [PhyloXML.Property(value, "style:font_color", "node", "xsd:token")]
        
        if not colour_branches: 
            for clade in tree.get_nonterminals() + tree.get_terminals():
                clade.color = None
    Phylo.write(coloured_trees, path, "phyloxml")


def output_figtree(coloured_trees, path, colour_branches, colours):

    if colour_branches:
        for tree in coloured_trees:
            for clade in tree.get_nonterminals():
                clade.name = COL_ATTRIB % BranchColor.to_hex(clade.color) # colour is stored as RGB vector, but we want RGB hex
            for clade in tree.get_terminals():
                clade.name += COL_ATTRIB % BranchColor.to_hex(clade.color)
    else:
        pass # colour labels added to taxlabel block in nexus_text

    f = open(path, "w")
    f.write(nexus_text(coloured_trees, colour_branches, colours).replace("'", ""))
    f.close()
    # the Bio code automatically adds inverted commas to colour attribute lables, which prevents figtree reading them as annotations


def annotate_site_state(tree, alignment, taxon_dict, site):
    """ Apply labels to tips showing site and state information (not colour)"""
    for tip in tree.get_terminals():
        state = alignment[ taxon_dict[tip.name] ][site].upper()
        tip.name += (STATE_SUFFIX % (site+1, state))

def colour_tree(parent, alignment, taxon_dict, site, colours, states):
    """ Apply colour labels to all tips and to branches, based on parsimony inference of
        ancestral characters, using a simplified form of Felsenstein's pruning algorithm.
        For an internal node, 'conditional probability' for a given state is 1
        if all descendent taxa are that state, and 0 otherwise.
        If there is any disagreement among descendent taxa then all 'conditional probabilities' 
        are 0, meaning we are not confident enough to assign any state to this branch.
    """
    if parent.is_terminal():
        state = alignment[ taxon_dict[parent.name] ][site].upper()
        parent_vector = [0] * len(states) 
        try:
            parent.color = colours[state] # color attribute stored as RGB tuple, even though value is hex representation
            parent_vector[ states.index(state) ] = 1
        except KeyError:
            parent.color = UNKNOWN_STATE_COL
        return parent_vector # if state is not recognised then parent_vector remains all 0
    else:
        parent_vector = [1] * len(states)
        for child in parent:
            child_vector = colour_tree(child, alignment, taxon_dict, site, colours, states)
            for i in range(len(states)):
                parent_vector[i] *= child_vector[i] # elementwise multiplication
        z = sum(parent_vector)
        if z == 0:
            col = UNKNOWN_STATE_COL
        elif z == 1:
            col = colours[ states[parent_vector.index(1)] ]
        else:
            raise ValueError("Incorrect parent vector!")
        parent.color = col # stored as RGB tuple
        return parent_vector

def colour_taxon(name, colours, n_chars=1, annotation_string=COL_ATTRIB):
    try:
        colour = colours[name[-n_chars]]
    except KeyError:
        colour = UNKNOWN_STATE_COL
    return name + annotation_string % colour

# TODO could include rooted/unrooted tree information, as is now standard in nexus format
def nexus_text(obj, colour_branches, colours, **kwargs):
    """ Take tree-like object(s) and create nexus-format representation.
        Allows for colouring tip names.
        Modified from http://biopython.org/DIST/docs/api/Bio.Phylo.NexusIO-pysrc.html
        NB here we compensate for an apparent bug in the Biopython implementation, 
        whereby an additional colon is wrongly added to confidence values in the output tree strings.
    """
    try:
        trees = list(obj) # assume iterable
    except TypeError:
        trees = [obj]
    writer = NewickIO.Writer(trees) 
    nexus_trees = [TREE_TEMPLATE % {'index': idx + 1, 'tree': nwk} 
                 for idx, nwk in enumerate( 
      writer.to_strings(plain=False, plain_newick=True, 
                        **kwargs))] 
    # if branches are being coloured, then taxon names already contain colouring annotation
    # otherwise we need to add this annotation here
    tax_labels = [ colour_taxon(str(x.name), colours) if not colour_branches else str(x.name) for x in chain(*(t.get_terminals() for t in trees))] 
    text = NEX_TEMPLATE % { 
      'count': len(tax_labels), 
      'labels': ' '.join(tax_labels), # taxlabels all on one line 
      'trees': '\n'.join(nexus_trees), # trees on separate lines
    }
    return re.sub(r':([0-9]{1,3}\.[0-9]{1,3}):', r'\1:', text) # Corrects for biopython bug. eg ":50.00:" -> "50.00:"

if __name__ == "__main__":
    main()
