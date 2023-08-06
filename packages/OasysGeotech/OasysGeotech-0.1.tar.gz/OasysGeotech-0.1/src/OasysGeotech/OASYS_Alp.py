"""
name: OASYS ALP COM Functions
description: n/a

BY:         MJJ
DATE:       10/02/2023
PURPOSE:    
INPUTS:     N/A

NOTES:		not complete, needs checking/testing. Fill out descriptions and args etc.
"""


import win32com.client
alp_obj = win32com.client.Dispatch("alpLib_20_0.AlpAuto");

def NewFile(filename:str):
    """
    Arguments:
        filename:   [string]

    Returns:

    Description:
        Open a new model.  The file suffix can be .alw or .json.  If it is not included, it will default to a binary .alw file.
    """
    tmp = alp_obj.NewFile(filename)

def Open(filename:str):
    """
    Arguments:
        filename:   [string]

    Returns:

    Description:
        Open an existing file.  The file suffix should be specified as either .alw or .json.
    """
    tmp = alp_obj.Open(filename)

def Save():
    """
    Arguments:

    Returns:

    Description:
        Save the data to the default file (i.e. overwriting the file that was opened or last saved)
    """
    tmp = alp_obj.Save()

def SaveAs(filename:str):
    """
    Arguments:
        filename:   [string]

    Returns:

    Description:
        Save the data to*.alw file.
        filename - the name of the file to be saved, including path and extension.
    """
    tmp = alp_obj.SaveAs(filename)

def ReadTextFile(filename:str):
    """
    Arguments:
        filename:   [string]

    Returns:

    Description:
        Sets all data in the current document to be equal to that set by a text file.  A template and example '.txt' file are included with the installation demonstrating the required format for any files to be imported.
        filename - the name of the '.txt' file to be imported, including path and extension.
    """
    tmp = alp_obj.ReadTextFile(filename)

def Close():
    """
    Arguments:

    Returns:

    Description:
        Close the current file.
    """
    tmp = alp_obj.Close()

def Show():
    """
    Arguments:

    Returns:

    Description:
        Show the running instance of Alp created by the Automation client
    """
    tmp = alp_obj.Show()

def UpdateVIews():
    """
    Arguments:

    Returns:

    Description:
        Refreshes all the Alp views currently displayed
    """
    tmp = alp_obj.UpdateVIews()

def SetJobNumber(jobnum:str):
    """
    Arguments:
        jobnum: [string]

    Returns:

    Description:

    """
    tmp = alp_obj.SetJobNumber(jobnum)

def SetJobTitle(jobtitle:str):
    """
    Arguments:
        jobtitle:   [string]

    Returns:

    Description:

    """
    tmp = alp_obj.SetJobTitle(jobtitle)

def SetInitials(initials:str):
    """
    Arguments:
        initials:   [string]

    Returns:

    Description:

    """
    tmp = alp_obj.SetInitials(initials)

def SetSubtitle(subtitle:str):
    """
    Arguments:
        subtitle:   [string]

    Returns:

    Description:
    """
    tmp = alp_obj.SetSubtitle(subtitle)

def SetCalcHeader(header:str):
    """
    Arguments:
        header:     [string]

    Returns:

    Description:
    """
    tmp = alp_obj.SetCalcHeader(header)

def SetNotes(notes:str):
    """
    Arguments:
        notes:      [string]

    Returns:

    Description:
        These functions all set the title item to the input string
    """
    tmp = alp_obj.SetNotes(notes)

def SetSoilModel(imodel:int):
    """
    Arguments:
        imodel:     [short]

    Returns:

    Description:
        Sets whether elastic-plastic, generated or specified P-Y model is to be used (parameter should be 0, 1 or 2 respectively)
    """
    tmp = alp_obj.SetSoilModel(imodel)

def SetGlobalSoilEFactor(dFactor:float):
    """
    Arguments:
        dFactor:    [float]

    Returns:

    Description:
        Sets the global soil E factor
    """
    tmp = alp_obj.SetGlobalSoilEFactor(dFactor)

def SetIncType(itype:int):
    """
    Arguments:
        itype:  [integer]

    Returns:

    Description:
        Sets the increment type - 0 loads only, 1 displacements only, 2 both
    """
    tmp = alp_obj.SetIncType(itype)

def SetNumIncs(ninc:int):
    """
    Arguments:
        ninc:   [integer]

    Returns:

    Description:
        Sets the number of analysis increments
    """
    tmp = alp_obj.SetNumIncs(ninc)


