# Katana
Transposable Element Scraper and Removal Tool.

Version 1.1 - 2/16/2020 Now takes multiple fasta files. An additional command line argument has been added to specify the specific chromosome you wish to splice from the repeatMasker file. Format should be relative to the .OUT repeatMasker file (ie. chr21 for <em>Homo sapiens</em> if sourced from http://www.repeatmasker.org/species/hg.html).

Version 1.2 - 2/18/2020 Now parses through a fasta file with multiple genomes. The previously added chromosome command has now been expanded to include multiple genome queries. If providing a fasta file with multiple genomes, specific the sequences to be spliced in order of appearance with a '-' to denote a different genome (ie. chr20-chr21 if working with an .OUT file from http://www.repeatmasker.org/species/hg.html). Further refinement is needed on command-line text.
