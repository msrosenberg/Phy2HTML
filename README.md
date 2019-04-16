# Phy2HTML

Phy2HTML is a simple Python program that is designed to read a tree in Newick format and create a visualization of the tree for display in a webpage using only HTML and CSS. No Java, Javascript, SVG, or embedded images, and readily scalable. It works by creating a CSS based-grid and adding appropriate cell borders to "draw" the tree. The output html and css are kept deliberately minimalistic to readily allow you to copy/embed the code into other pages or workflows.

The display tree is simplistic compared to what advanced phylogenetic visualization software can do, but it creates an output that may be more appropriate for display on the web, at least in some circumstances (*e.g.*, you can easily create links from the labels/taxa on the tree to any other page). The display style is simple, but can also be easily modified through simple application of CSS. Tree shape is limited to rectangular branches with the root on the left and tip labels on the right.

The program assumes/requires the tree to be rooted and it cannot contain reticulations, although polytomies are fine. At this time the program does not scale branch lengths; it is designed for display of branching patterns not evolutionary distances. Branches are simply scaled to equal node depths (the program will read branch lengths without a problem, it just doesn't use them).

You can see a simple example of the output by viewing [test_tree.html](http://htmlpreview.github.io/?https://github.com/msrosenberg/Phy2HTML/blob/master/test_tree.html) in a browser. (Obviously only works on browsers which support grid css; with legacy browsers such as Internet Explorer, your mileage may vary).

Two sample Newick files are included, one with 11 taxa and one with 66. There is no technical limit to the size of the tree it can display, but very large trees will likely become visually unwieldy just due to the standard scaling issues one would have with any very large tree.

The code is written in Python 3 and works in vanilla Python with no external dependencies.

To use, simply run phy2html.py (for an interactive mode that will prompt for input and output file names) or import it and call the function *create_html_tree(inname, outname)* where inname is the name of a simple text file containing a tree in Newick format and outname is the desired name for the HTML output.

*create_html_tree()* now returns the html as a list, so if calling the function directly you can set outname as an empty string to suppress writing the output to a file, but still use the returned list as input into other code.

Additional options allow one to set default column widths and row heights, which effect the scale over which the tree will be drawn. Another optional parameter is a *prefix* which will be pre-appended to the various css classes and ids; this can be used to more readily differentiate the classes and ids created by the code, particularly if one plans on using the output to display multiple trees in the same page. 

All of these can also be changed through post-processing editing of the output css styles.