# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hchacha']

package_data = \
{'': ['*'], 'hchacha': ['data/*']}

entry_points = \
{'console_scripts': ['hchacha = hchacha:cli']}

setup_kwargs = {
    'name': 'hchacha',
    'version': '1.0.2',
    'description': 'Human CHromosome Accession CHAnge - Convert between different human chromosome naming systems (of the same assembly/version)',
    'long_description': '# hchacha - Human CHromosome Accession CHange\n\nTranslate among the different naming systems used for human chromosomes (of the same assembly)\n\n## Background\n\nThere are a number of different groups that participant in and/or provide reference human sequence\ndata from the [Genome Reference Consortium](http://genomereference.org). However, the same reference\nsequence data for each chromosome get accessioned under different identifiers. This script converts\namong these identifiers (just within versions-- this is not a crossMap or liftOver), for several\ncommonly-used file formats, including VCF, SAM, FASTA, chain files...\n\nWhy? Well, there are several conventions for the naming of human chromosomes. The "ensembl" style\nnumbers them 1-22 then X and Y. The "ucsc" style (named after the UCSC genome browser, also\nused in GATK\'s reference bundles) prepends these with \'chr\'. However, a downside of both of these\nis that \'11\' or \'chr11\' do not uniquely identify a sequence (although they may in the context\nof a specific assembly version like GRCh38.p13. On the other hand, \'NC_000011.10\' is a specific\naccessioned sequence (which happens to be the chromosome 11 sequence version used in the\nGRCh38 primary assembly. Likewise, the genbank accession rather than the refseq accession could\nbe used.\n\n## Examples\n\n```\nhchacha --help\n```\n\n```\nzcat input.vcf.gz | hchacha vcf -a 37 -t ensembl | bgzip -c > output.vcf.gz\n```\n\n```\nsamtools view -h input.bam | hchacha sam -a 38 -t refseq | samtools view -b > output.bam\n```\n\n## Smarter handling for BAM/CRAM files\n\nSince all you are doing is really renaming the sequences in the header (and individual BAM/CRAM records\nrefer back to those sequence names by an integer index), you can do things much more quickly and with\nless CPU usage using `samtools reheader` if it is available on your system.\n\nFor example:\n\n```bash\nsamtools reheader -P -c \'python3 hchacha sam -a 38 -t ucsc -s\' input.bam > output.bam\n```\n\nWith some clever use of the `tee` command to output the new bam file and continue the shell pipeline\ngoing, you can even make the new index at the same time:\n\n```bash\nsamtools reheader -P -c \'python3 hchacha.py sam -a 38 -t ucsc -s\' input.bam | tee output.bam | samtools index - output.bam.bai\n```\n\n```\n\n## Data used\n\nNCBI provides a useful file (*.assembly_report.txt) for different GRCh reference versions and patch\nlevels, for instance [here](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_assembly_report.txt),\nthat maps among these names. To get the data included in the repository (for GRCh versions 37 and 38), I\ndid the following:\n\n```\ncurl https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_assembly_report.txt | gzip -9 > src/hchacha/data/GCF_000001405.39_GRCh38.p14_assembly_report.txt.gz\n\ncurl https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.25_GRCh37.p13/GCF_000001405.25_GRCh37.p13_assembly_report.txt | gzip -9 > src/hchacha/data/GCF_000001405.25_GRCh37.p13_assembly_report.txt.gz\n```\n\nChanging the above (like for new patch levels) would also require changing the relevant filenames in the script.\n\nThe mapping to ensEMBL names is not quite as straightforward. It looks\nlike they use the "short" names (like 1, 2, 3, ... X, Y) for the primary chromosomes, then RefSeq\naccessions for the others, so that is what this script does.\n\n## License\n\nMIT license, but I am open to re-licensing this simple to script some other way if you have a good reason.\n\nIt is my understandig that data derived from RefSeq/NCBI are in the public domain as the work\nproduct of an institution of the governement of the United States of America.\n',
    'author': 'Bradford Powell',
    'author_email': 'bpow@drpowell.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://bitbucket.org/bpow/hchacha',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
