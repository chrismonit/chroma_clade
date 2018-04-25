#!/usr/bin/python

from Bio import Phylo, AlignIO

class InputError(ValueError):
    pass

class Input:
    def __init__(self, tree_path, align_path, branches, tree_in_format,
            align_in_format, tree_out_format=None, start_site=None, end_site=None):
        
        # tree and alignment formats
        tree_in_format, align_in_format = tree_in_format.lower(), align_in_format.lower()

        if not tree_in_format in Phylo._io.supported_formats.keys():
            raise InputError("Oops: named tree format not recognised")
        else:
            self.tree_in_format = tree_in_format

        if not align_in_format in ["fasta", "nexus", "phylip", "phylip-relaxed", "phylip-sequential" ]: #AlignIO._FormatToIterator.keys()
            raise InputError("Oops: named alignment format not recognised")
        else:
            self.align_in_format = align_in_format
        
        # tree and alignment
        try:
            self.tree = Phylo.read(tree_path, tree_in_format) 
        except ValueError: # raised if 0 or >1 trees in file
            raise InputError("Oops: input tree file must contain exactly 1 tree")
        except IOError:
            raise InputError("Oops: can't find tree file")
        except Exception:
            raise InputError("Oops: problem reading tree file")
        
        self.tree_path = tree_path # keep this so output file name can be made later
        self.branches = branches 

        try:
            self.align = AlignIO.read(align_path, align_in_format)
        except ValueError: # raised if 0 or >1 alignments in file
            raise InputError("Oops: input alignment file must contain exactly 1 tree")
        except IOError:
            raise InputError("Oops: can't find alignment file")
        except Exception:
            raise InputError("Oops: problem reading alignment file")

        # tree out format
        if tree_out_format == None:
            self.tree_out_format = "figtree"
        else:
            tree_out_format = tree_out_format.lower()
            if not tree_out_format in ["figtree", "xml"]:
                raise InputError("Oops: named tree output format not recognised")
            else:
                self.tree_out_format = tree_out_format
        
        # start site (NB inclusive)
        if start_site == None:
            self.start_site = 0
        else:
            try:
                start_site = int(start_site)
            except Exception: # could be type error or value error
                raise InputError("Oops: start site must be interpretable as an integer")

            start_site = start_site - 1
            if start_site < 0 or start_site >= self.align.get_alignment_length():
                raise InputError("Oops: given start site must be within range of alignment length")
            else:
                self.start_site = start_site

        # end site (NB inclusive)
        if end_site == None:
            self.end_site = self.align.get_alignment_length() - 1
        else:
            try:
                end_site = int(end_site)
            except Exception: # could be type error or value error
                raise InputError("Oops: end site must be interpretable as an integer")

            end_site = end_site - 1
            if end_site < 0 or end_site >= self.align.get_alignment_length():
                raise InputError("Oops: given end site must be within range of alignment length")
            else:
                self.end_site = end_site



    # get methods
    def get_tree(self): return self.tree
    def get_align(self): return self.align
    def get_tree_in_format(self): return self.tree_in_format # probably not needed
    def get_align_in_format(self): return self.align_in_format # probably not needed
    def get_tree_out_format(self): return self.tree_out_format
    
    def get_start_site(self): return self.start_site
    def get_end_site(self): return self.end_site
    
    def get_tree_path(self): return self.tree_path
    def get_branches(self): return self.branches



def test():
    base_path = "/Users/cmonit1/Desktop/coloured_trees/"
    tree_path = base_path+"4tree.nwk.tre"
    align_path = base_path+"aln.fasta"
    #branches = False
    tree_in_format = "newick" 
    align_in_format = "fasta"
    tree_out_format = "figtree"
    start_site = None
    end_site = 5
    
    try:
        usr_input = Input(tree_path, align_path, False, tree_in_format, align_in_format, tree_out_format, start_site, end_site)
    except InputError as e:
        print str(e)

def main():
    test()

if __name__ == "__main__":
    main()
