"""
name: OASYS_SLOPE COM Functions
description: n/a

BY:         MJJ
DATE:       09/02/2023
PURPOSE:    
INPUTS:     N/A

NOTES:		not complete, needs checking/testing. Fill out descriptions and args etc.
"""

import win32com.client
slope_obj = win32com.client.Dispatch("safeLib.SafeAuto")

def Show():
    """
    Arguments:

    Returns:

    Description:
        This function has no input/output variables.  It opens Slope and shows the main program window.
    """
    slope_obj.Show()

def Open(sPathName: str) -> int:
    """
    Arguments:
        sPathName: [String] -- [description]

    Returns:
        returns an integer
    
    Description:
        This function opens a saved file.  sPathName is a string giving the file path. If the file is opened successfully the function will return 0, or if it was unsuccessful it will return 1.
    """
    tmp = slope_obj.Open(sPathName)
    return tmp

def Analyse(iStage: int) -> int:
    """
    Arguments:
        iStage: [Integer] -- [description]
    
    Returns:
        Returns an integer
    
    Description:
    """
    tmp = slope_obj.Analyse(iStage)
    return tmp

# This is a function instructing Slope to analyse the currently open file, up to the stage number iStage.  
def Save() -> int:
    """
    Arguments:
    
    Returns:
        returns an integer

    Description:
        Saves the currently open file.
    """
    tmp = slope_obj.Save()
    return tmp

def SaveAs(sPathName):
    """
    Arguments:
        sPathName:  [String]

    Returns:
        returns an integer
    
    Description:
        Saves the currently open file with a different name.
    """
    tmp = slope_obj.SaveAs(sPathName)
    return tmp

def DeleteResults():
    """
    Arguments:

    Returns:
        returns an integer
    
    Description:
        Deletes the existing results.
    """         
    tmp = slope_obj.DeleteResults()
    return tmp

def Close():
    """
    Arguments:

    Returns:
        returns an integer

    Description:
        Closes the current file.
    """
    tmp = slope_obj.Close()
    return tmp

# Material functions
# NOTE: Index  imat in material functions is zero based index.
def GetNumMaterial() -> int:
    """
    Arguments:

    Returns:
        returns the number of materials as an integer

    Description:
        ...
    """
    tmp = slope_obj.GetNumMaterial()
    return tmp

def CreateMaterial(name: str) -> None: 
    """
    Arguments:
        name:   [String]

    Returns:

    Description:
        creates a blank material record with the name specified
    """
    tmp = slope_obj.CreateMaterial(name)
    return tmp

def GetMatName(imat: int) -> str: 
    """
    Arguments:
        imat:   [integer]
    Returns:
        returns material name with index “imat”

    Description:

    """
    tmp = slope_obj.GetMatName(imat)
    return tmp

def SetUnitWtAbove(imat:int, value:float) -> None: 
    """
    Arguments:
        imat:   [integer]
        value:  [float]

    Returns:

    Description:
        sets material imat's unit weight above the water table to the value specified
    """
    tmp = slope_obj.SetUnitWtAbove(imat,value)

def SetUnitWtBelow(imat:int, value:float) -> None:
    """
    Arguments:
        imat:   [integer]
        value:  [float]

    Returns:

    Description:
        sets material imat's unit weight below the water table to the value specified
    """
    tmp = slope_obj.SetUnitWtBelow(imat,value)

def SetDrainageType(imat: int, type:int) -> None:
    """
    Arguments:
        imat:   [integer]
        type:   [integer]
    Returns:

    Description:
        sets the material imat to be undrained, drained with linear strength, drained with a power curve or hyperbolic strength relationship (values 0 to 3 respectively)
    """
    tmp = slope_obj.SetDrainageType(imat,type)


def SetPhi(imat:int, value:float):
    """
    Arguments:
        imat:   [integer]
        value:  [float]

    Returns:

    Description:
        sets the friction angle of the material
    """
    tmp = slope_obj.SetPhi(imat,value)


