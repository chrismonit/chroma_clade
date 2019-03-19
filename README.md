# ChromaClade

<p align="center">
<img src="docs/logo.jpg" alt="ChromaClade" width="200"/>
</p>

ChromaClade is a desktop application for producing  colour-annotated phylogenies that show amino acids found in each taxon and at each site in protein.

This repository houses ChromaClade executables, documentation, example input/output and its source code. ChromaClade as been developed and distributed by Christopher Monit.

If you use ChromaClade please cite
> Monit, C., Goldstein, R. A. and Towers, G. J., (submitted) ChromaClade: Combined visualisation of phylogenetic and sequence data 



## Installation
Pre-compiled apps are available for the following systems.

**Windows:** found in apps/windows/chroma_clade.exe from the links above.

**Mac OSX:** found in apps/macosx/chroma_clade.app from the links above.

## Instructions
### Graphical interface

<p align="center">
<img src="docs/gui.jpg" alt="GUI" width="200"/>
</p>


### Input
Use the buttons to select the files containing your tree and your corresponding alignment. 

Use the dropdown to select the file formats for your input files: either [Newick](https://en.wikipedia.org/wiki/Newick_format) or [Nexus](https://en.wikipedia.org/wiki/Nexus_file) format for trees and [Fasta](https://en.wikipedia.org/wiki/FASTA_format) or Nexus format for alignment. Tools are available for converting between tree formats (e.g. [here](http://phylogeny.lirmm.fr/phylo_cgi/data_converter.cgi)) and alignment formats (e.g. [here](https://www.ebi.ac.uk/Tools/sfc/emboss_seqret/)).

The alignment would ordinarily be amino acid sequences (e.g. translated from the nucleotide sequences used to first estimate the tree) but the method will work perfectly well with nucleotide states too. 

### Output

The output is a set of trees saved to a single file, where taxon names have been annotated and coloured according to the amino acid found in that taxon's sequence. E.g. if methionine is found at position 1 in the human sequence, then 

<p>
<font color="black">human</font>
</p>

becomes

<p>
<font color="#FF9900">human__site_1__M</font>
</p>

Use the dropdown to select the file formats for the output file, either a Nexus format file specifically compatible with the [FigTree](http://tree.bio.ed.ac.uk/software/figtree/) tree viewer, or the PhyloXML format compatible with other viewers such as [Archaeopteryx](https://sites.google.com/site/cmzmasek/home/software/archaeopteryx).

Click **Save as** to choose where to save the output.

### Colours

Unfortunately it is impossible to select 20 starkly different colours, so the contrast will vary between combinations of residues. The colours are defines as follows:

<p>
<font color="#FF0000">A</font>
<font color="#009933">C</font>
<font color="#FF0066">E</font>
<font color="#990000">D</font>
<font color="#00CC33">G</font>
<font color="#6666FF">F</font>
<font color="#660066">I</font>
<font color="#FFCC00">H</font>
<font color="#CC3300">K</font>
<font color="#FF9900">M</font>
<font color="#00CCFF">L</font>
<font color="#FF9966">N</font>
<font color="#FF00CC">Q</font>
<font color="#CC0099">P</font>
<font color="#336600">S</font>
<font color="#992600">R</font>
<font color="#FF6699">T</font>
<font color="#0000FF">W</font>
<font color="#FF66FF">V</font>
<font color="#0099FF">Y</font>
<font color="#797D7F">X</font>
<font color="#797D7F">\*</font>
<font color="#797D7F">-</font>
</p>






### Options

Branches can also be coloured by amino acids observed in descendent taxa, simply by clicking the **Colour branches** checkbox. Annotated trees can be made for a subset of sites by clicking the **Choose sites** checkbox and entering the site ranges to include, just as you would specify which of a document's pages to be printed.

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
