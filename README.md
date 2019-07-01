# Phy2HTML

Phy2HTML is a simple Python program that is designed to read a tree in Newick format and create a visualization of the tree for display in a webpage using only HTML and CSS. No Java, Javascript, SVG, or embedded images, and readily scalable. It works by creating a CSS based-grid and adding appropriate cell borders to "draw" the tree. The output html and css are kept deliberately minimalistic to readily allow you to copy/embed the code into other pages or workflows.

The displayed tree is simplistic compared to what advanced phylogenetic visualization software can do, but it creates an output that may be more appropriate for display on the web, at least in some circumstances (*e.g.*, you can easily create links from the labels/taxa on the tree to any other page). The display style is simple, but can also be easily modified through basic application of CSS. Tree shape is limited to rectangular branches with the root on the left and tip labels on the right.

The program assumes/requires the tree to be rooted and it cannot contain reticulations, although polytomies are fine. The program can draw the tree with or without scaled branch lengths.

You can see a simple example of the output by viewing [test_tree.html](http://htmlpreview.github.io/?https://github.com/msrosenberg/Phy2HTML/blob/master/test_tree.html) in a browser. (Obviously this only works on browsers which support grid css; with legacy browsers such as Internet Explorer, your mileage may vary).

Two sample Newick files are included, one with 11 taxa and one with 66. The 66 taxa tree contains branch lengths; the 11 taxa tree does not. There is no technical limit to the size of the tree it can display, but very large trees will likely become visually unwieldy just due to the standard scaling issues one would have with any very large tree.

The code is written in Python 3 and works in vanilla Python with no external dependencies.

To use, simply run phy2html.py (for an interactive mode that will prompt for input and output file names) or import the module and call the function *create_html_tree(inname, outname)* where inname is the name of a simple text file containing a tree in Newick format and outname is the desired name for the HTML output (a variety of other parameters are entirely optional).

*create_html_tree()* returns the html as a list, so if calling the function directly you can set outname as an empty string to suppress writing the output to a file, but still use the returned list as input into other code.

Additional options include:

- Draw the branch lengths to scale:
  - If this option is chosen, you can specify how many columns you wish to scale the tree over (default = 1000). Larger numbers allow more precise visualization of branch length differences, but potentially require more screen width (by default each column will be 1 pixel wide, although this can be changed, including fractional column widths).
  - If branch lengths are not being drawn to scale, one can specify the default column width at runtime.
- Default row height: Each taxon label is drawn over two rows and two empty rows are used as spacers between taxon labels. 
- Default tip label width: how much space to preserve for tip labels past the end of the tree
- An optional *prefix*: This label will be pre-appended onto the various css classes and ids; it can be used to more readily differentiate these classes and ids automatically created by the program, and is particularly useful if you wish to combine multiple trees into a single webpage.
- Labeling branches with CSS names: this option can be used to put the CSS labels on every horizontal and vertical line. It is not meant for final output, but rather as an aid in identifying which lines is which if you wish to customize particular elements. If using this option, you might want to modify the row height (*e.g.*, to 1em or 1.1em) so that the branch labels do not overlap the drawn lines.

Many of these elements (*e.g.*, row heights, column heights), can be modified directly in the output HTML/CSS and do not require one to rerun the program. When running the program these elements can (and should) include standard CSS units (*e.g.,* 10px or 1em).

