"""
Use the `AdminTask` object to run administrative commands with the `wsadmin` tool.

Administrative commands are loaded dynamically when you start the `wsadmin` tool. 
The administrative commands that are available for you to use, and what you can do 
with them, depends on the edition of the product that you use.

You can start the scripting client without having a server running by using the 
`-conntype NONE` option with the wsadmin tool. 

The `AdminTask` administrative commands are available in both connected and local modes. 
If a server is currently running, it is not recommended to run the `AdminTask` commands in 
local mode because any configuration changes made in local mode are not reflected in the 
running server configuration and vice versa. 
If you save a conflicting configuration, you can corrupt the configuration.

In a deployment manager environment, configuration updates are available only if a scripting
client is connected to a deployment manager. 
When connected to a node agent or a managed application server, you cannot update the configuration
because the configuration for these server processes are copies of the master configuration,
which resides in the deployment manager. 
The copies are created on a node machine when a configuration synchronization occurs between 
the deployment manager and the node agent. 
Make configuration changes to the server processes by connecting a scripting client to a deployment manager. 

To change a configuration, do not run a scripting client in local mode on a node machine because 
this is not supported.

Source:
https://www.ibm.com/docs/en/was-nd/8.5.5?topic=scripting-commands-admintask-object-using-wsadmin
"""
def createTCPEndPoint(): # undocumented
	pass

def getTCPEndPoint(): # undocumented
	pass

def help(): # undocumented
	pass

def listTCPEndPoints(): # undocumented
	pass

def listTCPThreadPools(): # undocumented
	pass

def updateAppOnCluster(): # undocumented
	pass
