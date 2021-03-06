# Katana
A Transposable Element (TE) parser and removal tool. This project's intended purpose is to parse through [.fasta](https://en.wikipedia.org/wiki/FASTA_format) files for their transpsoable elements. Transposable elements are defined as repetitive regions of DNA that can change their position within the genetic code of a cell; this sometimes induces mutations or amplifies the length of genetic sequences. Removal of these repetitive regions might allow easier sequencing of long genome files and is useful for observing the behavior of highly repetitive genomes.

## Usage
Katana works by taking commandline arguments involving a [RepeatMasker .out file](https://www.repeatmasker.org/webrepeatmaskerhelp.html#reading), a .fasta genome file (with seperate genomes being denoted by a '>[line]'), and a sequence of query genomes for the file output (seperated with the '-' character). Sample input would look like:

`python3 katana.py -f dm6.fa.out -c dMelanogasterChr4.fasta -q chr4`

For help, one would enter:

`python3 katana.py -h`

Katana generates it's own .fasta with a randomly removed number of TEs [**CURRENTLY A TEMPORARY FEATURE... THE TOOL WILL EVENTUALLY ALLOW THE USER TO DECIDE THE PERCENTAGE BY WHICH TES ARE RANDOMLY REMOVED. USERS WILL ALSO BE ABLE TO RELIABLY SELECT WHICH TES ARE REMOVED.**] in the same directory as katana.py.

### Process

Katana works  to create randomly sized offspring genome files. Transposable elements are removed in their entirety at random in order to create artificial variation within offsping files. 
* Katana does this by first collecting all TE positions from a given .out file and then removes them (at random) until a given percentage of TEs are left. 
* Katana then creates an output file named for the first genome queried (genome1).
* Katana parses through the given .fasta genome file starting with the queried genome. It will write all bases to the output file UNLESS it is part of a TE designated for removal. This ensures the original genoome is preserved and the selected TEs are removed.
* If there was more than one genome queried (genome2, genome3.... genomeN), Katana will generate new random TEs to remove for each genome using the .out file. Each result will be stored in a unique output file for the genome queried.

## Changelog
Version 1.0 - Initial Release.

Version 1.1 - 2/16/2020 Now takes multiple fasta files. An additional command line argument has been added to specify the specific chromosome you wish to splice from the repeatMasker file. Format should be relative to the .OUT repeatMasker file (ie. chr21 for <em>Homo sapiens</em> if sourced from http://www.repeatmasker.org/species/hg.html).

Version 1.2 - 2/18/2020 Now parses through a fasta file with multiple genomes. The previously added chromosome command has now been expanded to include multiple genome queries. If providing a fasta file with multiple genomes, specific the sequences to be spliced in order of appearance with a '-' to denote a different genome (ie. chr20-chr21 if working with an .OUT file from http://www.repeatmasker.org/species/hg.html). Further refinement is needed on command-line text as well specifying percentage of TEs to remove from command-line.