def SetAnalysisType(itype:int):
    """
    Arguments:
        itype:  [integer]
    Returns:

    Description:
        Sets analysis type - 0 for standard or 1 for pushover analysis
    """
    tmp = alp_obj.SetAnalysisType(itype)


def GetNumIncs(): #(short* ninc)
    """
    Arguments:

    Returns:
        Gets the number of analysis increments

    Description:
        
    """
    tmp = alp_obj.GetNumIncs()
    return tmp

def ClearNodes():
    """
    Arguments:

    Returns:

    Description:
        Clears all nodes from the data
    """
    tmp = alp_obj.ClearNodes()


def SetToeLevel(dToe:float):
    """
    Arguments:
        dToe:   [float]
        
    Returns:

    Description:
        Sets the toe level of the pile.  This will regenerate nodes if required.  The function fails if the input type is by node rather than by level.
    """
    tmp = alp_obj.SetToeLevel(dToe)

def GetToeLevel(): #double* dToe
    """
    Arguments:

    Returns:
        Returns the toe level of the pile
    
    Description:
    """
    tmp = alp_obj.GetToeLevel()
    return tmp

def SetMaxIterations(max:int):
    """
    Arguments:

    Returns:

    Description:
    """
    tmp = alp_obj.SetMaxIterations(max)

def SetDispTol(dTol:float):
    """
    Arguments:
        dTol:   [float]
        
    Returns:

    Description:

    """
    tmp = alp_obj.SetDispTol(dTol)

def SetPressTol(Tol:float):
    """
    Arguments:
        Tol:    [float]

    Returns:

    Description:

    """
    tmp = alp_obj.SetPressTol(Tol)

def SetDampingCoeff(dDamp):
    """
    Arguments:
        dDamp:  [float]

    Returns:

    Description:

    """
    tmp = alp_obj.SetDampingCoeff(dDamp)

def SetMaxIncDisp(dDisp):
    """
    Arguments:
        dDisp:  [float]

    Returns:

    Description:
        These functions all set the control parameters for the numerical analysis
    """
    tmp = alp_obj.SetMaxIncDisp(dDisp)

def GetNumNodes(): #(short* numnodes)
    """
    Arguments:

    Returns:

    Description:
        Gets the number of nodes in the current file.  NOTE: node numbers are referenced as a 1-based list, so the top node is node 1 in other functions which set or get node-based properties.
    """
    tmp = alp_obj.GetNumNodes()
    return tmp

def GetNodeLevel(inode:int) -> float:
    """
    Arguments:
        inode:  [integer]

    Returns:
        Float level at the given node 

    Description:
        Gets the level of the node identified by sIndex
    """
    tmp = alp_obj.GetNodeLevel(inode)
    return tmp

def InsertNode(dLev, iSect:int):
    """
    Arguments:
        dLev:   [float]
        iSect:  [integer]

    Returns:

    Description:
        Inserts a node into the data at level dLev with pile section iSect.  If the input mode is by level, this function sets it to be by node.
    """
    tmp = alp_obj.InsertNode(dLev, iSect)

def SetNodeSection(inode:int, iSect:int):
    """
    Arguments:
        inode:  []
        iSect:  []

    Returns:

    Description:
        Sets the pile section at node "inode" to section no. iSect
    """
    tmp = alp_obj.SetNodeSection(inode, iSect)

def DeleteNode(inode:int):
    """
    Arguments:
        inode:  [integer]

    Returns:

    Description:
        Deletes node "inode"
    """
    tmp = alp_obj.DeleteNode(inode)

def GetNodeEffWidth(inode:int) -> float: #,double* dWidth
    """
    Arguments:
        inode:  [integer]

    Returns:
        Gets the pile diameter/effective width at the node identified by sIndex

    Description:
    """
    tmp = alp_obj.GetNodeEffWidth(inode)
    return tmp

def GetNodeEI(inode:int) -> float:
    """
    Arguments:
        inode:  [integer]

    Returns:
        EI at inode

    Description:
        Gets the EI value of the pile at the node identified by sIndex
    """
    tmp = alp_obj.GetNodeEI(inode)
    return tmp

def GetNumLoadDisps() -> int:
    """
    Arguments:

    Returns:
        Gets the number of applied loads/displacements

    Description:
    """
    tmp = alp_obj.GetNumLoadDisps()
    return tmp

