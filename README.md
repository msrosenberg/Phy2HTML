# Phy2HTML

Phy2HTML is a simple Python program that is designed to read a tree in Newick format and create a visualization of the tree for display in a webpage using only HTML and CSS. No Java, Javascript, SVG, or embedded images, and readily scalable. It works by creating a CSS based-grid and adding appropriate cell borders to "draw" the tree. The output html and css are kept deliberately minimalistic to readily allow you to copy/embed the code into other pages or workflows.

The display tree is simplistic compared to what advanced phylogenetic visualization software can do, but it creates an output that may be more appropriate for display on the web, at least in some circumstances (e.g., you can easily create links from the labels/taxa on the tree to any other page). The display style is simple, but can also be easily modified through simple applicaton of CSS. Tree shape is limited to rectangular branches with the root on the left and tip labels on the right.

The program assumes/requires the tree to be rooted and it cannot contain reticulations, although polytomies are fine. At this time the program does not scale branch lengths; it is designed for display of branching patterns not evolutionary distances. Branches are simply scaled to equal node depths (the program will read branch lengths without a problem, it just doesn't use them).

You can see a simple example of the output by viewing [test_tree.html](http://htmlpreview.github.io/?https://github.com/msrosenberg/Phy2HTML/blob/master/test_tree.html) in a browser.

Two sample Newick files are included, one with 11 taxa and one with 66. There is no technical limit to the size of the tree it can display, but very large trees will likely become visually unwieldy just due to the standard scaling issues one would have with any very large tree.

The code is written in Python 3 and works in vanilla Python with no external dependencies.

To use, simply run phy2html.py (for an interactive mode that will prompt for input and output file names) or import it and call the function *create_html_tree(inname, outname)* where inname is the name of a simple text file containing a tree in Newick format and outname is the desired name for the HTML output.

More complicated interfaces and options may be available on request.
