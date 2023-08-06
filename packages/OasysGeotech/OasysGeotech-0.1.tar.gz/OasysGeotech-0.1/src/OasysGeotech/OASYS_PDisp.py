"""
name: OASYS ALP COM Functions
description: n/a

BY:         MJJ
DATE:       10/02/2023
PURPOSE:    
INPUTS:     N/A

NOTES:		far from complete.
"""


def NewFile():
    """
    Arguments:

    Returns:

    Description:
        Open a new model. 
    """

def Open(filename:str):
    """
    Arguments:
        filename:   [string]

    Returns:

    Description:
        Open a *.pdd file. 
        filename - the name of the file to be opened, including path and extension.
    """

def Save():
    """
    Arguments:

    Returns:

    Description:
        Save the data to the default file(i.e. overwriting the file that was opened or last saved).
    """

def SaveAs(filename:str):
    """
    Arguments:
        filename:   [string]
    
    Returns:

    Description:
        Save the data to*.pdd file. 
        filename - the name of the file to be saved, including path and extension.

    """

def Close():
    """
    Arguments:

    Returns:

    Description:
        Close the current file.  
    """

def Analyse():
    """
    Arguments:

    Returns:

    Description:
        Analyse the current file.
    """

def Delete():
    """
    Arguments:

    Returns:

    Description:
        Deletes the results in the current file.
    """

def Show():
    """
    Arguments:

    Returns:

    Description:
        Show the running instance of PDisp created by the Automation client. 
    """

def AnalysisMethod(sMethod:int):
    """
    Arguments:
        sMethod:    [integer]

    Returns:

    Description:
        Gets the method of analysis. 
        0 - Mindlin 
        1 - Boussinesq 
    """

def SetAnalysisMethod(sMethod:int):
    """
    Arguments:
        sMethod:    [integer]
    Returns:

    Description:
        Sets the method of analysis. 
        0 - Mindlin 
        1 - Boussinesq 
    """

def NumDisplacementData(short* sNumDispData):
    """
    Arguments:

    Returns:

    Description:
        Gets the number of displacement data entries in the current file. 
    """

def NumRectLoads(short* sNumRectLoads):
    """
    Arguments:

    Returns:

    Description:
        Gets the number of rectangular loads in the current file. 
    """

def NumCircLoads(short* sNumCircLoads):
    """
    Arguments:

    Returns:

    Description:
        Gets the number of circular loads in the current file. 
    """

def NumPolyLoads(short* sNumPolyLoads):
    """
    Arguments:

    Returns:

    Description:
        Gets the number of polygonal loads in the current file. 
    """

def NumDisplacementPoints(short* sNumDispPoints):
    """
    Arguments:

    Returns:

    Description:
        Gets the number of displacement points in the current file. 
    """

def NumDisplacementLines(short* sNumDispLines):
    """
    Arguments:

    Returns:

    Description:
        Gets the number of displacement lines in the current file. 
    """

def NumDisplacementGrids(short* sNumDispGrids):
    """
    Arguments:

    Returns:

    Description:
        Gets the number of displacement grids in the current file. 
    """

def NumPointsAlongLine(short sIndex, short* sPoints):
    """
    Arguments:

    Returns:

    Description:
        Gets the number of points along the extrusion direction of the displacement line identified with sIndex.
        sIndex is a one based input.
    """


def NumPointsAlongGrid(short sIndex, short* sPoints):
    """
    Arguments:

    Returns:

    Description:
        Gets the number of points along the extrusion direction of the displacement grid identified with sIndex.
        sIndex is a one based input.

    """

def NumPointsAcrossGrid(short sIndex, short* sPoints):
    """
    Arguments:

    Returns:

    Description:
        Gets the number of points across the extrusion direction of the displacement grid identified with sIndex.
        sIndex is a one based input.
    """


def NumResults(short* sResults):
    """
    Arguments:

    Returns:

    Description:
        Gets the number of results. 
    """


def NumPointResults(short sIndex, short* sResults):
    """
    Arguments:

    Returns:

    Description:
        Gets the number of results of the displacement point identified with sIndex. 
    """


def NumLineResults(short sIndex, short* sResults):
    """
    Arguments:

    Returns:

    Description:
        Gets the number of results of the displacement line identified with sIndex. 
    """


