"""Use the AdminControl object to invoke operational commands that manage objects for the application server.

Many of the AdminControl commands have multiple signatures so that they can either invoke in a raw mode using parameters that are specified by Java Management Extensions (JMX), or by using strings for parameters. In addition to operational commands, the AdminControl object supports some utility commands for tracing, reconnecting with a server, and converting data types.

Avoid trouble: 
When using the commands available in the AdminControl object in large topologies, query and search with process=dmgr and type=Cluster. This method of searching is more efficient, less time consuming, and avoids searching all nodes.

Source:
https://www.ibm.com/docs/en/was-nd/8.5.5?topic=scripting-commands-admincontrol-object-using-wsadmin
"""

def completeObjectName(object_name, template=""):
	""" 
	Use the `completeObjectName` command to create a string representation of a complete `ObjectName` value 
	that is based on a fragment. 
	
	This command does not communicate with the server to find a matching `ObjectName` value. 
	
	If the system finds several MBeans that match the fragment, the command returns the first one. 

	Args:
		object_name (ObjectName): Specifies the name of the object to complete.
		template (str): Specifies the name of the template to use. For example, the template might be `type=Server,*.`.

	Example:
	```
	server_on = AdminControl.completeObjectName('node=mynode,type=Server,*')
	```
	"""
	# TODO: Fix wrong parameters

def getAttribute(object_name, attribute):
	"""Use the `getAttribute` command to return the value of the attribute for the name that you provide.

	If you use the `getAttribute` command to determine the state of an application, one of the following values is returned:
	- 0 - which indicates that the application is starting
	- 1 - which indicates that the application has started
	- 2 - which indicates that the application is stopping
	- 3 - which indicates that the application has stopped
	- 4 - which indicates that the application failed to start

	Args:
		object_name (ObjectName): Specifies the object name of the MBean of interest.
		attribute (str): Specifies the name of the attribute to query.
		
	Example:
	```
	objNameString = AdminControl.completeObjectName('WebSphere:type=Server,*') 
	process_type  = AdminControl.getAttribute(objNameString, 'processType')
	
	print(process_type)
	```
	"""

def getAttribute_jmx(object_name, attribute):
	"""Use the `getAttribute_jmx` command to return the value of the attribute for the name that you provide.

	Args:
		object_name (ObjectName): Specifies the object name of the MBean of interest.
		attribute (str): Specifies the name of the attribute to query.
	
	Example:
	```
	import javax.management as mgmt 

	objNameString = AdminControl.completeObjectName('WebSphere:=type=Server,*') 
	objName       = mgmt.ObjectName(objNameString)
	process_type  = AdminControl.getAttribute_jmx(objName, 'processType')
	
	print(process_type)
	```
	"""

def getAttributes(object_name, attributes):
	"""Use the getAttributes command to return the attribute values for the names that you provide.

	Args:
		object_name (ObjectName): Use the getAttributes command to return the attribute values for the names that you provide.
		attributes (java.lang.String[] or java.lang.Object[]): Specifies the names of the attributes to query.
	
	Example:
	- Using Jython with string attributes:

	```
	objNameString = AdminControl.completeObjectname('WebSphere:type=Server,*)
	attributes    = AdminControl.getAttributes(objNameString, '[cellName nodeName]')
	
	print(attributes)
	```

	- Using Jython with object attributes:
	
	```
	objNameString = AdminControl.completeObjectname('WebSphere:type=Server,*)
	attributes    = AdminControl.getAttributes(objNameString, ['cellName', 'nodeName'])
	
	print(attributes)
	```


	"""

def getAttributes_jmx(): # undocumented
	""" """

def getCell(): # undocumented
	""" """

def getConfigId(): # undocumented
	""" """

def getDefaultDomain(): # undocumented
	""" """

def getDomainName(): # undocumented
	""" """

def getHost(): # undocumented
	""" """

def getMBeanCount(): # undocumented
	""" """

def getMBeanInfo_jmx(): # undocumented
	""" """

def getNode(): # undocumented
	""" """

def getObjectInstance(): # undocumented
	""" """

def getPort(): # undocumented
	""" """

def getPropertiesForDataSource(): # undocumented
	""" (Deprecated) """

def getType(): # undocumented
	""" """

def help(): # undocumented
	""" """

def invoke(): # undocumented
	""" """

def invoke_jmx(): # undocumented
	""" """

def isRegistered(): # undocumented
	""" """

def isRegistered_jmx(): # undocumented
	""" """

def makeObjectName(): # undocumented
	""" """

def queryMBeans(): # undocumented
	""" """

def queryNames(): # undocumented
	""" """

def queryNames_jmx(): # undocumented
	""" """

def reconnect(): # undocumented
	""" """

def setAttribute(): # undocumented
	""" """

def setAttribute_jmx(): # undocumented
	""" """

def setAttributes(): # undocumented
	""" """

def setAttributes_jmx(): # undocumented
	""" """

def startServer(): # undocumented
	""" """

def stopServer(): # undocumented
	""" """

def testConnection(): # undocumented
	""" """

def trace(): # undocumented
	""" """

