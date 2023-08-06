# Node

## Overview
Node is a node tree application used to interact with objects using a parent/child mapping.
Building an application using nodes helps decouple code and promotes re-usability and abstract configuration.

The advantage to placing application logic in a node tree is the separation of concerns from other application logic
and the ease of extending and reusing that logic.


## Installation
```
pip install node-core
```

## Examples
Creating a node tree application breaks development into three component types:
1. Nodes - Building blocks which contain application logic.
2. Tree - A structure that defines relationships between nodes.
3. Entry Point - The function which calls the root node.


A simple implementation in a single script looks like:
```

from node.core import Node

# 1. Writing the first node component
class PrinterNode(Node):
	def __fit__(self):
		super().__fit__()
		self.initattr('message')

	def __run__(self):
		super().__run__()
		print(self.message)


# 2. Defining the node tree
tree = Node(
	'message_printer_application'
	MessagePrinterNode(
		'hello_printer',
		message='Hello'
	),
	MessagePrinterNode(
		'world_printer',
		message='World'
	)
)


# 3. Writing an entry point function
def main():
	tree.__fit__()
	tree.__run__()


# Executing the application
if __name__ == '__main__':
	main()
```


In the above example we first import the Node class from node.core. We then write a class inheriting from Node.
Within the class the `__fit__` and `__run__` methods are overwritten.
- The `__fit__` method is for resolving any data before the application is run. When breaking down the content of this 
method in the example:
1. `super().__fit__()` -> Calls the `__fit__` method on all child nodes. It's best practice the leave this at the top
of the overwritten function unless there is a good reason to move it or no child should have their `__fit__` method 
called.
2. `self.initattr('message')` -> This creates a new attribute on "message" on this node. If no key word argument named
"message" is sent passed in the tree definition, the message is set to None.

- The `__run__` method for runtime processing. When looking at the above example, this is the "print" statement of the 
application.
1. `super().__run__()` -> calls all `__run__` methods on child nodes. This may move if your logic depends on child nodes
running before this parent.
2. `print(self.message)` -> prints the message set in from `__fit__`.


When defining the tree, we call all of the node's `__init__` method. This takes a string as the instantiated node's 
name, any number of child nodes, and any keyword arguments to be set as attributes.


To extend a node, simply create a new class inheriting from the base node and overwrite the `__fit__` and  `__run__` 
methods as needed.

```
class EchoNode(PrinterNode):
	def __run__(self):
		self.message = input(':')
		super().__run__()
```

This node will now gather input from the user and overwrite the message, then print it. But let's say this is too 
coupled and we want decouple the gathering and printing steps into separate nodes. We can access nodes across the 
tree by accessing the self argument via a pointer.
Pointers here are strings that define the path from one node to another within the tree using unix file path syntax, not 
a pointer to a location in memory such as they are in other level programming languages.

Using the '..' pointer moves self up one node. You could move up multiple nodes by using the same unix style path syntax
such as: '../../../', however if you move above the root node the application will throw an AttribureError.


```
class GathererNode(Node):
	def __run__(self):
		super().__run__()
		self['..'].message = input(':')


tree = Node(
	'echo_tree'
	PrinterNode(
		'printer',
		GathererNode(
			'gatherer'
		)
	)
)

```

When the echo_tree application is run, it will gather input from the user and print it.  

