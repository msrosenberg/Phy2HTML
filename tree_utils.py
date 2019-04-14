import math
import turtle

class Node():
    """
    A class which represents a single node of a phylgenetic tree

    The class works by hierarchically by pointing to other nodes, either as
    ancestor or as a set of descendants.
    """
    def __init__(self):
        self.__name = ""
        self.__branch_length = 1
        self.__ancestor = None
        self.__descendants = list()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def branch_length(self):
        """
        The branch length represents the distance from the node to it's
        ancestor
        """
        return self.__branch_length

    @branch_length.setter
    def branch_length(self, value):
        self.__branch_length = value

    @property
    def descendants(self):
        return self.__descendants

    @property
    def ancestor(self):
        return self.__ancestor

    @ancestor.setter
    def ancestor(self, value):
        self.__ancestor = value

    def add_child(self, new_child):
        """
        add a new descendant to the node. the function automatically assigns
        this node as the ancestor of the child
        """
        self.descendants.append(new_child)
        new_child.ancestor = self

    def n_descendants(self):
        """ return the immediate number of descendants of the node """
        return len(self.descendants)

    def root(self):
        """ find and return the node representing the root of the tree """
        if self.ancestor == None:
            return self
        else:
            return self.ancestor.root()

    def is_descendant(self, query):
        """ is the query node a descendant of the calling node """
        result = False
        for d in self.descendants:
            if d == query:
                result = True
            elif d.is_descendant(query):
                result = True
        return result

    def is_sibling(self, query):
        """
        is the query node a sibling (same direct ancestor) of the
        calling node
        """
        result = False
        for d in self.ancestor.descendants:
            if d == query:
                result = True
        return result

    def n_tips(self):
        """ number of tips descended from this node, including itself """
        if self.n_descendants() == 0:
            return 1
        else:
            count = 0
            for d in self.descendants:
                count += d.n_tips()
            return count

    def distance_to_ancestor(self, query):
        """
        returns the sum of branch lengths between this node and the queried
        ancestor. if the query is not an ancestor this will get stuck in a
        loop.
        """
        distance = 0
        current_node = self
        while current_node != query:
            distance += current_node.branch_length()
            current_node = current_node.ancestor()
        return distance

    def common_ancestor(self, query):
        """
        returns the node representing the common ancestor between this node
        and the query, including the case where one is the ancestor of the
        other
        """
        if query.is_descendant(self):
            return query
        else:
            common_anc = self
            while not common_anc.is_descedent(query):
                common_anc = common_anc.ancestor()
            return common_anc  

    def distance_on_tree(self, query):
        """
        returns the sum of branch lengths separating this node from the query
        node on the tree
        """
        if self.is_descendant(query):
            return query.distance_to_ancestor(self)
        elif query.is_descendant(self):
            return self.distance_to_ancestor(query)
        else:
            common_anc = self.common_ancestor(query)
            return (self.distance_to_ancestor(common_anc) +
                    query.distance_to_ancestor(common_anc))

    def max_node_tip_length(self):
        """ find the longest distance between a node and its most distance
            descendant """
        long = 0
        for d in self.descendants:
            dec_long = d.max_node_tip_length()
            long = max(long, dec_long)
        return long + self.branch_length

    def max_node_name(self):
        """ find the longest name associated with a node and its descendants """
        long = len(self.name())
        for d in self.descendants():
            dec_long = d.max_node_name()
            long = max(long, dec_long)
        return long

    def tip_names(self):
        """ return a list of all tip names associated with a node  """
        names = list()
        if self.n_descendants() == 0:
            names.append(self.name)
        else:
            for d in self.descendants:
                d_names = d.tip_names()
                names.extend(d_names)
        return names

    def tip_nodes(self):
        """ return a list of all tip nodes associated with a node """
        tips = list()
        if self.n_descendants() == 0:
            tips.append(self)
        else:
            for d in descendants:
                d_tips = d.tip_nodes()
                tips.extend(d_tips)
        return tips

    def _Newick_recursion(self, bl_format = "0.4f"):
        """
         This function will output the tree in the Newick format.  If
         bl_format is not empty it will include branch lengths in the format
         specified by the bl_format string.  
        """
        if self.n_descendants() == 0:
            outstr = self.name
        else:
            outlist = []
            for d in self.descendants:
                outlist.append(d._Newick_recursion(bl_format))
            outstr = "(" + ",".join(outlist) + ")"
        if bl_format != "":
            outstr += ":" + format(self.branch_length, bl_format)
        return outstr


    def output_Newick(self, bl_format = "0.4f"):
        """
        calls the recursive function to produce the Newick and adds the
        semicolon to the end
        """
        return self._Newick_recursion(bl_format) + ";"