def AddNodeLoadDisp(inode:int, dForce:float, dMom:float, dAppDisp:float):
    """
    Arguments:
        inode:      [integer]
        dForce:     [integer]
        dMom:       [integer]
        dAppDisp:   [integer]

    Returns:

    Description:
        Adds an applied load and/or displacement at node inode, with load/moment/displacement values in the dForce/dMom/dAppDisp parameters.
    """
    tmp = alp_obj.AddNodeLoadDisp(inode, dForce, dMom, dAppDisp)

def SetNodeLoadDisp(inode:int, dForce:float, dMom:float, dAppDisp:float):
    """
    Arguments:
        inode:      [integer]
        dForce:     [float]
        dMom:       [float]
        dAppDisp:   [float]

    Returns:

    Description:
        As above but updates an existing record if one exists at this node.
    """
    tmp = alp_obj.SetNodeLoadDisp(inode, dForce, dMom, dAppDisp)

def SetNodeLoadAndType(inode:float, dForce:float, dMom:float, dAppDisp:float, isFav:int, isLive:int):
    """
    Arguments:
        inode:      [float]
        dForce:     [float]
        dMom:       [float]
        dAppDisp:   [float]
        isFav:      [integer]
        isLive:     [integer]

    Returns:

    Description:
        Adds a node load at "inode", allowing setting of whether the load is favourable/unfavourable, live/dead by a 1 or 2 respectively in the isFav/isLive parameters.
    """
    tmp = alp_obj.SetNodeLoadAndType(inode, dForce, dMom, dAppDisp, isFav, isLive)

def DeleteNodeLoadDisp(inode:int):
    """
    Arguments:
        inode:  [integer]

    Returns:

    Description:
        Deletes an applied load and/or displacement at inode, with load/moment/displacement values in the dForce/dMom/dAppDisp parameters.
    """
    tmp = alp_obj.DeleteNodeLoadDisp(inode)

def ClearNodeLoadDisps():
    """
    Arguments:

    Returns:

    Description:
        Erases all the applied load and/or displacement.
    """
    tmp = alp_obj.ClearNodeLoadDisps()

def GetNumSections() -> int: #(short* numSec)t
    """
    Arguments:

    Returns:
        Gets the number of pile sections specified in the data.  Section references are a 1-based list so section 1 is the first in the data.

    Description:
    """
    tmp = alp_obj.GetNumSections()
    return tmp

def SetSection(iSect:int, sName:str, iType:int, dEff:float, dEI:float):
    """
    Arguments:
        iSect:  [integer]
        sName:  [string]
        iType:  [integer]
        dEff:   [float]
        dEI:    [float]

    Returns:

    Description:
        Sets an explicit pile section with the given parameters.  This either creates a new section or updates an already existing section.
    """
    tmp = alp_obj.SetSection(iSect, sName, iType, dEff, dEI)

def DeleteSection(iSect:int):
    """
    Arguments:
        iSect:  [integer]

    Returns:

    Description:
        Deletes a pile section from the model
    """
    tmp = alp_obj.DeleteSection(iSect)

def ClearSections():
    """
    Arguments:

    Returns:

    Description:
        Erases all pile sections from the model
    """
    tmp = alp_obj.ClearSections()

def GetNumSoils() -> int: #(short* numsoils)
    """
    Arguments:

    Returns:
        Gets the number of soil layers considered in the model, note this is the number of soil layers, not the number of materials. Soil layer references are 1-based.

    Description:
    """
    tmp = alp_obj.GetNumSoils()

def GetSoilLevel(sIndex:int) -> float: #,double* dLevel)
    """
    Arguments:
        sIndex:     [integer]

    Returns:
        Gets the top level of the soil layer specified by sIndex, with the indexing going from 1 for the top soil layer and increasing with depth.

    Description:
    """
    tmp = alp_obj.GetSoilLevel(sIndex)
    return tmp

def SetElasPlasSoil(iTopNode:int, dEval:float, dUnitWt:float, dCoh:float, dCohGrad:float):
    """
    Arguments:
        iTopNode:   [integer]
        dEval:      [float]
        dUnitWt:    [float]
        dCoh:       [float]
        dCohGrad:   [float]
        
    Returns:

    Description:
        Creates a new elastic-plastic soil or edits an existing one, if iTopNode is already the top node of an existing soil.  The soil parameters are set to the input values for the double parameters of this function.
    """
    tmp = alp_obj.SetElasPlasSoil(iTopNode, dEval, dUnitWt, dCoh, dCohGrad)