def SetCohesion(imat:int, value:float):
    """
    Arguments:
        imat:   [integer]
        value:  [float]

    Returns:

    Description:
        sets the cohesion value for the material
    """
    tmp = slope_obj.SetCohesion(imat,value)

def SetCohesionRefLevel(imat:int, value:float):
    """
    Arguments:
        imat:   [integer]
        value:  [float]

    Returns:

    Description:
        sets the level at which the cohesion value applies.  This need not be specified unless the material has varying cohesion with depth.
    """
    tmp = slope_obj.SetCohesionRefLevel(imat,value)

def SetCohesionGradient(imat:int, value:float):
    """
    Arguments:
        imat:   [integer]
        value:  [float]

    Returns:

    Description:
        sets the gradient of cohesion.  Need not be specified if the material has constant cohesion.
    """
    tmp = slope_obj.SetCohesionGradient(imat,value)

def SetPowerCurveParams(imat:int, value1:float, value2:float):
    """
    Arguments:
        imat:   [integer]
        value1: [float]
        value2: [float]

    Returns:

    Description:
        sets the values of the two parameters for use in drained materials with a power curve relationship (see Material Properties for details)
    """

    tmp = slope_obj.SetPowerCurveParams(imat,value1,value2)

def SetCupRatio(imat:int, value:float):
    """
    Arguments:
        imat:   [integer]
        value:  [float]

    Returns:

    Description:
        sets the Cu/p ratio for an undrained material.  If this is set as well as the cohesion gradient, the lower of the two values will be used.
    """
    tmp = slope_obj.SetCupRatio(imat,value)

def GetUnitWtAbove(imat:int) -> float:
    """
    Arguments:
        imat:   [integer]

    Returns:
        returns the unit weight above the water table

    Description:
        ...
    """
    tmp = slope_obj.GetUnitWtAbove(imat)
    return tmp

def GetUnitWtBelow(imat:int) -> float:
    """
    Arguments:
        imat:   [integer]
   
    Returns:
        returns the unit weight below the water table

    Description:

    """
    tmp = slope_obj.GetUnitWtAbove(imat)
    return tmp

def GetDrainageType(imat:int) -> int:
    """
    Arguments:
        imat:   [integer]
    
    Returns:
        returns the material drainage setting
    
    Description:
        ...
    """
    tmp = slope_obj.GetDrainageType(imat)
    return tmp

def GetPhi(imat:int) -> float:
    """
    Arguments:
        imat:   [integer]
    
    Returns:
        returns the friction angle of the material

    Description:
        ...
    """
    tmp = slope_obj.GetPhi(imat)
    return tmp

def GetCohesion(imat:int) -> float:
    """
    Arguments:
        imat:   [integer]

    Returns:
        returns the cohesion value for the material

    Description:
        ...
    """
    tmp = slope_obj.GetCohesion(imat)
    return tmp

def GetCohesionRefLevel(imat:int) -> float:
    """
    Arguments:
        imat:   [integer]

    Returns:
        returns the level at which the cohesion value applies

    Description:
        ...
    """
    tmp = slope_obj.GetCohesionRefLevel(imat)
    return tmp

def GetCohesionGradient(imat:int) -> float:
    """
    Arguments:
        imat:   [integer]

    Returns:
        returns the gradient of cohesion.

    Description:
        ...
    """
    tmp = slope_obj.GetCohesionGradient(imat)
    return tmp

def GetPowerCurveParamA(imat:int):
    """
    Arguments:
        imat:   [integer]

    Returns:
        returns the first parameter for use in drained materials with a power curve relationship (see manual for details)

    Description:
        ...
    """
    tmp = slope_obj.GetPowerCurveParamA(imat)
    return tmp

def GetPowerCurveParamB(imat:int):
    """
    Arguments:
        imat:   [integer]

    Returns:
        returns the second parameter for use in drained materials with a power curve relationship (see manual for details)

    Description:
        ...
    """
    tmp = slope_obj.GetPowerCurveParamB(imat)
    return tmp

