# context-builder
builds a pds4 context_area xml doc for data generation testing purposes

in order to run it, run "python inputgenerator.py" and then follow the prompt

it will generate intermediate files as well as context area xml files.

There is a bash script clean.sh  that should remove all of the generated files.

if you wish to write your own files, follow the template in sample-input and you can look at generated files for examples, run python inputprocessor.py in order to input self writted input files. 

most fields are not optional when writing your own files - follow generated files and sample-inputs example