def SetEforSoil(sIndex:int, dRefCoh:float):
    """
    Arguments:
        sIndex:     [integer]
        dRefCoh:    [float]

    Returns:

    Description:
        Sets the E value for the specified soil
    """
    tmp = alp_obj.SetEforSoil(sIndex, dRefCoh)

def SetPhiforSoil(sIndex:int, dPhiSoil:float):
    """
    Arguments:
        sIndex:     [integer]
        dPhiSoil:   [float]

    Returns:

    Description:
        Sets the phi value for the specified soil
    """
    tmp = alp_obj.SetPhiforSoil(sIndex, dPhiSoil)

def SetRefCohesionforSoil(sIndex:int, dRefCohesion:float):
    """
    Arguments:
        sIndex:         [integer]
        dRefCohesion:   [float]

    Returns:

    Description:
        Sets the cohesion value for the specified soil.
    """
    tmp = alp_obj.SetRefCohesionforSoil(sIndex, dRefCohesion)

def SetCohesionGradientforSoil(sIndex:int, dCohGrad:float):
    """
    Arguments:
        sIndex:     [integer]
        dCohGrad:   [float]

    Returns:

    Description:
        Sets the cohesion gradient for the specified soil
    """
    tmp = alp_obj.SetCohesionGradientforSoil(sIndex, dCohGrad)

def DeleteElasPlasSoil(sIndex:int):
    """
    Arguments:
        sIndex: [integer]

    Returns:

    Description:
        Deletes the elastic-plastic soil "sIndex" from the model
    """
    tmp = alp_obj.DeleteElasPlasSoil(sIndex)

def ClearElasPlasSoils():
    """
    Arguments:

    Returns:

    Description:
        Deletes all elastic-plastic soils from the model
    """
    tmp = alp_obj.ClearElasPlasSoils()

def AddNodePY(dP1:float, dY1:float, dP2:float, dY2:float, dP3:float, dY3:float, dP4:float, dY4:float, dP5:float, dY5:float, dP6:float, dY6:float):
    """
    Arguments:
        dP1:    [float]
        dY1:    [float]
        dP2:    [float]
        dY2:    [float]
        dP3:    [float]
        dY3:    [float]
        dP4:    [float]
        dY4:    [float]
        dP5:    [float]
        dY5:    [float]
        dP6:    [float]
        dY6:    [float]
        
    Returns:

    Description:
        This function adds a new specified PY point to the file, with dP1 corresponding to P1, dP2 corresponding to Y1, etc.  As with the AddNode function the points must be added in descending order corresponding to the node levels.
    """
    tmp = alp_obj.AddNodePY(dP1, dY1, dP2, dY2, dP3, dY3, dP4, dY4, dP5, dY5, dP6, dY6)

def SetNodePY(iNode:int, dP1:float, dY1:float, dP2:float, dY2:float, dP3:float, dY3:float, dP4:float, dY4:float, dP5:float, dY5:float, dP6:float, dY6:float):
    """
    Arguments:
        iNode:  [integer]
        dP1:    [float]
        dY1:    [float]
        dP2:    [float]
        dY2:    [float]
        dP3:    [float]
        dY3:    [float]
        dP4:    [float]
        dY4:    [float]
        dP5:    [float]
        dY5:    [float]
        dP6:    [float]
        dY6:    [float]

    Returns:

    Description:
        This function is similar to the AddNodePY function, however instead of adding a new PY curve it overwrites an existing curve for the node referenced by iNode.  If no curve has been specified for the node this function will return a fail
    """
    tmp = alp_obj.SetNodePY(iNode, dP1, dY1, dP2, dY2, dP3, dY3, dP4, dY4, dP5, dY5, dP6, dY6)

def ClearSpecPY():
    """
    Arguments:

    Returns:

    Description:
        Deletes all specified PY curves from the currently selected file provided that the soils mode is set to specified PY, for other modes the function will return a fail.
    """
    tmp = alp_obj.ClearSpecPY()

def SetKqforSoil(sIndex:int, KqValue:float):
    """
    Arguments:
        sIndex:     [integer]
        KqValue:    [float]

    Returns:

    Description:
        Sets Kq for the specified soil
    """
    tmp = alp_obj.SetKqforSoil(sIndex, KqValue)

def SetKcforSoil(sIndex:int, KcValue:float):
    """
    Arguments:
        sIndex:     [integer]
        KcValue:    [float]

    Returns:

    Description:
        Sets Kc for the specified soil
    """
    tmp = alp_obj.SetKcforSoil(sIndex, KcValue)
    