def GetCupRatio(imat:int):
    """
    Arguments:
        imat:   [integer]
    
    Returns:
        returns the Cu/p ratio for an undrained material

    Description:
        ...
    """
    tmp = slope_obj.GetCupRatio(imat)
    return tmp

# Geometry functions
def DefineCutPlane(xmin:float, ymin:float, xmax:float, ymax:float):
    """
    Arguments:
        xmin:   [float]
        ymin:   [float]
        xmax:   [float]
        ymax:   [float]

    Returns:

    Description:
        define a vertical plane from (xmin, ymin) to (xmax, ymax) along which to cut a 3D surface.  The 3D surface can be imported from a TIN surface contained in an XML file.
    """
    tmp = slope_obj.DefineCutPlane(xmin,ymin,xmax,ymax)


def SetStraightnessTol(tol:float):
    """
    Arguments:
        tol:    [float]

    Returns:

    Description:
        sets a straightness tolerance, in degrees.  Two adjacent lines on a polyline will be treated as one line (middle point will be omitted) if their angles are within this tolerance of each other, i.e. if the lines are nearparallel.
    """
    tmp = slope_obj.SetStraightnessTol(tol)

def ImportXml(path:str):
    """
    Arguments:
        path:   [string]

    Returns:

    Description:
        reads the specified XML file, imports the 3D data contained in it, and generates polylines where the 3D surface cuts the previously specified cutting plane
    """
    tmp = slope_obj.ImportXml(path)

def SetStratum(istra:int, name:str, matname:str): #var name is bricked
    """
    Arguments:
        is:         [integer]
        name:       [string]
        matname:    [string]

    Returns:

    Description:
        creates a “blank” stratum (no points yet) with the specified name.  The integer should be the stratum number.  The first stratum should have the number 1.
    """
    tmp = slope_obj.SetStratum(istra,name,matname)

def SetStratumPoint(istra:int, ip:float, xp:float, yp:float):
    """
    Arguments:
        istra:      [integer]
        ip:         [integer]
        xp:         [float]
        yp:         [float]

    Returns:

    Description:
        set point 'ip' in stratum is to the value (xp, yp)
    """
    tmp = slope_obj.SetStratumPoint(istra,ip,xp,yp)

def NumStrata():
    """
    Arguments:

    Returns:
        returns the number of strata as an integer

    Description:
    """
    tmp = slope_obj.NumStrata()
    return tmp

def GetStratumPointX(istra:int, ip:int) -> float:
    """
    Arguments:
        is: [integer]
        ip: [integer]

    Returns:

    Description:
    returns the X coordinate of point 'ip' in stratum 'is' (zerobased point counter)
    """
    tmp = slope_obj.GetStratumPointX(istra,ip)
    return tmp

def GetStratumPointY(istra:int, ip:int) -> float:
    """
    Arguments:
        is: [integer]
        ip: [integer]
    
    Returns:
        returns the Y coordinate of point 'ip' in stratum 'is' (zerobased point counter)

    Description:
    """
    tmp = slope_obj.GetStratumPointY(istra,ip)
    return tmp

def Create2DSection():
    """
    Arguments:

    Returns:

    Description:
        creates a 2D section from the existing strata information
    """
    tmp = slope_obj.Create2DSection()

def NumNodes() -> int:
    """
    Arguments:

    Returns:
        returns the number of "nodes" (vertices of the soil layer polygons)

    Description:
    """
    tmp = slope_obj.NumNodes()

def NodeX(inode:int):
    """
    Arguments:
        inode:  [integer]
    
    Returns:
        returns the X coordinate of node 'inode' (1based node counter)

    Description:
    """
    tmp = slope_obj.NodeX(inode)

def NodeY(inode:int):
    """
    Arguments:
        inode:  [integer]

    Returns:
        returns the Y coordinate of node 'inode' (1based node counter)

    Description:
    """
    tmp = slope_obj.NodeY(inode)

