#!/usr/bin/python

from Bio import Phylo, AlignIO
import os.path

OUT_PREFIX = "col_"
SITES_DELIM = ","
RANGE_DELIM = "-"
COLOUR_DELIM = ","

class InputError(ValueError):
    pass

class Input:

    DEFAULT_COL_FILE = "default_colour.csv"

    def __init__(self, tree_path, align_path, branches, tree_in_format,
            align_in_format, colour_file_path, output_path=None, tree_out_format=None, 
            sites_string=""):
        
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
            raise InputError("Oops: input tree file must contain exactly 1 tree.\n(Is the specified format correct?)")
        except IOError:
            raise InputError("Oops: can't find tree file")
        except Exception:
            raise InputError("Oops: problem reading tree file")
        
        self.tree_path = tree_path # keep this so output file name can be made later
        self.branches = branches 

        try:
            self.align = AlignIO.read(align_path, align_in_format)
        except ValueError: # raised if 0 or >1 alignments in file
            raise InputError("Oops: input alignment file must contain exactly 1 alignment.\n(Is the specified format correct?)")
        except IOError:
            raise InputError("Oops: can't find alignment file")
        except Exception:
            raise InputError("Oops: problem reading alignment file")
        
        # validate tree/alignment content
        if set([ clade.name for clade in self.tree.get_terminals()]) != set([ seq.id for seq in self.align ]):
            raise InputError("Oops: sequence names in tree and alignment don't match")

        # output file path
        if output_path == None:
            directory, filename = os.path.split( os.path.abspath(self.tree_path) )
            self.output_path = directory + "/" + (OUT_PREFIX + filename) 
        else:
            directory = os.path.split( os.path.abspath(output_path) )[0]
            if not os.path.exists(directory):
                raise InputError("Oops: can't find the given folder for saving output")
            else:
                self.output_path = output_path

        # tree out format
        if tree_out_format == None:
            self.tree_out_format = "figtree"
        else:
            tree_out_format = tree_out_format.lower()
            if not tree_out_format in ["figtree", "xml"]:
                raise InputError("Oops: named tree output format not recognised")
            else:
                self.tree_out_format = tree_out_format
        
        # parse site ranges
        # NB we don't sort or remove duplicate site numbers, so user can control order and frequency
        try:
            if not sites_string or sites_string.isspace(): # if string is not empty or is all white space 
                self.sites = range(self.align.get_alignment_length())
            elif not any(char.isdigit() for char in sites_string):
                raise InputError("Oops: no digits given for site numbers")
            else:
                input_sites = map(lambda x: x-1, self._parse_sites(sites_string, SITES_DELIM) ) # -1 to make zero based 
                for input_site in input_sites:
                    if not (0 <= input_site < self.align.get_alignment_length()):
                        raise InputError("Oops: specified site number(s) outside alignment length")
                self.sites = input_sites
        except InputError as e:
            raise e
        except Exception as e:
            raise InputError("Oops: don't understand the specified alignment sites")
        
        # parse colour codes
        try:
            f = open(colour_file_path)
            self.colours = dict([ tuple(l.strip().split(COLOUR_DELIM)) for l in f.readlines() if not l.isspace() ])
            f.close()
        except IOError as e:
            raise InputError("Oops: can't find file containing colour codes")
        except Exception as e:
            raise InputError("Oops: problem reading file containing colour codes")

    
    def _parse_sites(self, sites_string, delim):
        sections = ("".join(sites_string.split())).split(delim) # remove all white space and then split on delim
        sites = []
        for section in filter(None, sections): # iterate over non-empty strings
            if RANGE_DELIM in section:
                a, b = section.split(RANGE_DELIM )
                a, b = int(a), int(b)
                if a > b:
                    raise ValueError("Invalid range argument: '%s' (%d > %d)" % (section, a, b))
                sites.extend(range(a, b + 1))
            else:
                a = int(section)
                sites.append(a)
        return sites

    # get methods
    def get_tree(self): return self.tree
    def get_align(self): return self.align
    def get_tree_in_format(self): return self.tree_in_format # probably not needed
    def get_align_in_format(self): return self.align_in_format # probably not needed
    def get_output_path(self): return self.output_path
    def get_tree_out_format(self): return self.tree_out_format
    
    def get_start_site(self): return self.start_site
    def get_end_site(self): return self.end_site
    
    def get_tree_path(self): return self.tree_path
    def get_branches(self): return self.branches
    
    def get_sites(self): return self.sites
    def get_colours(self): return self.colours

def test():
    base_path = "/Users/cmonit1/Desktop/coloured_trees/"
    tree_path = base_path+"4tree.nwk.tre"
    align_path = base_path+"aln.fasta"
    branches = False
    tree_in_format = "newick" 
    align_in_format = "fasta"
    outpath = base_path + "test_checkinput.txt"
    tree_out_format = "figtree"
    start_site = None
    end_site = 4
    sites_string = "1-4"
    colour_file = "/Users/cmonit1/Desktop/coloured_trees/chroma_clade/src/dat/default_colour.csv"
    
    try:
        usr_input = Input(tree_path, align_path, branches, tree_in_format, 
                align_in_format, outpath, tree_out_format, sites_string, colour_file
                )
    except InputError as e:
        print str(e)
        exit()
    

def main():
    test()

if __name__ == "__main__":
    main()
