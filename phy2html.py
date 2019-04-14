"""
Phy2HTML
"""

from typing import TextIO
import tree_utils


def start_html(outfile: TextIO) -> None:
    outfile.write("<html>\n")
    outfile.write("  <head>\n")


def end_head_section(outfile: TextIO) -> None:
    outfile.write("  </head>\n")
    outfile.write("  <body>\n")


def end_html(outfile: TextIO) -> None:
    outfile.write("  </body>\n")
    outfile.write("</html>\n")


def write_style_to_head(outfile: TextIO) -> None:
    outfile.write("    <style>\n")
    outfile.write("    </style>\n")


def write_tree_to_body(outfile: TextIO) -> None:
    outfile.write("    <div class=\"phylogeny_container\">\n")
    outfile.write("      <div class=\"phylogeny\">\n")

    outfile.write("      </div>\n")
    outfile.write("    </div>\n")


def create_html_tree(inname: str, outname: str, rows_per_tip: int = 2) -> None:
    with open(inname, "r") as infile:
        newick_str = infile.readline()
    print()
    print("Input file: " + inname)
    print("Imported Tree String: ", newick_str)
    print()
    tree = tree_utils.read_newick_tree(newick_str)
    print("File read successfully.")
    print("Tree contains", tree.n_tips(), "tips.")
    print()
    ntips = tree.n_tips()
    nrows = rows_per_tip * (2*ntips - 1)
    with open(outname, "w") as outfile:
        start_html(outfile)
        write_style_to_head(outfile)
        end_head_section(outfile)
        write_tree_to_body(outfile)
        end_html(outfile)
    print("HTML file created: " + outname)


def main():
    # get input parameters
    default = "fiddler_tree.nwk"
    inname = input("Name of tree file [default={}]: ".format(default))
    if inname == "":
        inname = default
    default = "test_tree.html"
    outname = input("Name of output HTML file [default={}]: ".format(default))
    if outname == "":
        outname = default
    create_html_tree(inname, outname)


if __name__ == "__main__":
    main()
