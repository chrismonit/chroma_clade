#!/usr/bin/python
from Bio import Phylo
from Bio import AlignIO, SeqIO
from itertools import chain 
import os.path

from Bio.Nexus import Nexus 
from Bio.Phylo import Newick, NewickIO, PhyloXML
from Bio.Phylo.BaseTree import BranchColor
import copy

from check_input import *

AA_STATES = ["A", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "Y", "*", "-", "X"]
N_STATES = len(AA_STATES)

# TODO check these colours carefully
BLANK_BRANCH_COL = '#797D7F' # dark grey
COLOURS = { 'A':'#FF0000', 'C':'#009933', 'D':'#990000', 'E':'#FF0066', 'F':'#6666FF', 'G':'#00CC33', 'H':'#FFCC00', 'I':'#660066', 'K':'#CC3300', 'L':'#00CCFF', 'M':'#FF9900', 'N':'#FF9966', 'P':'#CC0099', 'Q':'#FF00CC', 'R':'#992600', 'S':'#336600', 'T':'#FF6699', 'V':'#FF66FF', 'W':'#0000FF', 'Y':'#0099FF', '*':BLANK_BRANCH_COL, '-':BLANK_BRANCH_COL, 'X':BLANK_BRANCH_COL }

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

# for running as a CLI app
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument( "tree", type=str)
    parser.add_argument( "alignment", type=str)
    parser.add_argument( "-b", action="store_true", help="Colour branches in addition to tip names")
    parser.add_argument( "-tf", metavar="<tree_format>", default="newick", type=str, help="Tree file format, 'newick' (default), 'nexus' or 'phyloxml'" )
    parser.add_argument( "-af", metavar="<alignment_format>", default="fasta", type=str, help="Alignment file format, 'fasta' (default) or 'nexus'" )
    parser.add_argument( "-s", metavar="<sites>", default=None, type=str, help="Specify subrange of alignment sites to make trees for, e.g. '18', or '2,4-6,10' etc." )
    parser.add_argument( "-o", metavar="<output_path>", default=None, type=str, help="Output file name or path (default is same directory as input tree file with 'col_' prefix added to file name)" )
    parser.add_argument( "-of", metavar="<output_format>", default="figtree", type=str, help="Output tree format, either FigTree-compatible Nexus (default) or Phylo-XML" )

    args = parser.parse_args()
    
    try:
        usr = Input(args.tree, args.alignment, args.b, args.tf, args.af, output_path=args.o, tree_out_format=args.of, sites_string=args.s)
    except InputError as e:
        print str(e)
        print ""
        parser.print_help()
        exit()
    
    run(usr)

# TODO check alignment and taxon names match, in case this causes an exception
# TODO could do with generic exception catch for anything unexpected
def run(usr):
    tree, aln = usr.get_tree(), usr.get_align()

    taxon_dict = dict([ (aln[i].id, i) for i in range(len(aln)) ]) # maps taxon identifiers to their alignment indices 

    trees = []
    for site in usr.get_sites():
        tree_copy = copy.deepcopy(tree)
        colour_tree(tree_copy.root, aln, taxon_dict, site)
        annotate_tips_only(tree_copy, aln, taxon_dict, site) # add site and state info
        trees.append(tree_copy)
    
    if usr.get_tree_out_format() == "xml":
        output_xml(trees, usr.get_output_path(), usr.get_branches())
    else:
        output_figtree(trees, usr.get_output_path(), usr.get_branches())




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


def output_figtree(coloured_trees, path, colour_branches):

    if colour_branches:
        for tree in coloured_trees:
            for clade in tree.get_nonterminals():
                clade.name = COL_ATTRIB % BranchColor.to_hex(clade.color) # colour is stored as RGB vector, but we want RGB hex
            for clade in tree.get_terminals():
                clade.name += COL_ATTRIB % BranchColor.to_hex(clade.color)
        tip_annotation_func = identity
    else:
        tip_annotation_func = colour_taxon

    f = open(path, "w")
    f.write(nexus_text(coloured_trees, tip_annotation_func).replace("'", ""))
    f.close()
    # the Bio code automatically adds inverted commas to colour attribute lables, which prevents figtree reading them as annotations


def annotate_tips_only(tree, alignment, taxon_dict, site, states=AA_STATES):
    """ Apply labels to tips showing site and state information (not colour)"""
    for tip in tree.get_terminals():
        state = alignment[ taxon_dict[tip.name] ][site].upper()
        tip.name += (STATE_SUFFIX % (site+1, state))

def colour_tree(parent, alignment, taxon_dict, site, states=AA_STATES):
    """ Apply colour labels to all tips and to branches, based on parsimony inference of
        ancestral characters, using a simplified form of Felsenstein's pruning algorithm.
        For an internal node, 'conditional probability' for a given state is 1
        if all descendent taxa are that state, and 0 otherwise.
        If there is any disagreement among descendent taxa then all 'conditional probabilities' 
        are 0, meaning we are not confident enough to assign any state to this branch.
    """
    if parent.is_terminal():
        state = alignment[ taxon_dict[parent.name] ][site].upper()
        parent.color = COLOURS[state] # stored as RGB tuple
        parent_vector = [0] * N_STATES 
        parent_vector[ AA_STATES.index(state) ] = 1
        return parent_vector
    else:
        parent_vector = [1] * N_STATES
        for child in parent:
            child_vector = colour_tree(child, alignment, taxon_dict, site, states=states)
            for i in range(N_STATES):
                parent_vector[i] *= child_vector[i] # elementwise multiplication
        z = sum(parent_vector)
        if z == 0:
            col = BLANK_BRANCH_COL
        elif z == 1:
            col = COLOURS[ AA_STATES[parent_vector.index(1)] ]
        else:
            raise ValueError("Incorrect parent vector!")
        parent.color = col # stored as RGB tuple
        return parent_vector

def colour_taxon(name, value_dict=COLOURS, n_chars=1, annotation_string=COL_ATTRIB):
    return name + annotation_string % value_dict[name[-n_chars]]

def identity(name): # use for no annotation
    return name


# TODO could include rooted/unrooted tree information, as is now standard in nexus format
def nexus_text(obj, tip_annotation_func, **kwargs):
    """ Take tree-like object(s) and create nexus-format representation.
        Allows for colouring tip names.
        Modified from http://biopython.org/DIST/docs/api/Bio.Phylo.NexusIO-pysrc.html
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
    tax_labels = [ tip_annotation_func(str(x.name)) for x in chain(*(t.get_terminals() for t in trees))] 
    text = NEX_TEMPLATE % { 
      'count': len(tax_labels), 
      'labels': ' '.join(tax_labels), # taxlabels all on one line 
      'trees': '\n'.join(nexus_trees), # trees on separate lines
    }
    return text

if __name__ == "__main__":
    main()
