'''
#*************************************************************************
                            Skyline Genarator:
#*************************************************************************
Description: - generate Randomic Skilines;
             - Advanced Distrubution Options
#*************************************************************************
 Author: Laura Siviero
         laura.seav@gmail.com
 
 License: MIT https://github.com/laurasiviero/SkylineGenerator/blob/main/LICENSE
 
 Date 2021.07.16
#*************************************************************************
'''

import sys
import maya.cmds as cmds


# *************************************************************************
# UI:
# *************************************************************************


def basic_skyline_ui(USERPATH):
    ui_title = "cubic_skyline"
    sys.path.append(USERPATH)
    # COLOR PALETTE
    ########################################
    theme_color = [0.286, 0.286, 0.286]
    analogue_color = [0.2, 0.2, 0.2]
    complementary_color = [0.0, 0.0, 0.0]
    # PATHS
    ########################################
    image_path = USERPATH + "\\images\\"

    # DELETE if it already exists:
    if cmds.window(ui_title, exists=True):
        cmds.deleteUI(ui_title)

    window = cmds.window(ui_title, title="Cubic Skyline",
                         backgroundColor=theme_color,
                         resizeToFitChildren=True)

    cmds.columnLayout(adjustableColumn=True)
    cmds.image("bs_banner", image=image_path + 'skyline_banner.png')
    cmds.button("bs_generate", label="GENERATE SKYLINE",
                height=50,
                backgroundColor=analogue_color,
                command="bsg.scatter_buildings()")
    cmds.text(label="More Options:", align="left")
    cmds.separator(backgroundColor=analogue_color, style="double",
                   height=3)
    cmds.text(label="Spread:", align="left")
    cmds.floatSliderGrp("bs_spread_width", label="Width: ",
                        columnWidth=[(1, 50), (3, 30)],
                        field=True,
                        precision=3,
                        min=0, max=1, value=0)
    cmds.floatSliderGrp("bs_spread_depth", label="Depth: ",
                        columnWidth=[(1, 50), (3, 30)],
                        field=True,
                        precision=3,
                        min=0, max=1, value=0)

    cmds.text(label="City Management:", align="left")
    cmds.floatSliderGrp("bs_density", label="Density: ",
                        columnWidth=[(1, 50), (3, 30)],
                        field=True,
                        precision=3,
                        min=-1, max=1, value=0)
    cmds.floatSliderGrp("bs_height", label="Height: ",
                        columnWidth=[(1, 50), (3, 30)],
                        field=True,
                        precision=3,
                        min=-1, max=1, value=0)
    cmds.separator(backgroundColor=analogue_color, style="double",
                   height=3)

    cmds.showWindow(window)
