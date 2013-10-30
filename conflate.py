import ast
import os
import sys
import pprint

#Accepted commandline reactions to Y/N questions
AFF = ["yes","y","yes'm"]
NEG = ["no","n","nope"]



class confmgr(object):

    def __init__(self, config_filename, 
                 assign_op = "=", comment_op = "#",
                 silent = False, CONF = None):

        """ Initialize the confmgr object.

        Required Arguments:
        config_filename -- string name of the file where configuration is
                           or should be stored.

        Keyword Arguments:
        assign_op -- user defined assignment operator used in the 
                     configuration file.
        comment_op -- user defined comment operator used in the 
                      configuration file.

        NOTE: currently there is no way to escape the operators.

        silent -- True to run module silently

        """

        self.config_filename = config_filename #string
        self.assign_op = assign_op #string
        self.comment_op = comment_op #string
        self.silent = silent #boolean
        self._CONF = None
        self.CONF = CONF #Dictionary of configuration settings

    def readconf(self,
                 read_uservalues = False,
                 protect_config = True):

        """ Reads configuration from file.

        Keyword Arguments:
        read_uservalues -- "True" allows the addition of new keys into the
                           configuration dictionary in memory by reading
                           from disk.
        protect_config -- "False" will turn off functionality that restores
                          configuration dictionary if disk-read goes awry

        Must have a config file on disk, or call to readconf will prompt user
        to touch the file.
        
        A well formed configuration file will contain line separated 
        key-value pairs of the form 'key `assign_op` value'.
        
        NOTE: Currently no support for multi-line values.

        e.g. 'width = 960' , or 'names : [Ray, Augusta, Sally, Mitch]'


        """

        bak = self.CONF.copy()

        try:
            f =  open(self.config_filename, 'r+')
            config_file = f.read()
            f.close()

            if read_uservalues:
                for t in config_file.splitlines():
                    if self.comment_op in t:
                        t = t[:t.find(self.comment_op)]
                    p = t.partition(self.assign_op)
                    entry = p[0].strip()
                    if entry not in self.CONF and not entry == '':
                        self.CONF[entry] = None

            for k in self.CONF:
                for t in config_file.splitlines():
                    if self.comment_op in t:
                        t = t[:t.find(self.comment_op)]
                    p = t.partition(self.assign_op)
                    if k == p[0].strip():
                        try:
                            self.CONF[k] = ast.literal_eval(p[2].strip())
                        except ValueError:
                            print >> sys.stderr, \
                                "CONFLATE: Malformed value for property \'" + \
                                str(k) + "\'"
                            if protect_config:
                                self.CONF = bak
        except IOError as e:
            self.nofile()


    def writeconf(self):

        """ Write changes from self.CONF to disk.

        Creates file if no file is present, prompting in the same manner
        as the `readconf` method. Compares self.CONF to the contents of
        the configuration file; changes values if a difference is present,
        inserts currently missing key-value pairs.

        NOTE: Currently no way to write a single property at a time.
        
        """

        try:
            f =  open(self.config_filename, 'r+')
            config_file = f.read()
            f.close()
            lines = config_file.splitlines()
            for k in self.CONF:
                exists = False
                p = None
                pprime = None
                head = ''
                tail = ''

                for n,t in enumerate(lines[:]):
                    if self.comment_op in t:
                        head = t[:t.find(self.comment_op)]
                        tail = t[t.find(self.comment_op):]
                        p = head.partition(self.assign_op)
                    else:
                        tail = ''
                        p = t.partition(self.assign_op)
                    if k == p[0].strip():
                        exists = True
                        break

                pprime = (str(k), self.assign_op, repr(self.CONF[k]))
                if exists == True:
                    lines[n] = ' '.join(pprime) + ' ' + tail
                else:
                    lines.append(' '.join(pprime))
            f =  open(self.config_filename, 'w')
            f.write('\n'.join(lines))

        except IOError as e:
            self.nofile()
    
    
    def printconf(self):
        
        """ Prints configuration (self.CONF) in an advantageous manner.

        Takes no arguments.

        """

        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.CONF)

    
    ####### Internals

    @property
    def CONF(self):
        return self._CONF

    @CONF.setter
    def CONF(self, raw):
        d = None
        try:
            if isinstance(raw,list):
                d = dict.fromkeys(raw)
            elif isinstance(raw,dict):
                d = raw
        except TypeError:
            print >> sys.stderr, \
                "CONFLATE: Configuration was not in an acceptable format."
        finally:
            self._CONF = d

    def nofile(self):
        # Handling for the absence of a configuration file
        feedback = "Yes"
        if not self.silent:
            feedback = \
                raw_input("No config file found. Touch \'" +
                          self.config_filename+"\' in " + os.getcwd() + "? ")
        if feedback.lower() in AFF:
            print >> sys.stderr, \
                "CONFLATE: No config file found. Touching \'" + \
                self.config_filename+"\' in " + os.getcwd()
            open(self.config_filename,'a+').close()

        else:
            sys.exit()


if __name__=="__main__":
    f = open("test.conf", 'w')
    st = ('# Testfile for conflate configuration manager.\n'
          '# Running conflate.py by itself from its home directory will\n'
          '# modify this file.\n'
          'test1 = False # this is a comment\n' 
          '# Comment on its own line\n'
          "test2 = {'hat': 2, 'baz': ['hi', 'hi', 'hi'], 'flibber': 8}\n" 
          "test3 = 'string'\n"
          'test4 = False')
    f.write(st)
    f.close()

    c = confmgr("test.conf", silent = True, CONF = ['test1','test2','test3'])
    c.readconf()
    c.printconf()
    c.CONF = {'test1': False, 
              'test2' : {'baz':['bye', 'bye', 'bye'], 'hat': 1, 'flibber':7},
              'test3' : 'string'}
    c.writeconf()
    c.readconf(read_uservalues=True)
    c.printconf()