def read_Newick_tree(tree_str):
    """
    Translate a string representing a tree in Newick format into the internal
    tree struture and return the node representing the root.
    """
    SYMBOLS = "(),;"
    i = 0
    current_node = Node()
    while tree_str[i] != ";":
        if tree_str[i] == "(":
            new_node = Node()
            current_node.add_child(new_node)
            current_node = new_node
        elif tree_str[i] == ",":
            current_node = current_node.ancestor
            new_node = Node()
            current_node.add_child(new_node)
            current_node = new_node
        elif tree_str[i] == ")":
            if current_node.ancestor != None:
                current_node = current_node.ancestor
        else: # must be a name and/or a branch length
            j = i
            while not tree_str[j] in SYMBOLS:
                j += 1
            sub_str = tree_str[i:j]
            if not ":" in sub_str: # just a name
                current_node.name = sub_str
            elif sub_str[0] == ":": # just a branch length
                bl = eval(sub_str[1:].strip())
                current_node.branch_length = bl
            else: # a name and branch length combined
                new_name, new_bl = sub_str.split(":")
                current_node.name = new_name
                current_node.branch_length = eval(new_bl.strip())
            i = j - 1
        i += 1
    root_node = current_node.root()
    return root_node


def tree_turtle(tree, minx, maxx, miny, maxy, scale, DrawLabels,
                DrawBranchLengths):
    """
    use turtle graphics to draw the tree

    minx, maxx, miny, and maxy represent the drawing bounds for the target
    node, with minx representing the horizontal position of the ancestor of the
    node, maxx representing the right hand edge of the entire tree, miny and
    maxy representing the vertical positioning of the node and all of its
    descednents.

    scale is a precalculated value that converts branch lengths to pixels

    DrawLabels and DrawBranchLengths are boolean flags
    """

    yadj = 5 # this is a shift for font height
    name_padding = 10 # space names away from tree tips

    """
    the following calcuates the number of pixels necessary for the horizontal
    line conneting the node to it's ancestor. the node itself is at the
    """
    x = math.trunc(tree.branch_length * scale)

    """
    if the node has descendants, first draw all of the descendants in the box
    which goes from the right edge of the horizontal line for this node to the
    right hand edge of the drawing window, and the vertical box defined for the
    entire node
    """
    if tree.n_descendants() > 0:  # this is an internal node
        top_vert_line = 0
        bottom_vert_line = 0
        nd = tree.n_tips()
        topy = miny
        for i, d in enumerate(tree.descendants):
            """
            divide the vertical plotting area for each descendant proportional
            to the number of tips contained within that descendant
            """
            ndd = d.n_tips()
            bottomy = topy + math.trunc((ndd/nd) * (maxy-miny))
            # draw the descendant in its own smaller bounded box
            y = tree_turtle(d, minx+x, maxx, topy, bottomy, scale,
                            DrawLabels, DrawBranchLengths)
            """
            the vertical position of the first and last descendants represent
            the positions to draw the vertical line connecting all of the
            descendants
            """
            if i == 0:
                bottom_vert_line = y
            elif i == tree.n_descendants() - 1:
                top_vert_line = y
            topy = bottomy
        """
        draw the vertical line connecting the descendants at the horizontal
        position of the node
        """
        turtle.penup()
        turtle.goto(minx+x, bottom_vert_line);
        turtle.pendown()
        turtle.goto(minx+x, top_vert_line);
        """
        the vertical position of the node should be the midpoint of the
        vertical line connecting the descendants
        """
        y = ((top_vert_line-bottom_vert_line) // 2) + bottom_vert_line;
    else:  # this is a tip node
        """
        if the node has no descendants, figure out the vertical position as the
        midpoint of the vertical bounds
        """
        y = ((maxy - miny) // 2) + miny
        if DrawLabels:
            # if desired, label the node 
            turtle.penup()
            turtle.goto(minx + x + name_padding, y - yadj)
            turtle.pendown()
            turtle.write(tree.name)

    # draw the horizontal line connecting the node to its ancestor
    turtle.penup()
    turtle.goto(minx, y) # ancestral node location
    turtle.pendown()
    turtle.goto(minx+x, y) # this node location

    # add branch lengths
    if DrawBranchLengths:
        pass
        # not yet enabled

    return y
   

def draw_tree_turtle(root):
    xwidth = 1000
    yheight = 1000
    margin = 10
    maxbranch = root.max_node_tip_length()
    scale = (xwidth - 100) / maxbranch
    win = turtle.Screen()
    win.screensize(xwidth + 2*margin, yheight + 2*margin)
    win.setworldcoordinates(-margin, -margin, xwidth+margin, yheight+margin)
    turtle.hideturtle()
    turtle.color("black")
    tree_turtle(root, 0, xwidth, 0, yheight, scale, True, False)


def main():
    # test the code
    with open("mammal_tree.txt", "r") as infile:
        newick_str = infile.readline()
    print("Input:", newick_str)
    print()
    tree = read_Newick_tree(newick_str)
    print("File read succesfully.")
    print("Tree contains", tree.n_tips(), "taxa.")
    taxa_list = tree.tip_names()
    for i, t in enumerate(taxa_list):
        print(i+1, t)
    print()
    print("Newick output:", tree.output_Newick())
    input("Press Enter to continue")
    draw_tree_turtle(tree)



if __name__ == "__main__":
    main()