def NumGridResults(short sIndex, short* sResults):
    """
    Arguments:

    Returns:

    Description:
        Gets the number of results of the displacement grid identified with sIndex. 
    """

def GetDisplacementPoint(SHORT sIndex, DisplacementPoint* dispPoint):
    """
    Arguments:

    Returns:

    Description:
        Gets the DisplacementPoint at sIndex.
        sIndex is a one based input.
    """


def GetDisplacementLine(SHORT sIndex, DisplacementLine* dispLine):
    """
    Arguments:

    Returns:

    Description:
        Gets the DisplacementLine at sIndex.
        sIndex is a one based input.
    """


def GetDisplacementGrid(SHORT sIndex, DisplacementGrid* dispGrid):
    """
    Arguments:

    Returns:

    Description:
        Gets the DisplacementGrid at sIndex.
        sIndex is a one based input.
    """


def SetDisplacementPoint(SHORT sIndex, DisplacementPoint* dispPoint):
    """
    Arguments:

    Returns:

    Description:
        Sets the DisplacementPoint at sIndex.
        sIndex is a one based input.
    """


def SetDisplacementLine(SHORT sIndex, DisplacementLine* dispLine):
    """
    Arguments:

    Returns:

    Description:
        Sets the DisplacementLine at sIndex.
        sIndex is a one based input.
    """

def SetDisplacementGrid(SHORT sIndex, DisplacementGrid* dispGrid):
    """
    Arguments:

    Returns:

    Description:
        Sets the DisplacementGrid at sIndex.
        sIndex is a one based input.
    """

def GetRectLoad(SHORT sIndex, RectLoad* rectLoad):
    """
    Arguments:

    Returns:

    Description:
        Gets the RectLoad at sIndex.
        sIndex is a one based input.
    """

def GetCircLoad(SHORT sIndex, CircLoad* circLoad):
    """
    Arguments:

    Returns:

    Description:
        Gets the CircLoad at sIndex.
        sIndex is a one based input.
    """

def GetPolyLoad(SHORT sIndex, PolyLoad* polyLoad):
    """
    Arguments:

    Returns:

    Description:
        Gets the PolyLoad at sIndex.
        sIndex is a one based input.
    """

def SetRectLoad(SHORT sIndex, RectLoad* rectLoad):
    """
    Arguments:

    Returns:

    Description:
        Sets the RectLoad at sIndex.
        sIndex is a one based input.
    """

def SetCircLoad(SHORT sIndex, CircLoad* circLoad):
    """
    Arguments:

    Returns:

    Description:
        Sets the CircLoad at sIndex.
        sIndex is a one based input.
    """

def SetPolyLoad(SHORT sIndex, PolyLoad* polyLoad):
    """
    Arguments:

    Returns:

    Description:
        Sets the PolyLoad at sIndex.
        sIndex is a one based input.
        sIndex is a one based input.
    """

def AddDisplacementPoint(DisplacementPoint* dispPoint):
    """
    Arguments:

    Returns:

    Description:
        Adds the DisplacementPoint.
    """

def AddDisplacementPoint(DisplacementPoint* dispPoint):
    """
    Arguments:

    Returns:

    Description:
        Adds the DisplacementPoint.
    """


def AddDisplacementLine(DisplacementLine* dispLine):
    """
    Arguments:

    Returns:

    Description:
        Adds the DisplacementLine.
    """

def AddDisplacementGrid(DisplacementGrid* dispGrid):
    """
    Arguments:

    Returns:

    Description:
        Adds the DisplacementGrid.
    """


def AddRectLoad(RectLoad* rectLoad):
    """
    Arguments:

    Returns:

    Description:
        Adds the RectLoad.
    """


def AddCircLoad(CircLoad* circLoad):
    """
    Arguments:

    Returns:

    Description:
        Adds the CircLoad.
    """


def AddPolyLoad(PolyLoad* polyLoad):
    """
    Arguments:

    Returns:

    Description:
        Adds the PolyLoad. 
    """


def DeleteDisplacementPoint(SHORT sIndex):
    """
    Arguments:

    Returns:

    Description:
        Deletes the DisplacementPoint at sIndex.
        sIndex is a one based input.
    """

def DeleteDisplacementLine(SHORT sIndex):
    """
    Arguments:

    Returns:

    Description:
        Deletes the DisplacementLine at sIndex.
        sIndex is a one based input.
    """

