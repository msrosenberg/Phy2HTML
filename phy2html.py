"""
Phy2HTML
"""

from typing import TextIO, Tuple
import tree_utils


class Branch:
    def __init__(self, min_col: int = 0, col_span: int = 0, row: int = 0):
        self.min_col = min_col
        self.col_span = col_span
        self.row = row


class VLine:
    def __init__(self, min_row: int = 0, row_span: int = 0, col: int = 0):
        self.min_row = min_row
        self.row_span = row_span
        self.col = col


class Taxon:
    def __init__(self, node: tree_utils.Node, row: int = 0):
        self.node = node
        self.row = row


def start_html(outfile: TextIO) -> None:
    outfile.write("<html>\n")
    outfile.write("  <head>\n")


def end_head_section(outfile: TextIO) -> None:
    outfile.write("  </head>\n")
    outfile.write("  <body>\n")


def end_html(outfile: TextIO) -> None:
    outfile.write("  </body>\n")
    outfile.write("</html>\n")


def write_style_to_head(outfile: TextIO, nrows: int, ncols: int, taxa: list, branches: list, vlines: list) -> None:
    outfile.write("    <style>\n")
    outfile.write("      .phylogeny {\n")
    outfile.write("                   display: grid;\n")
    outfile.write("                   grid-template-rows: repeat({}, 20px);\n".format(nrows))
    outfile.write("                   grid-template-columns: repeat({}, 40px) 200px;\n".format(ncols-1))
    outfile.write("                 }\n")
    outfile.write("      .taxon-name { align-self: center; padding-left: 10px }\n")
    outfile.write("      .genus-species-name {font-style: italic }\n")
    outfile.write("      .branch-line { border-bottom: solid black 1px; text-align: center }\n")
    outfile.write("      .vert-line { border-right: solid black 1px }\n")
    outfile.write("\n")
    for i, t in enumerate(taxa):
        outfile.write("	     #taxon{} {{ grid-area: {} / {} / span 2 / span 1 }}\n".format(i+1, t.row, ncols))
    outfile.write("\n")
    for i, b in enumerate(branches):
        outfile.write("	     #branch{} {{ grid-area: {} / {} / span 1 / span {} }}\n".format(i+1,
                                                                                             b.row,
                                                                                             b.min_col,
                                                                                             b.col_span))
    outfile.write("\n")
    for i, v in enumerate(vlines):
        outfile.write("	     #vline{} {{ grid-area: {} / {} / span {} / span 1 }}\n".format(i+1,
                                                                                            v.min_row,
                                                                                            v.col,
                                                                                            v.row_span))
    outfile.write("\n")
    outfile.write("    </style>\n")


def write_tree_to_body(outfile: TextIO, taxa: list, branches: list, vlines: list) -> None:
    outfile.write("    <div class=\"phylogeny_container\">\n")
    outfile.write("      <div class=\"phylogeny\">\n")
    outfile.write("\n")
    for i, t in enumerate(taxa):
        outfile.write("        <div id=\"taxon{}\" "
                      "class=\"genus-species-name taxon-name\">{}</div>\n".format(i+1, t.node.name))
    outfile.write("\n")
    for b in range(len(branches)):
        outfile.write("        <div id=\"branch{}\" class=\"branch-line\">&nbsp;</div>\n".format(b+1))
    outfile.write("\n")
    for v in range(len(vlines)):
        outfile.write("        <div id=\"vline{}\" class=\"vert-line\">&nbsp;</div>\n".format(v+1))
    outfile.write("\n")
    outfile.write("      </div>\n")
    outfile.write("    </div>\n")


def total_rows_per_node(n: int, rows_per_tip: int) -> int:
    return (2*n - 1) * rows_per_tip


def tree_recursion(tree, min_col: int, max_col: int, min_row: int, max_row: int, taxa: list, branches: list,
                   vlines: list, rows_per_tip: int) -> int:
    """
    calculate positions of taxa, branches, and vertical connectors on subtrees
    """

    """
    determine the number of columns for the branch connecting a node to its ancestor
    """
    if tree.ancestor is not None:
        col_span = tree.node_depth - tree.ancestor.node_depth
    else:
        col_span = 0

    """
    if the node has descendants, first draw all of the descendants in the box which starts in the column to the 
    right of this node, and the rows defined for the entire node
    """
    if tree.n_descendants() > 0:  # this is an internal node
        vert_top_row = 0
        vert_bottom_row = 0
        # nd = tree.n_tips()
        top_row = min_row
        for i, d in enumerate(tree.descendants):
            """
            calculate the total rows for each descendant based on the number of tips of the descendant
            """
            ndd = d.n_tips()
            d_rows = total_rows_per_node(ndd, rows_per_tip)
            bottom_row = top_row + d_rows - 1
            # draw the descendant in its own smaller bounded box
            row = tree_recursion(d, min_col + col_span, max_col, top_row, bottom_row, taxa, branches, vlines,
                                 rows_per_tip)
            """
            the rows of the first and last descendants represent the positions to draw the vertical line 
            connecting all of the descendants
            """
            if i == 0:
                vert_top_row = row + 1
            elif i == tree.n_descendants() - 1:
                vert_bottom_row = row
            top_row = bottom_row + rows_per_tip + 1

        """
        add the vertical line connecting the descendants at the horizontal position of the node
        """
        new_line = VLine(vert_top_row, vert_bottom_row - vert_top_row + 1, min_col+col_span)
        vlines.append(new_line)

        """
        the vertical position of the node should be the midpoint of the vertical line connecting the descendants
        """
        row = ((vert_bottom_row - vert_top_row) // 2) + vert_top_row
    else:  # this is a tip node
        """
        if the node has no descendants, add it to the taxon list
        """
        row = min_row
        new_taxon = Taxon(tree, row)
        taxa.append(new_taxon)

    # add the branch connecting the node to its ancestor
    if col_span > 0:
        new_branch = Branch(min_col+1, col_span, row)
        branches.append(new_branch)

    return row


def calculate_tree(tree: tree_utils.Node, nrows: int, ncols: int, rows_per_tip: int) -> Tuple[list, list, list]:
    taxa = []
    branches = []
    vlines = []
    tree_recursion(tree, 1, ncols, 1, nrows, taxa, branches, vlines, rows_per_tip)
    return taxa, branches, vlines


def add_node_depth(tree: tree_utils.Node, max_depth: int) -> None:
    """
    add the column depth of each node on the tree, where the root is column 1 and the tips are column x - 1
    where x is the last column which will contain the tip names
    """
    tree.node_depth = max_depth - tree.max_node_tip_count()
    for d in tree.descendants:
        add_node_depth(d, max_depth)


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
    nrows = total_rows_per_node(ntips, rows_per_tip)
    ncols = tree.max_node_tip_count() + 1
    add_node_depth(tree, ncols+1)
    taxa, branches, vlines = calculate_tree(tree, nrows, ncols, rows_per_tip)
    with open(outname, "w") as outfile:
        start_html(outfile)
        write_style_to_head(outfile, nrows, ncols, taxa, branches, vlines)
        end_head_section(outfile)
        write_tree_to_body(outfile, taxa, branches, vlines)
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