def SetNodeX(inode:int, xnode:float):
    """
    Arguments:
        inode:  [integer]
        xnode:  [float]

    Returns:

    Description:
        sets the X coordinate of node inode.  Caution required not to set invalid data.
    """
    tmp = slope_obj.SetNodeX(inode, xnode)

def SetNodeY(inode:int, ynode:float):
    """
    Arguments:
        inode:  [integer]
        ynode:  [float]

    Returns:

    Description:
        sets the Y coordinate of node inode.
    """
    tmp = slope_obj.SetNodeY(inode, ynode)

#Water data functions
#Note: Index iref in water data functions is 1 based index.

def SetWaterTable(iref:int, dX1:float, fY1:float, dX2:float, dY2:float):
    """
    Arguments:
        iref:   [integer]
        dX1:    [float]
        fY1:    [float]
        dX2:    [float]
        dY2:    [float]

    Returns:

    Description:
    sets water table "iref" to have 2 points at (dX1, dY1) and (dX2, dY2).  "iref" is a 1based counter.  If "iref" equals zero or is greater than the current number of water tables, a new one will be added.
    """
    tmp = slope_obj.SetWaterTable(iref, dX1, fY1, dX2, dY2)

def SetWaterPoint(iref:int, dX:float, dY:float):
    """
    Arguments:
        iref:   [integer]
        dX:     [float]
        dY:     [float]

    Returns:

    Description:
        inserts the point (dX, dY) in xcoordinate order into the water table "iref" (1based counter)
    """
    tmp = slope_obj.SetWaterPoint(iref, dX, dY)

def SetStratumWater(istratum:int, iref:int):
    """
    Arguments:
        istratum:   [integer]
        iref:       [integer]

    Returns:

    Description:
        sets stratum "istratum" to have the water table "iref" Slip circle functions
    """
    tmp = slope_obj.SetStratumWater(istratum, iref)

def SetSingleOrGrid(i:int):
    """
    Arguments:
        i:  [integer]

    Returns:

    Description:
        set 0 for a single circle or 1 for a grid of circle centres
    """
    tmp = slope_obj.SetSingleOrGrid(i)

def SetPosition(x:float, y:float):
    """
    Arguments:
        x:  [float]
        y:  [float]

    Returns:

    Description:
        Coordinates of lower left corner of grid
    """
    tmp = slope_obj.SetPosition(x,y)

def SetNumXCentresAndSpacing(nx:int, dx:float):
    """
    Arguments:
        nx: [integer]
        dx: [float]

    Returns:

    Description:
        set the grid to have nx centres in the x direction at dx distance apart
    """
    tmp = slope_obj.SetNumXCentresAndSpacing(nx, dx)

def SetNumYCentresAndSpacing(ny:int, dy:float):
    """
    Arguments:
        ny: [integer]
        dy: [float]

    Returns:

    Description:
        set the grid to have ny centres in the y direction at dy distance apart
    """
    tmp = slope_obj.SetNumYCentresAndSpacing(ny, dy)

def SetGridAngle(angle:float):
    """
    Arguments:
        angle:  [float]

    Returns:

    Description:
        set the grid to an angle of inclination (positive in the anticlockwise direction from the bottom left of the grid)
    """
    tmp = slope_obj.SetGridAngle(angle)

def SetRadSpec(itype:int):
    """
    Arguments:
        itype:  [integer]

    Returns:

    Description:
        which radius option  set 
    """
    tmp = slope_obj.SetRadSpec(itype)

def SetCommonPoint(x:float, y:float):
    """
    Arguments:
        x:  [float]
        y:  [float]

    Returns:

    Description:
        set the coordinates of the common point through which all slip circles will pass
    """
    tmp = slope_obj.SetCommonPoint(x,y)

def SetRadius(rad:float):
    """
    Arguments:
        rad:    [float]
    Returns:

    Description:
        set the initial radius 
    """
    tmp = slope_obj.SetRadius(rad)

def SetRadInc(rinc:float):
    """
    Arguments:
        rinc:   [float]

    Returns:

    Description:
        set the radius increment.  Slip circles will be increased from the initial radius by this increment, until the maximum possible radius has been analysedResults functions
    """
    tmp = slope_obj.SetRadInc(rinc)

