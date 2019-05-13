---
title: 'Phy2HTML: A simple method for displaying phylogenies in webpages'
tags:
- Python
- phylogenetics
- html
- css
authors:
- name: Michael S. Rosenberg
 orcid: 0000-0001-7882-2467
 affiliation: 1
affiliations: 
- name: Center for the Study of Biological Complexity, Virginia Commonwealth University, Richmond, VA, USA
 index: 1
date: 13 May 2019
bibliography: paper.bib
---

# Summary

Phylogenetic trees are a key research output of systematic biology and represent a key visualization tool underlying most evolutionary thinking [@Baum:2012]. While many tools can create phylogetic visualizations suitable for traditional print purposes, displaying trees on the web is a bit more complicated. Displaying a phylogeny in a webpage generally involves either using static images which cannot be readily modified or interacted with (*e.g.,* raster images or SVG) or relying on scripting languages such as Java or Javascript, which impose costs on website delivery and responsiveness and offer a complexity well beyond the needs of many users. Phy2HTML is a simple Python script that displays a tree using only HTML and CSS. The tree is readily scalable, easily modifiable, and mildly interactable as tip names or branch lables can be made into hyperlinks. The output HTML and CSS are deliberately kept simple to allow the tree to be readily embedded into other pages or integrated into larger scripts for post-processing.

Phy2HTML takes advantage of CSS Grids to construct a layout with a large number of rows and columns. Displayed items (*i.e.* tip labels, lines) are assigned to ranges of cells in the grid and the tree is "drawn" by applying border properties to the containing cells. All elements are given common and unique identifier allowing a user with a basic grasp of CSS to customize the style of the displayed tree. This visualization should work on all modern browsers, although legacy browsers such as Internet Explorer may not support CSS Grid layouts. Trees can be imported from standard Newick format. Phy2HTML is written in Python 3 with no external dependencies and can be obtained from <https://github.com/msrosenberg/Phy2HTML> under a GPL-3.0 license.

Phy2HTML currently has two major limitations: (1) it requires trees to be rooted, and (2) it does not display branch lengths to scale, rather focusing only on branching pattern. The latter could likely be overcome by defining a very dense grid of columns.

An example of two output trees can be seen on the fiddlercrab.info website [@Rosenberg:2014], specifically at: http://www.fiddlercrab.info/uca_phylogeny.html. These two trees were post-processed to display on a single page and to replace the default tip names with hyperlinks to taxon-specific pages.



# Acknowledgements

This project was supported by the Center for the Study of Biological Complexity and VCU Life Sciences.



# References
