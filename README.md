# Phy2HTML

Phy2HTML is a simple Python program that is designed to read a tree in Newick format and create a visualization of the tree for display in a webpage using only HTML and CSS. No Java, Javascript, SVG, or embedded images. It works by creating a fine CSS based-grid and adding appropriate cell borders to "draw" the tree.

The display tree is simplistic compared to what advanced phylogenetic visualization software can do, but it creates an output that may be more appropriate for display in webpages, at least in some circumstances (e.g., you can easily create links from the labels/taxa on the tree to any other page). The display style is simple, but can also be easily modified through simple applicaton of CSS. Tree shape is limited to rectangular branches with the root on the left and tip labels on the right.

The program assumes/requires the tree to be rooted and it cannot contain reticulations, although polytomies are fine. At this time the program does not scale branch lengths; it is designed for display of branching patterns not evolutionary distances. Branches are simply scaled to equal node depths.

You can see a simple example by viewing test_tree.html in a browser.