def CriticalCircleRef():
    """
    Arguments:

    Returns:
        returns an integer corresponding to the position, in the results set, of the circle with the lowest factor of safety

    Description:

    """
    tmp = slope_obj.CriticalCircleRef()
    return tmp

def GetMinFoS(iref:int):
    """
    Arguments:
        iref:   [integer]

    Returns:
        returns the factor of safety.  Iref should be the previously obtained critical circle reference.
    
    Description:

    """
    tmp = slope_obj.GetMinFoS(iref)
    return tmp

def GetCriticalCentreX(iref:int):
    """
    Arguments:
        iref:   [integer]

    Returns:
        returns the x coordinate of the circle centre iref

    Description:
    
    """
    tmp = slope_obj.GetCriticalCentreX(iref)
    return tmp

def GetCriticalCentreY(iref:int):
    """
    Arguments:
        iref:   [integer]

    Returns:
        returns the y coordinate of the circle centre iref
    
    Description:

    """
    tmp = slope_obj.GetCriticalCentreY(iref)
    return tmp

def GetCriticalCircleRadius(iref:int):
    """
    Arguments:
        iref:   [integer]

    Returns:
        returns the radius of the slip circle irefLoad functions
    
    Description:
    
    """
    tmp = slope_obj.GetCriticalCircleRadius(iref)
    return tmp

#Note: Index iload in water data functions is 1 based index.
def NumLoads():
    """
    Arguments:

    Returns:
        returns the number of loads

    Description:

    """
    tmp = slope_obj.NumLoads()
    return tmp

def GetXminLoad(iload:int):
    """
    Arguments:
        iload:  [integer]

    Returns:
        returns the minimum X coordinate of load 'iload' (1based load counter)

    Description:
    """
    tmp = slope_obj.GetXminLoad(iload)
    return tmp

def GetXmaxLoad(iload:int):
    """
    Arguments:
        iload:  [integer]

    Returns:
        returns the maximum X coordinate of load 'iload'
    
    Description:

    """
    tmp = slope_obj.GetXmaxLoad(iload)
    return tmp
    
def SetXminLoad(iload:int, xmin:float):
    """
    Arguments:
        iload:  [integer]
        xmin:   [float]

    Returns:

    Description:
        sets the minimum X coordinate of load 'iload'
    """
    tmp = slope_obj.SetXminLoad(iload, xmin)

def SetXmaxLoad(iload:int, xmax:float):
    """
    Arguments:
        iload:  [integer]
        xmin:   [float]

    Returns:

    Description:
        sets the maximum X coordinate of load 'iload'
    """
    tmp = slope_obj.SetXmaxLoad(iload, xmax)

def GetVertLoadIntensity(iload:int):
    """
    Arguments:
        iload:  [integer]

    Returns:

    Description:
        gets the vertical load intensity of load 'iload'
    """
    tmp = slope_obj.GetVertLoadIntensity(iload)
    return tmp

def GetHorzLoadIntensity(iload:int):
    """
    Arguments:
        iload:  [integer]

    Returns:

    Description:
        gets the horizontal load intensity of load 'iload'
    """
    tmp = slope_obj.GetHorzLoadIntensity(iload)
    return tmp

def SetVertLoadIntensity(iload:int, vP:float):
    """
    Arguments:
        iload:  [integer]
        vP:     [float]

    Returns:

    Description:
        sets the vertical load intensity of load 'iload' to 'vP'
    """
    tmp = slope_obj.SetVertLoadIntensity(iload, vP)

def SetHorzLoadIntensity(iload:int, vP:float):
    """
    Arguments:
        iload:  [integer]
        vP:     [float]

    Returns:

    Description:
        sets the horizontal load intensity of load 'iload' to 'vP'Reinforcement functions
    """
    tmp = slope_obj.SetHorzLoadIntensity(iload, vP)

#Note: Index iload in water data functions is 0 based index.

