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

import maya.cmds as cmds
import random


class Basic_building:

    def __init__(self, transform):
        self.transform = transform
        self.height = random.randint(40, 65) - 0.5
        self.size = "big"
        self.bbox = abs(cmds.getAttr(self.transform + ".boundingBoxMaxX") -
                        cmds.getAttr(self.transform + ".boundingBoxMinX"))

##########################################################################
############################# BASIC MODULES ##############################


def generate_basic_building(index_building=1, size="big"):
    height_delta = cmds.floatSliderGrp("bs_height", query=True, value=True)
    transforms = cmds.ls("skyline_GRP", type="transform")
    if "skyline_GRP" in transforms:
        cmds.delete("skyline_GRP")

    depth = random.randint(2, 15)
    width = random.randint(2, 15)
    building = Basic_building(cmds.polyCube()[0])

    # Manage Height and pivot:
    ####################################
    cmds.select(building.transform + ".f[3]", replace=True)
    cmds.move(0, 0.5, 0, relative=True, )
    cmds.select(clear=True)

    if size == "medium":
        building.height = random.randint(30, 45) - 0.5
    elif size == "small":
        building.height = random.randint(15, 35) - 0.5
    elif size == "tiny":
        building.height = random.randint(7, 20) - 0.5

    cmds.scale(width, building.height + (height_delta * building.height / 2), depth,
               building.transform, relative=True)
    cmds.delete(building.transform, constructionHistory=True)
    building.bbox = abs(cmds.getAttr(building.transform + ".boundingBoxMaxX") -
                        cmds.getAttr(building.transform + ".boundingBoxMinX"))
    return building


def generate_skyline_buildings():
    density = cmds.floatSliderGrp("bs_density", query=True, value=True)
    base_density_min = 35
    base_density_max = 50
    density_normalized_min = int(base_density_min +
                                 (base_density_min * density))
    density_normalized_max = int(base_density_max +
                                 (base_density_max * density))

    value = random.randint(density_normalized_min, density_normalized_max)
    buildings = []
    index = 1
    for number in range(1, int(value / 4 + 3)):
        for size in ["big", "medium", "small", "tiny"]:
            building = generate_basic_building(index, size)
            building.size = size
            new_name = "building" + "{:02}".format(index) + "_geo"
            cmds.rename(building.transform, new_name)
            building.transform = new_name
            buildings.append(building)
            cmds.makeIdentity(building.transform, apply=True, t=1, r=1, s=1)
            index += 1

    return buildings, size


def scatter_buildings():
    import maya.mel as mel
    buildings, size = generate_skyline_buildings()
    coefficent_tx = cmds.floatSliderGrp("bs_spread_width",
                                        query=True, value=True)
    coefficent_tz = cmds.floatSliderGrp("bs_spread_depth",
                                        query=True, value=True)

    base_tx = 70
    base_tz = 50

    normalized_tx = int((base_tx + base_tx * coefficent_tx) / 2)
    normalized_tz = int((base_tz + base_tz * coefficent_tz) / 2)

    tx = -normalized_tx
    bigs = []
    mediums = []
    smalls = []
    tinies = []

    # Manage Custom Values:
    #########################################################

    for building in buildings:
        if building.size == "big":
            bigs.append(building)
        elif building.size == "medium":
            mediums.append(building)
        elif building.size == "small":
            smalls.append(building)
        else:
            tinies.append(building)

    delta_z = normalized_tz
    tx = -normalized_tx
    density = cmds.floatSliderGrp("bs_density", query=True, value=True)

    def distribute_along_x_axis(tx, delta_z, buildings):
        for building in buildings:
            if building.size == "big":
                tz = random.randint(delta_z - 5, delta_z + 5)
            elif building.size == "medium":
                tz = random.randint(delta_z / 2 - 5, delta_z / 2 + 5)
            elif building.size == "small":
                tz = random.randint(- 5, 5)
            else:
                tz = random.randint(-delta_z / 2 - 5, -delta_z / 2 + 5)

            cmds.xform(building.transform,
                       translation=(tx, 0, tz))
            tx += building.bbox + random.randint(-2, 2) + \
                building.bbox * coefficent_tx - \
                building.bbox / 8 * density

    for cubes in [bigs, mediums, smalls, tinies]:
        distribute_along_x_axis(tx, delta_z, cubes)

    cmds.select(clear=True)

    # Manage Hierarchy
    ##########################################################
    for building in buildings:
        cmds.select(building.transform, add=True)
    cmds.group(name="skyline_GRP")
    cmds.select(clear=True)

    # Create Light and Camera
    ##########################################################
    skyline_props = cmds.ls("skyline_*")
    cameras = []
    for prop in skyline_props:
        if prop.startswith("skyline_cam"):
            cameras.append(prop)

    if not cameras:
        cmds.camera(name="skyline_cam", aspectRatio=1.778,  focalLength=35.0,
                    position=(-13.562, 8.133, -120.605), rotation=(3.455, 192.4, 0.031))

    if not "skyline_lgt" in skyline_props:
        light = cmds.spotLight(name="skyline_lgt")
        mel.eval("""evalDeferred("AElightTypeCB AttributeEditor|MainAttributeEditorLayout|formLayout1|AEmenuBarLayout|AErootLayout|AEStackLayout|AErootLayoutPane|AEbaseFormLayout|AEcontrolFormLayout|AttrEdspotLightFormLayout|scrollLayout2|columnLayout5|frameLayout36|columnLayout6|columnLayout7 skyline_lgtShape");
                AElightTypeCB AttributeEditor|MainAttributeEditorLayout|formLayout1|AEmenuBarLayout|AErootLayout|AEStackLayout|AErootLayoutPane|AEbaseFormLayout|AEcontrolFormLayout|AttrEdspotLightFormLayout|scrollLayout2|columnLayout5|frameLayout36|columnLayout6|columnLayout7 skyline_lgtShape;""")

        cmds.setAttr("skyline_lgt.intensity", 10)

        cmds.setAttr("skyline_lgt.tx", 95.414)
        cmds.setAttr("skyline_lgt.ty", 150.17)
        cmds.setAttr("skyline_lgt.tz", -30.343)

        cmds.setAttr("skyline_lgt.rx", -69.044)
        cmds.setAttr("skyline_lgt.ry", -245.958)
        cmds.setAttr("skyline_lgt.rz", -24.772)