def DeleteDisplacementGrid(SHORT sIndex):
    """
    Arguments:

    Returns:

    Description:
        Deletes the DisplacementGrid at sIndex.
        sIndex is a one based input.
    """

def DeleteRectLoad(SHORT sIndex):
    """
    Arguments:

    Returns:

    Description:
        Deletes the RectLoad at sIndex.
        sIndex is a one based input.
    """

def DeleteCircLoad(SHORT sIndex):
    """
    Arguments:

    Returns:

    Description:
        Deletes the CircLoad at sIndex.
        sIndex is a one based input.
    """


def DeletePolyLoad(SHORT sIndex):
    """
    Arguments:

    Returns:

    Description:
        Deletes the PolyLoad at sIndex.
        sIndex is a one based input. 
    """

def GetBoussResult_RectLoad(SHORT sIndex, PdispBoussinesqResult* loadResult):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispBoussinesqResult object for the rectangular load identified with sIndex.
        sIndex is a one based input.
        This function is to be called if the analysis method chosen is Boussinesq.
    """

def GetBoussResult_CircLoad(SHORT sIndex, PdispBoussinesqResult* loadResult):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispBoussinesqResult object for the circular load identified with sIndex.
        sIndex is a one based input.
        This function is to be called if the analysis method chosen is Boussinesq.
    """

def GetBoussResult_PolyLoad(SHORT sIndex, PdispBoussinesqResult* loadResult):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispBoussinesqResult object for the polygonal load identified with sIndex.
        sIndex is a one based input.
        This function is to be called if the analysis method chosen is Boussinesq.  
    """
 
def GetBoussResult_DispPoint(SHORT sIndex, PdispBoussinesqResult* dispResult):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispBoussinesqResult object for the displacement point identified with sIndex.
        sIndex is a one based input.
        This function is to be called if the analysis method chosen is Boussinesq.
    """

def GetMindlinResult_RectLoad(SHORT sIndex, PdispMindlinResult* loadResult):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispMindlinResult object for the rectangular load identified with sIndex.
        sIndex is a one based input.
        This function is to be called if the analysis method chosen is Mindlin.
    """

def GetMindlinResult_CircLoad(SHORT sIndex, PdispMindlinResult* loadResult):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispMindlinResult object for the circular load identified with sIndex.
        sIndex is a one based input.
        This function is to be called if the analysis method chosen is Mindlin.
    """

def GetMindlinResult_PolyLoad(SHORT sIndex, PdispMindlinResult* loadResult):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispMindlinResult object for the polygonal load identified with sIndex.
        sIndex is a one based input.
        This function is to be called if the analysis method chosen is Mindlin.   
    """

def GetMindlinResult_DispPoint(SHORT sIndex, PdispMindlinResult* dispResult):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispMindlinResult object for the displacement point identified with sIndex.
        sIndex is a one based input.
        This function is to be called if the analysis method chosen is Mindlin.
        short GetBoussResults_RectLoad(SHORT sIndex, SAFEARRAY(PdispBoussinesqResult)* loadResults)
    """

def THINK_IM_MISSING_A_FUNC():
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispBoussinesqResult object for the rectangular load identified with sIndex.
        sIndex - index of the rectangular load. It is a one based input.
        loadResults - SAFEARRAY of PdispBoussinesqResult objects for the rectangular load identified with sIndex.
        This function is to be called if the analysis method chosen is Boussinesq.
    """

def GetBoussResults_CircLoad(SHORT sIndex, SAFEARRAY(PdispBoussinesqResult)* loadResults):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispBoussinesqResult object for the circular load identified with sIndex.
        sIndex - index of the circular load. It is a one based input.
        loadResults - SAFEARRAY of PdispBoussinesqResult objects for the circular load identified with sIndex.
        This function is to be called if the analysis method chosen is Boussinesq.
    """

def GetBoussResults_PolyLoad(SHORT sIndex, SAFEARRAY(PdispBoussinesqResult)* loadResults):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispBoussinesqResult object for the polygonal load identified with sIndex.
        sIndex - index of the polygonal load. It is a one based input.
        loadResults - SAFEARRAY of PdispBoussinesqResult objects for the polygonal load identified with sIndex.
        This function is to be called if the analysis method chosen is Boussinesq.   
    """

def GetBoussResults_DispPoint(SHORT sIndex, SAFEARRAY(PdispBoussinesqResult)* loadResults):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispBoussinesqResult object for the displacement point identified with sIndex.
        sIndex - index of the displacement point. It is a one based input.
        loadResults - SAFEARRAY of PdispBoussinesqResult objects for the displacement point identified with sIndex.
        This function is to be called if the analysis method chosen is Boussinesq.
    """