def SetReinfActive(b):
    """
    Arguments:
        b:  [bool]

    Returns:

    Description:
        set reinforcement active if b is nonzero, or inactive if b is zero
    """
    tmp = slope_obj.SetReinfActive(b)

def AddReinforcement(itype:int, bName):
    """
    Arguments:
        itype:  [integer]
        bName:  [BSTR] #CHECK THIS

    Returns:

    Description:
        add a new reinforcement member with name bName, and reinforcement type being  depicted by itype 
        Note itype:
            1 for Ground Anchor, 
            2 for SoilNail, 
            3 for Geotextile, 
            4 for Rock Bolt Type A, 
            5 for Rock Bolt Type B
    """
    tmp = slope_obj.AddReinforcement(itype, bName)

def UpdateSoilNailReinforcement(ireinf:int, soilnail):
    """
    Arguments:
        ireinf:     [integer]
        soilnail:   [struct SoilNail*] #CHECK THIS

    Returns:

    Description:
        updates the Soil Nail reinforcement at index ireinf. The soil nail information is input by passing a SoilNail object. 
    """
    tmp = slope_obj.UpdateSoilNailReinforcement(ireinf, soilnail)

def DeleteReinforcement(ireinf:int):
    """
    Arguments:
        ireinf: [integer]

    Returns:

    Description:
        deletes the reinforcement member at index ireinf (NOTE: index is 0 based)
    """
    tmp = slope_obj.DeleteReinforcement(ireinf)

def ClearReinforcements():
    """
    Arguments:

    Returns:

    Description:
        deletes all the reinforcement members.
    """
    tmp = slope_obj.ClearReinforcements()

def GetSoilNailReinforcement(ireinf:int, soilnail):
    """
    Arguments:
        ireinf:     [integer]
        soilnail:   [struct SoilNail*] #CHECK THIS

    Returns:

    Description:
        retrieves all the soil nail reinforcement parameters in SoilNail object.
    """
    tmp = slope_obj.GetSoilNailReinforcement(ireinf, soilnail)
    return tmp

def GetSoilNailReinforcementName(ireinf:int, ReinfName:str):
    """
    Arguments:
        ireinf:     [integer]
        ReinfName:  [string]

    Returns:

    Description:
        gets the name of the reinforcement with index ireinf
    """
    tmp = slope_obj.GetSoilNailReinforcementName(ireinf, ReinfName)
    return tmp

def GetSoilNailReinforcementNumLayers(ireinf:int, numLayers:int):
    """
    Arguments:
        ireinf:     [integer]
        numLayers:  [integer]

    Returns:

    Description:
        gets the number of layers in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.GetSoilNailReinforcementNumLayers(ireinf, numLayers)
    return tmp

def GetSoilNailReinforcementUppermostLevel(ireinf:int, UppermostLevel:float):
    """
    Arguments:
        ireinf:         [integer]
        UppermostLevel: [float]

    Returns:

    Description:
        gets the upper most layer level in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.GetSoilNailReinforcementUppermostLevel(ireinf, UppermostLevel)
    return tmp

def GetSoilNailReinforcementLayerSpacing(ireinf:int, LayerSpacing:float):
    """
    Arguments:
        ireinf:         [integer]
        LayerSpacing:   [float]

    Returns:

    Description:
        gets the layer spacing in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.GetSoilNailReinforcementLayerSpacing(ireinf, LayerSpacing)
    return tmp

def GetSoilNailReinforcementOffsetFromSlopeSurface(ireinf:int, Offset:float):
    """
    Arguments:
        ireinf:     [integer]
        Offset:     [float]

    Returns:

    Description:
        gets the offset from slope surface of the soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.GetSoilNailReinforcementOffsetFromSlopeSurface(ireinf, Offset)
    return tmp

