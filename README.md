 conflate
===========

A late-to-the-party, lightweight, stupid simple configuration manager.

 Install
----------

`python setup.py install` should do it.


 Use Cases
-----------

1. Create a dictionary full of the properties you'll want to be able to 
load from a file.
   ```python
   
   config = { height : 600,
              width : 960,
			  database_location : '/var/databas/foo',
			  pages : ['index.html', 'upload.html', 'template.html'],
			  preferences : None
			}
			
	```
	Yes, you may put anything you want as a value. These will probably be 
	your defaults. Put `None` if you don't want the property to have a 
	default.
	
	
2. You can create a confmgr object with a configuration specified, or just
   give it the filename(required) and wait until later. Configuration needs to
   be in the working directory and will be created (by a read or write) 
   if not present.
   
   ```python
   
   from conflate import confmgr
   
   c = confmgr('test.conf', CONF=config) # from above

   ```
   
3. And now you can write to disk with `writeconf`, read from disk 
   with `readconf`, and check your configuration with `printconf`.
   
   ```python
   
   c.writeconf() # writes out initial configuration
   c.readconf() # sync contents of CONF with disk
   c.printconf() # is everything okay?
   
   
   ```
   
4. Changing properties is as easy as editing a dictionary.

   ```python
   
   c.CONF['width'] = 700 # update an exisiting one
   c.CONF['comment'] = 'This is a test' # and make a new one
   c.writeconf() # ...and write everything to disk.
   
   ```
 Options   
--------------

+ confmgr can take named attributes:
 + assign_op - change the assignment operator to whatever you please. 
   Defaults to '='.
   e.g. '=' for `test = 1` or ':' for `test : 1`
 + comment_op - change comment symbol to whatever you please.
   Defaults to '#'
   e.g. '#' for `# is a comment` or ';' for `; is a comment`
 + silent - a boolean that will silence any prompts
 + CONF - the property that contains the configuration dict. Can be assigned
   at object creation as an attribute, or directly later.


 If I were you
---------------

Ship a configuration file with your product, or write a script to set it up 
the first time. This way you can include comments and defaults that can be 
changed later.

An example configuration file can be found in the source. It is named 
'test.conf'.