def GetNumWaterPoints():
    """
    Arguments:

    Returns:
        Gets the number of water data points
        
    Description:
    """
    tmp = alp_obj.GetNumWaterPoints()
    return tmp

def SetWaterPoint(dLev:float, dPressure:float, dUnitWt:float):
    """
    Arguments:
        dLev:       [float]
        dPressure:  [float]
        dUnitWt:    [float]

    Returns:

    Description:
        Sets a water data point at level dLev with the specified values for pore pressure and unit weight
    """
    tmp = alp_obj.SetWaterPoint(dLev, dPressure, dUnitWt)

def GetPorePressureAtLevel(dLEv:float): # double* dPorePress
    """
    Arguments:
        dLEv:   [float]

    Returns:
        Returns the pore pressure at the specified level.  This is interpolated between water data points.

    Description:
    """
    tmp = alp_obj.GetPorePressureAtLevel(dLEv)
    return tmp

def GetPorePressureAtNode(inode:int): # double* dPorePress
    """
    Arguments:
        inode:  [integer]

    Returns:
        Returns the pore pressure at the specified node.  This is interpolated between water data points.

    Description:
    """
    tmp = alp_obj.GetPorePressureAtNode(inode)
    return tmp

def DeleteWaterPoint(iref:int):
    """
    Arguments:
        iref:   [integer]

    Returns:

    Description:
        Deletes the water data point "iref" (1-based)
    """
    tmp = alp_obj.DeleteWaterPoint(iref)

def ClearWaterPoints():
    """
    Arguments:

    Returns:

    Description:
        Deletes all water data points
    """
    tmp = alp_obj.ClearWaterPoints()

def MaxDisp() -> float: #double* dMaxDisp
    """
    Arguments:

    Returns:
        Gets the maximum displacement of the pile.

    Description:
       
    """
    tmp = alp_obj.MaxDisp()
    return tmp

def GetNodeDisp(sIndex:int) -> float: # double* dDisp
    """
    Arguments:
        sIndex: [integer]

    Returns:
        Gets the pile displacement at the node identified by sIndex.

    Description:
    """
    tmp = alp_obj.GetNodeDisp(sIndex)
    return tmp

def GetNodeRotation(sIndex:int): #double* dRot
    """
    Arguments:
        sIndex: [integer]

    Returns:
        Gets the pile rotation at the node identified by sIndex.

    Description:
    """
    tmp = alp_obj.GetNodeRotation(sIndex)
    return tmp

def GetNodeShear(sIndex:int, Below:bool): #double* dShear
    """
    Arguments:
        sIndex: [integer]
        Below:  [bool]

    Returns:

    Description:
        Gets the pile shear at the node identified by sIndex. If the BOOL value is TRUE, the function returns the shear just below the node, otherwise it returns the shear just above the node.
    """
    tmp = alp_obj.GetNodeShear(sIndex, Below)
    return tmp

def GetNodeBM(sIndex:int, Below:bool) -> float: # double* dNodeBM
    """
    Arguments:
        sIndex: [integer]
        Below:  [bool]

    Returns:
        Gets the pile bending moment at the node identified by sIndex.
    
    Description:
        
    """
    tmp = alp_obj.GetNodeBM(sIndex,Below)
    return tmp

def MaxBM(): #(double* dMaxBending
    """
    Arguments:

    Returns:

    Description:
        Gets the maximum magnitude of bending moment down the pile, i.e. -122kNm will be returned from this function if the maximum positive bending moment is less than 122kNm.
    """
    tmp = alp_obj.MaxBM()
    return tmp

def MaxShear(): #double* dMaxShear
    """
    Arguments:

    Returns:
        Gets the maximum magnitude of shear force down the pile, i.e. -95kN will be returned from this function if the maximum positive bending moment is less than 95kN.

    Description:
    """
    tmp = alp_obj.MaxShear()
    return tmp

def ReadTextFile(sPath:str):
    """
    Arguments:
        sPath:  [string]

    Returns:

    Description:
        Reads all model data from the specified text file.
    """
    tmp = alp_obj.ReadTextFile(sPath)

def Export(sPath:str):
    """
    Arguments:
        sPath:  [string]

    Returns:

    Description:
        Exports the text output of results to various formats.  This function may pop up message boxes.
    """
    tmp = alp_obj.Export(sPath)

def ExportCSV(sPath:str):
    """
    Arguments:
        sPath:  [string]

    Returns:

    Description:
        Exports the text output of results to a csv file. The file path and extension should be specified in the sPath variable.
    """
    tmp = alp_obj.ExportCSV(sPath)