def GetSoilNailReinforcementTopNailLength(ireinf:int, TopNailLength:float):
    """
    Arguments:
        ireinf:         [integer]
        TopNailLength:  [float]

    Returns:

    Description:
        gets the top nail length of the soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.GetSoilNailReinforcementTopNailLength(ireinf, TopNailLength)
    return tmp

def GetSoilNailReinforcementBottomNailLength(ireinf:int, BottomNailLength:float):
    """
    Arguments:
        ireinf:             [integer]
        BottomNailLength:   [float]

    Returns:

    Description:
        gets the bottom nail length of the in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.GetSoilNailReinforcementBottomNailLength(ireinf, BottomNailLength)
    return tmp

def GetSoilNailReinforcementOutOfPlaneSpacing(ireinf:int, OutOfPlaneSpacing:float):
    """
    Arguments:
        ireinf:             [integer]
        OutOfPlaneSpacing   [float]

    Returns:

    Description:
        gets the out of plane spacing of the in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.GetSoilNailReinforcementOutOfPlaneSpacing(ireinf, OutOfPlaneSpacing)
    return tmp

def GetSoilNailReinforcementTensileCapacity(ireinf:int, TensileCapacity:float):
    """
    Arguments:
        ireinf:             [integer]
        TensileCapacity:    [float]

    Returns:

    Description:
        gets the tensile capacity of the in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.GetSoilNailReinforcementTensileCapacity(ireinf, TensileCapacity)
    return tmp

def GetSoilNailReinforcementPlateCapacity(ireinf:int, PlateCapacity:float):
    """
    Arguments:
        ireinf:         [integer]
        PlateCapacity:  [float]

    Returns:

    Description:
        gets the plate capacity of the in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.GetSoilNailReinforcementPlateCapacity
    return tmp

def IsSoilNailReinforcementBondStrengthCalculated(ireinf:int, Calculated):
    """
    Arguments:
        ireinf:     [integer]
        Calculated: [bool]

    Returns:
        returns bool flag whether the bond strength of the soil nail reinforcement with index ireinf is calculated
    
    Description:
         
    """
    tmp = slope_obj.IsSoilNailReinforcementBondStrengthCalculated
    return tmp

def GetSoilNailReinforcementBondStrength(ireinf:int, BondStrength:int):
    """
    Arguments:
        ireinf:         [integer]
        BondStrength:   [integer]

    Returns:

    Description:
        gets the bond strength of the in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.GetSoilNailReinforcementBondStrength
    return tmp

def GetSoilNailReinforcementAngleFromHorizontal(ireinf:int, Angle:int):
    """
    Arguments:
        ireinf: [integer]
        Angle:  [integer] #why is suggested value a float in oasys manual?

    Returns:

    Description:
        gets the inclination angle of  the soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.GetSoilNailReinforcementAngleFromHorizontal
    return tmp

def GetSoilNailReinforcementGroutDiameter(ireinf:int, GroutDiameter:float):
    """
    Arguments:
        ireinf:         [integer]
        GroutDiameter:  [float]

    Returns:

    Description:
        gets the grout diameter of the in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.GetSoilNailReinforcementGroutDiameter
    return tmp

def SetSoilNailReinforcementName(ireinf:int,  ReinfName):
    """
    Arguments:
        ireinf:     [integer]
        ReinfName:  [BSTR]

    Returns:

    Description:
        sets the name of the reinforcement with index ireinf
    """
    tmp = slope_obj.SetSoilNailReinforcementName

def SetSoilNailReinforcementNumLayers(ireinf:int, numLayers:int):
    """
    Arguments:
        ireinf:     [integer]
        numLayers:  [integer]

    Returns:

    Description:
        sets the number of layers in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.SetSoilNailReinforcementNumLayers

def SetSoilNailReinforcementUppermostLevel(ireinf:int, UppermostLevel:float):
    """
    Arguments:
        ireinf:         [integer]
        UppermostLevel: [float]

    Returns:

    Description:
        sets the upper most layer level in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.SetSoilNailReinforcementUppermostLevel

