# hchacha - Human CHromosome Accession CHange

Translate among the different naming systems used for human chromosomes (of the same assembly)

## Background

There are a number of different groups that participant in and/or provide reference human sequence
data from the [Genome Reference Consortium](http://genomereference.org). However, the same reference
sequence data for each chromosome get accessioned under different identifiers. This script converts
among these identifiers (just within versions-- this is not a crossMap or liftOver), for several
commonly-used file formats, including VCF, SAM, FASTA, chain files...

Why? Well, there are several conventions for the naming of human chromosomes. The "ensembl" style
numbers them 1-22 then X and Y. The "ucsc" style (named after the UCSC genome browser, also
used in GATK's reference bundles) prepends these with 'chr'. However, a downside of both of these
is that '11' or 'chr11' do not uniquely identify a sequence (although they may in the context
of a specific assembly version like GRCh38.p13. On the other hand, 'NC_000011.10' is a specific
accessioned sequence (which happens to be the chromosome 11 sequence version used in the
GRCh38 primary assembly. Likewise, the genbank accession rather than the refseq accession could
be used.

## Examples

```
hchacha --help
```

```
zcat input.vcf.gz | hchacha vcf -a 37 -t ensembl | bgzip -c > output.vcf.gz
```

```
samtools view -h input.bam | hchacha sam -a 38 -t refseq | samtools view -b > output.bam
```

## Smarter handling for BAM/CRAM files

Since all you are doing is really renaming the sequences in the header (and individual BAM/CRAM records
refer back to those sequence names by an integer index), you can do things much more quickly and with
less CPU usage using `samtools reheader` if it is available on your system.

For example:

```bash
samtools reheader -P -c 'python3 hchacha sam -a 38 -t ucsc -s' input.bam > output.bam
```

With some clever use of the `tee` command to output the new bam file and continue the shell pipeline
going, you can even make the new index at the same time:

```bash
samtools reheader -P -c 'python3 hchacha.py sam -a 38 -t ucsc -s' input.bam | tee output.bam | samtools index - output.bam.bai
```

```

## Data used

NCBI provides a useful file (*.assembly_report.txt) for different GRCh reference versions and patch
levels, for instance [here](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_assembly_report.txt),
that maps among these names. To get the data included in the repository (for GRCh versions 37 and 38), I
did the following:

```
curl https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_assembly_report.txt | gzip -9 > src/hchacha/data/GCF_000001405.39_GRCh38.p14_assembly_report.txt.gz

curl https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.25_GRCh37.p13/GCF_000001405.25_GRCh37.p13_assembly_report.txt | gzip -9 > src/hchacha/data/GCF_000001405.25_GRCh37.p13_assembly_report.txt.gz
```

Changing the above (like for new patch levels) would also require changing the relevant filenames in the script.

The mapping to ensEMBL names is not quite as straightforward. It looks
like they use the "short" names (like 1, 2, 3, ... X, Y) for the primary chromosomes, then RefSeq
accessions for the others, so that is what this script does.

## License

MIT license, but I am open to re-licensing this simple to script some other way if you have a good reason.

It is my understandig that data derived from RefSeq/NCBI are in the public domain as the work
product of an institution of the governement of the United States of America.