def ExportCSVResult(sPath:str, iType:int, iInc:int):
    """
    Arguments:
        sPath:  [string]
        iType:  [integer]
        iInc:   [integer]

    Returns:

    Description:
        Exports a csv table from the current file.  The string sPAth needs to specify the full file path, name and extension.  iType indicates which result to export and can have the following values - 0 for the bending moment profile with depth, 1 for the shear profile with depth and 2 the displacement profile with depth.   iInc indicates the load increment for which the results are required.
    """
    tmp = alp_obj.ExportCSVResult(sPath, iType, iInc)

def ExportCSVPushOver(sPath:str):
    """
    Arguments:
        sPath:  [string]

    Returns:

    Description:
        This function exports a csv table from the current file showing the pushover curve for the top node (i.e. the lateral load v displacement for the top node for the number of increments analysed).  The string sPath needs to specify the full file path, name and extension.
    """
    tmp = alp_obj.ExportCSVPushOver(sPath)

def ExportCSVPY(sPath:str, iNode:int):
    """
    Arguments:
        sPath:  [sPath]
        iNode:  [iNode]

    Returns:

    Description:
        Exports generated P-Y curves for node iNode to the file sPath.
    """
    tmp = alp_obj.ExportCSVPY(sPath, iNode)

def DeleteResults():
    """
    Arguments:

    Returns:

    Description:
        Deletes the results in the current file.
    """
    tmp = alp_obj.DeleteResults()

def Analyse():
    """
    Arguments:

    Returns:

    Description:
        Analyses the current data
    """
    tmp = alp_obj.Analyse()

def PrintTabular(bsPath:str, bNotes:bool, bGen:bool, bConv:bool, bPartFacts:bool, bSoils:bool, bSects:bool, bPileP:bool, bLoads:bool, bPush:bool, bRest:bool, bSurch:bool, bGeom:bool, bResults:bool):
    """
    Arguments:
        bsPath:     [string]
        bNotes:     [bool]
        bGen:       [bool]
        bConv:      [bool]
        bPartFacts: [bool]
        bSoils:     [bool]
        bSects:     [bool]
        bPileP:     [bool]
        bLoads:     [bool]
        bPush:      [bool]
        bRest:      [bool]
        bSurch:     [bool]
        bGeom:      [bool]
        bResults:   [bool]

    Returns:

    Description:
        Prints the tabular output to a file "sPath".  The BOOL parameters should be set to 1 when a particular data item is required in the output.  The parameters are for Notes, General Data, Convergence Data, Partial Factors, Soil Data, Sections, ... , Applied Loads/Displacements, Pushover, Restraints, Surcharges, Geometry and Results respectively.
    """
    tmp = alp_obj.PrintTabular(bsPath, bNotes, bGen, bConv, bPartFacts, bSoils, bSects, bPileP, bLoads, bPush, bRest, bSurch, bGeom, bResults)

def PrintGraphical(sPath:str, bDisp:bool, bRotation:bool, bPressure:bool, bBbending:bool, bShear:bool):
    """
    Arguments:
        sPath:      [string]
        bDisp:      [bool]
        bRotation:  [bool]
        bPressure:  [bool]
        bBbending:  [bool]
        bShear:     [bool]

    Returns:

    Description:
        Prints a graphical view to a png file "sPath".  The BOOL parameters switch on display of: displacement, rotation, pressure, bending moment and shear force respectively.
    """
    tmp = alp_obj.PrintGraphical(sPath, bDisp, bRotation, bPressure, bBbending, bShear)

def AddRestraint(iNode:int, dLS:float, dRS:float):
    """
    Arguments:
        iNode:  [integer]
        dLS:    [float]
        dRS:    [float]

    Returns:

    Description:
        Adds a restraint at node iNode with Lateral Stiffness equal to dLS and Rotational stiffness equal to dRS   
    """
    tmp = alp_obj.AddRestraint(iNode, dLS, dRS)

def ModifyRestraint(iIndex:int, iNode:int, dLS:float, dRS:float):
    """
    Arguments:
        iIndex: [integer]
        iNode:  [integer]
        dLS:    [float]
        dRS:    [float]

    Returns:

    Description:
        Modifies the values of node, lateral stiffness, rotational stiffness for the restraint at index iIndex. Note: index is 1-based.   
    """
    tmp = alp_obj.ModifyRestraint(iIndex, iNode, dLS, dRS)