def SetSoilNailReinforcementLayerSpacing(ireinf:int, LayerSpacing:float):
    """
    Arguments:
        ireinf:         [integer]
        LayerSpacing:   [float]

    Returns:

    Description:
        sets the layer spacing in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.SetSoilNailReinforcementLayerSpacing

def SetSoilNailReinforcementOffsetFromSlopeSurface(ireinf:int, Offset:float):
    """ 
    Arguments:
        ireinf: [integer]
        Offset: [float]

    Returns:

    Description:
        sets the offset from slope surface of the soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.SetSoilNailReinforcementOffsetFromSlopeSurface

def SetSoilNailReinforcementTopNailLength(ireinf:int, TopNailLength:float):
    """ 
    Arguments:
        ireinf:         [integer]
        TopNailLength:  [float]

    Returns:

    Description:
        sets the top nail length of the soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.SetSoilNailReinforcementTopNailLength

def SetSoilNailReinforcementBottomNailLength(ireinf:int, BottomNailLenght:float): #spelling mistaken from manual
    """ 
    Arguments:
        ireinf:             [integer]
        BottomNailLength:   [float]

    Returns:

    Description:
        sets the bottom nail length of the in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.SetSoilNailReinforcementBottomNailLength(ireinf, BottomNailLenght)

def SetSoilNailReinforcementOutOfPlaneSpacing(ireinf:int, OutOfPlaneSpacing:float):
    """ 
    Arguments:
        ireinf: [integer]
        Out:    [float]
    Returns:

    Description:
        sets the out of plane spacing of the in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.SetSoilNailReinforcementOutOfPlaneSpacing(ireinf, OutOfPlaneSpacing)

def SetSoilNailReinforcementTensileCapacity(ireinf:int, TensileCapacity:float):
    """ 
    Arguments:
        ireinf:             [integer]
        TensileCapacity:    [float]

    Returns:

    Description:
        sets the tensile capacity of the in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.SetSoilNailReinforcementTensileCapacity(ireinf, TensileCapacity)

def SetSoilNailReinforcementPlateCapacity(ireinf:int, PlateCapacity:float):
    """ 
    Arguments:
        ireinf:         [integer]
        PlateCapacity:  [float]

    Returns:

    Description:
        sets the plate capacity of the in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.SetSoilNailReinforcementPlateCapacity(ireinf, PlateCapacity)

def SetSoilNailReinforcementBondStrengthCalculated(ireinf:int, Calculated):
    """ 
    Arguments:
        ireinf:     [integer]
        Calculated: [bool]

    Returns:

    Description:
        sets bool flag whether the bond strength of the soil nail reinforcement with index ireinf is calculated 
    """
    tmp = slope_obj.SetSoilNailReinforcementBondStrengthCalculated(ireinf, Calculated)

def SetSoilNailReinforcementBondStrength(ireinf:int, BondStrength:int):
    """ 
    Arguments:
        ireinf:         [integer]
        BondStrength:   [integer]

    Returns:

    Description:
        sets the bond strength of the in soil nail reinforcement with index ireinfSetSoilNailReinforcementAngleFromHorizontal(Integer ireinf, Integer  Angle)  sets the inclination angle of  the soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.SetSoilNailReinforcementBondStrength(ireinf, BondStrength)

def SetSoilNailReinforcementGroutDiameter(ireinf:int, GroutDiameter:float):
    """ 
    Arguments:
        ireinf:         [integer]
        GroutDiameter:  [float]

    Returns:

    Description:
        sets the grout diameter of the in soil nail reinforcement with index ireinf
    """
    tmp = slope_obj.SetSoilNailReinforcementGroutDiameter(ireinf, GroutDiameter)


def SlopeCommands(module):
    """
    Arguments:
        Module
    
    Description:
        e.g. when you import the module via:
            from OasysGeotech import OASYS_Slope
        you can do:
            print(OASYS_Slope.SlopeCommands(OASYS_Slope))
        to return a list of available commands in bulk.
    """
    funcs = dir(module)
    edited = [f for f in funcs if "_" not in f] #list comprehension to remove __doc__ etc
    edited.remove("SlopeCommands")
    return(edited)