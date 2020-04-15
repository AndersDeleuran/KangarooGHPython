# KangarooGHPython

Examples of how to implement [Kangaroo2](http://www.food4rhino.com/project/kangaroo) in [GHPython](http://www.food4rhino.com/project/ghpython). Please note that these examples are a first attempt at using Kangaroo2 with GHPython. So use with caution and be aware that there may be better approaches. Feedback and suggestions are more than welcome. The implementation has the following dependencies which will need to be installed on your system:

ghpython.gha <br/>
KangarooSolver.dll <br/>

**Installing ghpython.gha and KangarooSolver.dll**<br/>
1) Move the files to the Grasshopper Libraries folder (%appdata%\Grasshopper\Libraries). <br/>
2) Unblock them (right-click the file -> Properties -> Unblock -> Ok). <br/>

**Add the Grasshopper Libraries folder path to the RhinoPython paths list**<br/>
In order to implement KangarooSolver.dll using GHPython you will need to add the Grasshopper Libraries folder path to the RhinoPython paths list:

1) In Rhino type in the command "EditPythonScript".<br/>
2) In this Python editor go "Tools -> Options -> Files".<br/>
3) Here you will see an overview of the directories which are currently referenced.<br/>
4) Add a reference to the Grasshopper Libraries folder (it may be hidden, of so [unhide it](http://www.sevenforums.com/tutorials/56005-file-folder-hide-unhide.html)).<br/>
5) Restart Rhino.<br/>
