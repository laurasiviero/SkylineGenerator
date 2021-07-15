*************************************************************************

Skyline Generator:

*************************************************************************

Author: Laura Siviero; laura.seav@gmail.com

Date 2021.05.05

*************************************************************************

Description:
- The tool allows you to generate a randomic Skyline (python 2.7);
- Tool for Maya;

Video: https://vimeo.com/575581074

License: MIT https://github.com/laurasiviero/SkylineGenerator/blob/main/LICENSE

*****************************************************************************

Instructions:

- Put the cubic_skyline folder in the folder: C:\Users\YOU\Documents\maya\20XX\scripts
- Extract everything in the same location;
- Launch maya;
- Copy the following line in the script editor, make sure to change the path in the next lines too:

import sys

import sys
USERPATH = r"C:\Users\YOU\Documents\maya\20XX\scripts" 
sys.path.append(USERPATH)
import basic_skyline_ui as bs
import basic_skyline_generator as bsg
bs.basic_skyline_ui(USERPATH)

Feel free to add the code to your shelf;
Replace the default shelf icon with the appropriate one: tic_tac_toe\tic_tac_toe_icons\tic_tac_toe_shelf;
DO NOT MOVE ANY SUBFOLDERS;
Have fun!
