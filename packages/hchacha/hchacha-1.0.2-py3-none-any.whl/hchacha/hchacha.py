#!/usr/bin/env python

import sys
import argparse
import re
import collections
import gzip
import os.path

contig_pattern = re.compile(r"##contig=<ID=([^,]+),(.*)")


def make_translation(assembly="38", target="refseq", silent=False):
    # Read the appropriate mappings of chromosome names
    # data originally from location like:
    # https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.38_GRCh38.p12/GCF_000001405.38_GRCh38.p12_assembly_report.txt
    if assembly == "37":
        assembly_report = "data/GCF_000001405.25_GRCh37.p13_assembly_report.txt.gz"
    elif assembly == "38":
        assembly_report = "data/GCF_000001405.39_GRCh38.p14_assembly_report.txt.gz"
    else:
        raise RuntimeError("Assembly %s is not recognized" % assembly)

    assembly_report = os.path.join(os.path.dirname(__file__), assembly_report)

    # ensembl uses Sequence-Name for full chromosomes, otherwise Genbank-Accn
    # GenBank and RefSeq use GenBank-Accn and Refseq-Accn (of course...)
    # UCSC uses UCSC-style-name

    mapping = dict()
    columns = "Sequence-Name Sequence-Role Assigned-Molecule Assigned-Molecule-Location/Type GenBank-Accn Relationship RefSeq-Accn Assembly-Unit Sequence-Length UCSC-style-name".split()
    target_column = {"ensembl": 4, "genbank": 4, "refseq": 6, "ucsc": 9}[target]

    for row in (
        line.rstrip().split("\t")
        for line in gzip.open(assembly_report, "rt")
        if not line.startswith("#")
    ):
        # The GRCh38.p12 file seems to have a bug in it...
        if row[4] == "KI270752.1":
            row[6] = "NT_187507.1"
        translated = row[target_column]
        # handle chromosomes in ensembl-- use shortened name
        if target == "ensembl" and (
            translated.startswith("CM") or translated.startswith("J")
        ):
            translated = row[0]
        for alias in (row[i] for i in (0, 4, 6, 9)):
            mapping[alias] = translated

    def translate(key):
        """returns the corresponding mapped sequence name, but behavior when there is a KeyError depends on the "silent" setting"""
        try:
            return mapping[key]
        except KeyError:
            if silent:
                return key
            else:
                raise Exception('identifier "%s" not found for %s' % (key, target))

    return translate


def separated_values(
    inf=sys.stdin,
    assembly="38",
    target="refseq",
    silent=False,
    column=1,
    delimiter="\t",
    subformat=None,
    **kwargs,
):
    translate = make_translation(assembly, target, silent)
    column = int(column) - 1
    for line in inf:
        if subformat == "vcf":
            # special handling for header lines-- most pass-through, but translate the 'contig' lines
            if line.startswith("#"):
                if line.startswith("##contig=<"):
                    m = contig_pattern.match(line)
                    if m:
                        g = m.groups()
                        line = "##contig=<ID=%s,%s\n" % (translate(g[0]), g[1])
                print(line, end="")
                continue

        if subformat == "sam":
            if line.startswith("@SQ"):
                row = [
                    "SN:%s" % translate(x[3:]) if x.startswith("SN:") else x
                    for x in line.rstrip().split("\t")
                ]
                print("\t".join(row))
                continue
            elif line.startswith("@"):
                print(line, end="")
                continue

        if subformat is not None and subformat.startswith("chain") and not line.startswith("chain"):
            print(line, end="")
            continue

        row = line.rstrip("\n").split(delimiter)
        try:
            row[column] = translate(row[column])
            # handle the contig for the paired sequence in sam
            if "sam" == subformat and row[6] != "=":
                row[6] = translate(row[6])
        except IndexError:
            print(line, end="")
            continue
        print(delimiter.join(row))


def fasta(inf=sys.stdin, assembly="38", target="refseq", silent=False, **kwargs):
    translate = make_translation(assembly, target, silent)
    for line in inf:
        if line.startswith(">"):
            old_identifier = line[1:].split()[0]
            translated_line = ">%s%s" % (
                translate(old_identifier),
                line[(len(old_identifier) + 1) :],
            )
            print(translated_line, end="")
        else:
            print(line, end="")


def cli(args=None):
    parser = argparse.ArgumentParser(
        description="Change chromosome names to/from accessions"
    )
    parser.set_defaults(func=lambda **x: parser.print_usage())

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "--assembly",
        "-a",
        action="store",
        help="GRCh assembly version",
        default="38",
        choices=("37", "38"),
    )
    parent_parser.add_argument(
        "--silent",
        "-s",
        action="store_true",
        help="silently pass through identifiers that are not recognized (otherwise throw exception)",
    )
    parent_parser.add_argument(
        "--target",
        "-t",
        action="store",
        default="refseq",
        help="target naming system",
        choices=("ensembl", "genbank", "refseq", "ucsc"),
    )

    subparsers = parser.add_subparsers()

    parser_tsv = subparsers.add_parser(
        "tsv",
        parents=[parent_parser],
        help="Generic tab-separated (or other separated...) values formats, useful for BED files and the like",
    )
    parser_tsv.add_argument(
        "--column",
        "-c",
        action="store",
        default="1",
        help="column (1-based) to look for the chromosome in, default = 1",
    )
    parser_tsv.add_argument(
        "--delimiter",
        "-d",
        action="store",
        default="\t",
        help="column delimiter, default is <TAB>",
    )
    parser_tsv.set_defaults(func=separated_values)

    parser_fasta = subparsers.add_parser(
        "fasta",
        parents=[parent_parser],
        help="FASTA or similar formats (e.g., with header lines starting with '>')",
    )
    parser_fasta.set_defaults(func=fasta)

    parser_vcf = subparsers.add_parser(
        "vcf",
        parents=[parent_parser],
        help="Variant Call File format (space/tab delimited, but with special headers)"
    )
    parser_vcf.set_defaults(
        func=separated_values, delimiter="\t", column=1, subformat="vcf"
    )

    parser_sam = subparsers.add_parser(
        "sam",
        parents=[parent_parser],
        help="Sequence Alignment Map file format (like TSV, but special header and handling of paired sequence)",
    )
    parser_sam.set_defaults(
        func=separated_values, delimiter="\t", column=3, subformat="sam"
    )

    parser_chaintarget = subparsers.add_parser(
        "chaintarget",
        parents=[parent_parser],
        help="LiftOver chain target file (space-separated using 2nd column"
    )
    parser_chaintarget.set_defaults(
        func=separated_values, delimiter=" ", column=2, subformat="chain"
    )

    parser_chaintarget = subparsers.add_parser(
        "chainquery",
        parents=[parent_parser],
        help="LiftOver chain query file (space-separated using 7th column"
    )
    parser_chaintarget.set_defaults(
        func=separated_values, delimiter=" ", column=7, subformat="chain"
    )

    args = parser.parse_args()
    args.func(**vars(args))


if "__main__" == __name__:
    cli()
