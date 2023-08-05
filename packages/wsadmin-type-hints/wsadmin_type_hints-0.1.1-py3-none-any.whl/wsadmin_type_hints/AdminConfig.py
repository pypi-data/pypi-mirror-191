"""
Use the `AdminConfig` object to invoke configuration commands and to create or 
change elements of the WebSphere® Application Server configuration, for example, 
creating a data source.

You can start the scripting client without a running server, if you only want to 
use local operations. 
To run in local mode, use the `-conntype NONE` option to start the scripting client. 
You receive a message that you are running in the local mode. 
If a server is currently running, do not run the `AdminConfig` tool in local mode. 
Configuration changes that are made in local mode are not be reflected in the running
server configuration. 
If you save a conflicting configuration, you could corrupt the configuration.

In a deployment manager environment, configuration updates are available only if 
a scripting client is connected to a deployment manager.

When connected to a node agent or a managed application server, you are not able 
to update the configuration because the configurations for these server processes
are copies of the master configuration that resides in the deployment manager. 
The copies are created on a node machine when a configuration synchronization occurs
between the deployment manager and the node agent.
Make configuration changes to the server processes by connecting a scripting client 
to a deployment manager. 

For this reason, to change a configuration, do not run a scripting client in 
local mode on a node machine.
It is not a supported configuration.

Source:
https://www.ibm.com/docs/en/was-nd/8.5.5?topic=scripting-commands-adminconfig-object-using-wsadmin
"""
from typing import Any
from .wsadmin_types import _OpaqueDigestObject

def attributes(object_type: str) -> str:
	"""Get a multiline string containing the top level attributes for the given type.

	Args:
		object_type (str): name of the object type. Use `AdminConfig.types()` to get a list of available types.

	Returns:
		str: Multiline string the top level attributes for the given type.
	"""
	pass

# TODO: Check return type
def checkin(document_uri: str, file_name: str, opaque_object: _OpaqueDigestObject) -> Any:
	"""Checks a file that the document URI describes into the configuration repository.
	This method only applies to deployment manager configurations.

	Args:
		document_uri (str): The document URI, relative to the root of the configuration repository.
		file_name (str): The name of the source file to check.
		opaque_object (_OpaqueDigestObject): The object returned by a prior call to the `AdminConfig.extract()` command.
	"""
	pass

def convertToCluster(): # undocumented
	pass

def create(): # undocumented
	pass

def createClusterMember(): # undocumented
	pass

def createDocument(): # undocumented
	pass

def createUsingTemplate(): # undocumented
	pass

def defaults(): # undocumented
	pass

def deleteDocument(): # undocumented
	pass

def existsDocument(): # undocumented
	pass

def extract(document_uri: str, filename: str) -> _OpaqueDigestObject:
	"""Extracts a configuration repository file that is described by the document URI and places it in the file named by filename. 
	This method only applies to deployment manager configurations.

	Args:
		document_uri (str): The document URI, relative to the root of the configuration repository. This MUST exist in the repository.
		filename (str): The name of the source file to check. If it exists already, it will be overwritten.

	Returns:
		_OpaqueDigestObject: An opaque "digest" object which should be used to check the file back in using the checkin command.
	"""
	pass

def getCrossDocumentValidationEnabled(): # undocumented
	pass

def getid(): # undocumented
	pass

def getObjectName(): # undocumented
	pass

def getObjectType(): # undocumented
	pass

def getSaveMode(): # undocumented
	pass

def getValidationLevel(): # undocumented
	pass

def getValidationSeverityResult(): # undocumented
	pass

def hasChanges(): # undocumented
	pass

def help(): # undocumented
	pass

def installResourceAdapter(): # undocumented
	pass

def list(): # undocumented
	pass

def listTemplates(): # undocumented
	pass

def modify(): # undocumented
	pass

def parents(): # undocumented
	pass

def queryChanges(): # undocumented
	pass

def remove(): # undocumented
	pass

def required(): # undocumented
	pass

def reset(): # undocumented
	pass

def resetAttributes(): # undocumented
	pass

def save(): # undocumented
	pass

def setCrossDocumentValidationEnabled(): # undocumented
	pass

def setSaveMode(): # undocumented
	pass

def setValidationLevel(): # undocumented
	pass

def show(): # undocumented
	pass

def showall(): # undocumented
	pass

def showAttribute(): # undocumented
	pass

def types(): # undocumented
	pass

def uninstallResourceAdapter(): # undocumented
	pass

def unsetAttributes(): # undocumented
	pass

def validate(): # undocumented
	pass