def DeleteRestraint(iIndex:int):
    """
    Arguments:

    Returns:

    Description:
        Deletes the restraint at index iIndex. Note: index is 1-based.
    """
    tmp = alp_obj.DeleteRestraint(iIndex)

def GetNumberofRestraint(): #short* iNum
    """
    Arguments:

    Returns:
        Returns the total number of restraints defined.

    Description:
    """
    tmp = alp_obj.GetNumberofRestraint()

def GetNumModificationFactors(): #short* iNum
    """
    Arguments:

    Returns:
        Returns the total number of modification factor records defined.

    Description:
    """
    tmp = alp_obj.GetNumModificationFactors()

def AddModificationFactor(level:float, factor:float):
    """
    Arguments:

    Returns:

    Description:
        Adds a modification factor record.
    """
    tmp = alp_obj.AddModificationFactor(level, factor)

def GetModificationFactor(iIndex:int): #, double* level, double* factor
    """
    Arguments:

    Returns:
        Gets the level and factor specified for record identified by iIndex. iIndex is a 1 based input. Will return failure if iIndex is greater than the number of records.

    Description:
    """
    tmp = alp_obj.GetModificationFactor(iIndex)

def DeleteModificationFactor(iIndex:int):
    """
    Arguments:

    Returns:

    Description:
        Deletes the record identified by iIndex. iIndex is a 1 based input.  Will return failure if iIndex is greater than the number of records.
    """
    tmp = alp_obj.DeleteModificationFactor(iIndex)

def SetModificationFactor(iIndex:int, level:float, factor:float):
    """
    Arguments:

    Returns:

    Description:
        Sets the record identified by iIndex. iIndex is a 1 based input. Will return failure if iIndex is greater than the number of records.
    """
    tmp = alp_obj.SetModificationFactor(iIndex, level, factor)

def AddLoadDispByLevel(dLevel:float, dforce:float, dmoment:float, dAppDisp:float):
    """
    Arguments:

    Returns:

    Description:
        Adds a new record in applied loads & displacements table in a level based input file - with application level as dLevel, force as dforce, moment as dmoment, and applied soil displacement as dAppDisp.
    """
    tmp = alp_obj.AddLoadDispByLevel(dLevel, dforce, dmoment, dAppDisp)

def SetLoadDispByLevel(index:int, dLevel:float, dForce:float, dMoment:float, dDisp:float):
    """
    Arguments:

    Returns:

    Description:
        Updates the record with index iIndex in restraints table in a level based input file - with restraint level as dLevel, lateral stiffness as dLS, and rotational stiffness as dRS.
    """
    tmp = alp_obj.SetLoadDispByLevel(index, dLevel, dForce, dMoment, dDisp)

def AddRestraintByLevel(dLevel:float, dLS:float, dRS:float):
    """
    Arguments:

    Returns:

    Description:
        Adds a new record in restraints table in a level based input file - with restraint level as dLevel, lateral stiffness as dLS, and rotational stiffness as dRS.
    """
    tmp = alp_obj.AddRestraintByLevel

def ModifyRestraintByLevel(iIndex:int, dLS:float, dRS:float):
    """
    Arguments:

    Returns:

    Description:
        Updates the record having index iIndex in restraints table in a level based input file - with restraint level as dLevel, lateral stiffness as dLS, and rotational stiffness as dRS .
    """
    tmp = alp_obj.ModifyRestraintByLevel

def AddElasPlasSoilByLevel(dLevel:float, dEval:float, dUnitWt:float, dCoh:float, dCohGrad:float):
    """
    Arguments:

    Returns:

    Description:
        Adds a new Elastic-plastic soil material data record in soils table in a level based input file - level as dLevel, Youngs modulus as dEVal, unit weight as dUnitWt, cohesion as dCoh, and cohesion gradient as dCohGrad.
    """
    tmp = alp_obj.AddElasPlasSoilByLevel

def SetElasPlasSoilByLevel(iIndex:int, dLevel:float, dEval:float, dUnitWt:float, dCoh:float, dCohGrad:float):
    """
    Arguments:

    Returns:

    Description:
        Sets the Elastic-plastic soil material data for record with index "iIndex" in soils table in a level based input file - level as dLevel, Youngs modulus as dEVal, unit weight as dUnitWt, cohesion as dCoh, and cohesion gradient as dCohGrad.
    """
    tmp = alp_obj.SetElasPlasSoilByLevel(iIndex, dLevel, dEval, dUnitWt, dCoh, dCohGrad)