def GetBoussResults_DispLine(SHORT sIndex, SAFEARRAY(PdispBoussinesqResult)* loadResults):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispBoussinesqResult object for the displacement line identified with sIndex.
        sIndex - index of the displacement line. It is a one based input.
        loadResults - SAFEARRAY of PdispBoussinesqResult objects for the displacement line identified with sIndex.
        This function is to be called if the analysis method chosen is Boussinesq.
    """



def GetBoussResults_DispGrid(SHORT sIndex, SAFEARRAY(PdispBoussinesqResult)* loadResults):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispBoussinesqResult object for the displacement grid identified with sIndex.
        sIndex - index of the displacement grid. It is a one based input.
        loadResults - SAFEARRAY of PdispBoussinesqResult objects for the displacement grid identified with sIndex.
        This function is to be called if the analysis method chosen is Boussinesq.
    """

def GetMindlinResults_RectLoad(SHORT sIndex, SAFEARRAY(PdispBoussinesqResult)* loadResults):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispMindlinResult object for the rectangular load identified with sIndex.
        sIndex - index of the rectangular load. It is a one based input.
        loadResults - SAFEARRAY of PdispMindlinResult objects for the rectangular load identified with sIndex.
        This function is to be called if the analysis method chosen is Mindlin.
    """



def GetMindlinResults_CircLoad(SHORT sIndex, SAFEARRAY(PdispBoussinesqResult)* loadResults):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispMindlinResult object for the circular load identified with sIndex.
        sIndex - index of the circular load. It is a one based input.
        loadResults - SAFEARRAY of PdispMindlinResult objects for the circular load identified with sIndex.
        This function is to be called if the analysis method chosen is Mindlin.
    """


def GetMindlinResults_PolyLoad(SHORT sIndex, SAFEARRAY(PdispBoussinesqResult)* loadResults):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispMindlinResult object for the polygonal load identified with sIndex.
        sIndex - index of the polygonal load. It is a one based input.
        loadResults - SAFEARRAY of PdispMindlinResult objects for the polygonal load identified with sIndex.
        This function is to be called if the analysis method chosen is Mindlin.
    """

def GetMindlinResults_DispPoint(SHORT sIndex, SAFEARRAY(PdispBoussinesqResult)* loadResults):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispMindlinResult object for the displacement point identified with sIndex.
        sIndex - index of the displacement point. It is a one based input.
        loadResults - SAFEARRAY of PdispMindlinResult objects for the displacement point identified with sIndex.
        This function is to be called if the analysis method chosen is Mindlin.
    """

def GetMindlinResults_DispLine(SHORT sIndex, SAFEARRAY(PdispBoussinesqResult)* loadResults):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispMindlinResult object for the displacement line identified with sIndex.
        sIndex - index of the displacement line. It is a one based input.
        loadResults - SAFEARRAY of PdispMindlinResult objects for the displacement line identified with sIndex.
        This function is to be called if the analysis method chosen is Mindlin.
    """

def GetMindlinResults_DispGrid(SHORT sIndex, SAFEARRAY(PdispBoussinesqResult)* loadResults):
    """
    Arguments:

    Returns:

    Description:
        Gets the PdispMindlinResult object for the displacement grid identified with sIndex.
        sIndex - index of the displacement grid. It is a one based input.
        loadResults - SAFEARRAY of PdispMindlinResult objects for the displacement grid identified with sIndex.
        This function is to be called if the analysis method chosen is Mindlin.
    """



def PDispCommands(module):
    """
    Arguments:
        Module
    
    Description:
        e.g. when you import the module via:
            from OasysGeotech import OASYS_PDisp
        you can do:
            print(OASYS_PDisp.PDispCommands(OASYS_PDisp))
        to return a list of available commands in bulk.
    """
    
    funcs = dir(module)
    edited = [f for f in funcs if "_" not in f] #list comprehension to remove __doc__ etc
    edited.remove("PdispCommands")
    return(edited)