"""
Use the `AdminApp` object to install, modify, and administer applications.

The `AdminApp` object interacts with the WebSphere® Application Server management 
and configuration services to make application inquiries and changes. 
This interaction includes installing and uninstalling applications, listing modules, 
exporting, and so on.

You can start the scripting client when no server is running, if you want to 
use only local operations. 
To run in local mode, use the `-conntype NONE` option to start the scripting client. 
You receive a message that you are running in the local mode. 

Running the `AdminApp` object in local mode when a server is currently running is not recommended. 
This is because any configuration changes made in local mode will not be reflected in
the running server configuration and vice versa. 
If you save a conflicting configuration, you could corrupt the configuration.

Source:
https://www.ibm.com/docs/en/was-nd/8.5.5?topic=scripting-commands-adminapp-object-using-wsadmin
"""
def deleteUserAndGroupEntries(): # undocumented
	pass

def edit(): # undocumented
	pass

def editInteractive(): # undocumented
	pass

def export(): # undocumented
	pass

def exportDDL(): # undocumented
	pass

def exportFile(): # undocumented
	pass

def getDeployStatus(): # undocumented
	pass

def help(): # undocumented
	pass

def install(): # undocumented
	pass

def installInteractive(): # undocumented
	pass

def isAppReady(): # undocumented
	pass

def list(): # undocumented
	pass

def listModules(): # undocumented
	pass

def options(): # undocumented
	pass

def publishWSDL(): # undocumented
	pass

def searchJNDIReferences(): # undocumented
	pass

def taskInfo(): # undocumented
	pass

def uninstall(): # undocumented
	pass

def update(): # undocumented
	pass

def updateAccessIDs(): # undocumented
	pass

def updateInteractive(): # undocumented
	pass

def view(): # undocumented
	pass