def AddSectionAssignementByLevel(dLevel:float, iSection:int):
    """
    Arguments:

    Returns:

    Description:
        Adds a new record in Section Assignment table in a level based input file - with section having index iSection at level dLevel.
    """
    tmp = alp_obj.AddSectionAssignementByLevel(dLevel, iSection)
    
def SetSectionAssignementByLevel(i:int, dLevel:float, iSection:int):
    """
    Arguments:

    Returns:

    Description:
        Sets the section assignment data (new level = dLevel in user defined units, and new section index = iSection) for record with index 'i' in a level based input data file.
    """
    tmp = alp_obj.SetSectionAssignementByLevel(i, dLevel, iSection)
    
def DeleteSectionAssignementByLevel(i:int):
    """
    Arguments:

    Returns:

    Description:
        Deletes the section assignment record with index 'i' in a level based input data file.
    """
    tmp = alp_obj.DeleteSectionAssignementByLevel(i)
    
def ClearSectionAssignementByLevel():
    """
    Arguments:

    Returns:

    Description:
        Clears the section assignment data in a level based input data file.
    """
    tmp = alp_obj.ClearSectionAssignementByLevel()
    
def MaxBMNodeLevel(): #double* pMaxBending
    """
    Arguments:

    Returns:
        Gets the node level corresponding to maximum absolute bending moment along the pile length.

    Description:
    """
    tmp = alp_obj.MaxBMNodeLevel()
    return tmp
    
def MaxShearNodeLevel(): #double* pMaxShear
    """
    Arguments:

    Returns:
        Gets the node level corresponding to maximum absolute shear along the pile length.

    Description:
    """
    tmp = alp_obj.MaxShearNodeLevel()
    return tmp 

def MaxDispNodeLevel(): #double* pMaxShear
    """
    Arguments:

    Returns:
        Gets the node level corresponding to maximum absolute displacement along the pile length.

    Description:
    """
    tmp = alp_obj.MaxDispNodeLevel()
    
def MaxRotationNodeLevel(): #double* pMaxShear
    """
    Arguments:

    Returns:
        Gets the node level corresponding to maximum absolute rotation along the pile length.

    Description:
    """
    tmp = alp_obj.MaxRotationNodeLevel()
    return tmp

def SetLengthUnit(length_string:str):
    """
    Arguments:

    Returns:

    Description:
        Sets the length or level units in the file.
    """
    tmp = alp_obj.SetLengthUnit(length_string)
    
def SetDisplacementUnit(disp_string:str):
    """
    Arguments:

    Returns:

    Description:
        Sets the displacement units in the file.
    """
    tmp = alp_obj.SetDisplacementUnit(disp_string)
    
def SetStressUnit(stress_string:str):
    """
    Arguments:

    Returns:

    Description:
        Sets the stress units in the file.
    """
    tmp = alp_obj.SetStressUnit(stress_string)
    
def SetForceUnit(force_string:str):
    """
    Arguments:

    Returns:

    Description:
        Sets the force units in the file.
    """
    tmp = alp_obj.SetForceUnit(force_string)
    
def GetLengthUnit(): #BSTR* length_string
    """
    Arguments:

    Returns:
        Gets the length or level units in the file.

    Description:
    """
    tmp = alp_obj.GetLengthUnit()
    return tmp
    
def GetDisplacementUnit(): #BSTR* disp_string
    """
    Arguments:

    Returns:
        Gets the displacement units in the file.

    Description:
    """
    tmp = alp_obj.GetDisplacementUnit()
    return tmp
    
def GetStressUnit(): #BSTR* stress_string
    """
    Arguments:

    Returns:
        Gets the stress units in the file.

    Description:
    """
    tmp = alp_obj.GetStressUnit()
    return tmp  

def GetForceUnit(): #BSTR*force_string
    """
    Arguments:

    Returns:
        Gets the force units in the file.

    Description:
    """
    tmp = alp_obj.GetForceUnit()
    return tmp
    
def ALPCommands(module) -> list:
    """
    Arguments:
        Module
    
    Description:
        e.g. when you import the module via:
            from OasysGeotech import OASYS_Alp
        you can do:
            print(OASYS_Alp.ALPCommands(OASYS_Alp))
        to return a list of available commands in bulk.
    """

    funcs = dir(module)
    edited = [f for f in funcs if "_" not in f] #list comprehension to remove __doc__ etc
    edited.remove("ALPCommands")
    edited.remove("win32com")

    return(edited)