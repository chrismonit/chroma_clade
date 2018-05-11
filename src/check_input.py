#!/usr/bin/python

from Bio import Phylo, AlignIO
import os.path

OUT_PREFIX = "col_"
SITES_DELIM = ","
RANGE_DELIM = "-"

class InputError(ValueError):
    pass

class Input:
    def __init__(self, tree_path, align_path, branches, tree_in_format,
            align_in_format, output_path=None, tree_out_format=None, 
            start_site=None, end_site=None, sites_string=""):
        
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
            raise InputError("Oops: input tree file must contain exactly 1 tree. Is the specified format correct?")
        except IOError:
            raise InputError("Oops: can't find tree file")
        except Exception:
            raise InputError("Oops: problem reading tree file")
        
        self.tree_path = tree_path # keep this so output file name can be made later
        self.branches = branches 

        try:
            self.align = AlignIO.read(align_path, align_in_format)
        except ValueError: # raised if 0 or >1 alignments in file
            raise InputError("Oops: input alignment file must contain exactly 1 alignment. Is the specified format correct?")
        except IOError:
            raise InputError("Oops: can't find alignment file")
        except Exception:
            raise InputError("Oops: problem reading alignment file")
        
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
        
        # NB we don't sort of remove duplicate site numbers, so user can control order and frequency
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

    import sys
    sites_string = sys.argv[1] 
    #sites_string = "1,2,3-4"
    
    print "input:", repr(sites_string)

    try:
        usr_input = Input(tree_path, align_path, branches, tree_in_format, 
                align_in_format, outpath, tree_out_format, start_site, end_site, 
                sites_string)
    except InputError as e:
        print str(e)
        exit()
    
    print "result", usr_input.get_sites()

def main():
    test()

if __name__ == "__main__":
    main()
