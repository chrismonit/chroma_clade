# ChromaClade

<p align="center">
<img src="docs/logo.jpg" alt="ChromaClade" width="200"/>
</p>

ChromaClade is a desktop application for producing  colour-annotated phylogenetic trees that show amino acids found in each taxon and at each site in protein.

This repository houses ChromaClade executables, documentation, example input/output and its source code. ChromaClade as been developed and distributed by Christopher Monit.

If you use ChromaClade please cite
> Monit, C., Goldstein, R. A. and Towers, G. J., (submitted) ChromaClade: Combined visualisation of phylogenetic and sequence data 


## Installation
Pre-compiled apps are available for the following systems.

**Windows:** found in 'apps/windows/chroma_clade.exe' from the links above.

**Mac OSX:** found in 'apps/macosx/chroma_clade.app' from the links above.

## Instructions
### Graphical interface

<p align="center">
<img src="docs/gui.jpg" alt="GUI" width="300"/>
</p>


### Input
Use the buttons to select the files containing your tree and your corresponding alignment. 

Use the dropdown to select the **file format** for your input files: either [Newick](https://en.wikipedia.org/wiki/Newick_format) or [Nexus](https://en.wikipedia.org/wiki/Nexus_file) format for trees and [Fasta](https://en.wikipedia.org/wiki/FASTA_format) or Nexus format for alignment. Tools are available for converting between tree formats (e.g. [here](http://phylogeny.lirmm.fr/phylo_cgi/data_converter.cgi)) and alignment formats (e.g. [here](https://www.ebi.ac.uk/Tools/sfc/emboss_seqret/)).

The alignment would ordinarily be amino acid sequences (e.g. translated from the nucleotide sequences used to first estimate the tree) but the method will work perfectly well with nucleotide states too. 

### Output

The output is a set of trees saved to a single file, where taxon names have been annotated according to the amino acid found in that taxon's sequence. E.g. if methionine is found at position 1 in the human sequence, then 

> human

becomes

> human__site_1__M

In addition, the taxon name will be assigned a colour specific to methionine.

Use the dropdown to select the **output file format** for the output file, either a Nexus format file specifically compatible with the [FigTree](http://tree.bio.ed.ac.uk/software/figtree/) tree viewer, or the PhyloXML format compatible with other viewers such as [Archaeopteryx](https://sites.google.com/site/cmzmasek/home/software/archaeopteryx).

Click **Save as** to choose where to save the output.


### Options

Branches can also be coloured by amino acids observed in descendent taxa, by clicking the **Colour branches** checkbox. Annotated trees can be made for a subset of sites by clicking the **Choose sites** checkbox and entering the site ranges to include, just as you would specify pages of a document to print.

## Command Line Interface

ChromaClade also has a CLI (i.e. terminal-based interface) which should run on any system where [Python 2.7](https://www.python.org/downloads/) and [Biopython](https://pypi.org/project/biopython/) are installed.

Basic usage:
`$ cd chroma_clade/src`

`$ python2 chroma_clade.py <newick_tree_file> <fasta_alignment>`

For more information and options, run 

`$ python2 chroma_clade.py -h`

## License 

See `LICENSE.txt` file.

> This README.md is written with [StackEdit](https://stackedit.io/).
