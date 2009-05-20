#!/usr/bin/env python

import urllib2
import re
from time import time
from Plugin import Plugin

class UploadedTo(Plugin):
    
    def __init__(self, parent):
        Plugin.__init__(self, parent)
        self.plugin_name = "Uploaded.to"
        self.plugin_pattern = r"http://(www\.)?uploaded.to/"
        self.plugin_type = "hoster"
        self.plugin_config = {}
        pluginProp = {}
        pluginProp ['name'] = "UploadedTo"
        pluginProp ['version'] = "0.1"
        pluginProp ['format'] = "*.py"
        pluginProp ['description'] = """Uploaded Plugin"""
        pluginProp ['author'] = "spoob"
        pluginProp ['author_email'] = "spoob@gmx.de"
        self.pluginProp = pluginProp 
        self.parent = parent
        self.html = None
        self.html_old = None         #time() where loaded the HTML
        self.time_plus_wait = None   #time() + wait in seconds
        self.want_reconnect = None
    
    def set_parent_status(self):
        """ sets all available Statusinfos about a File in self.parent.status
        """
        if self.html == None:
            self.download_html()
        self.parent.status.filename = self.get_file_name()
        self.parent.status.url = self.get_file_url()
        self.parent.status.wait = self.wait_until()
        
    def download_html(self):
        url = self.parent.url
        self.html = req.load(url)

        try:
            wait_minutes = re.search(r"Or wait (\d+) minutes", self.html).group(1)
            self.time_plus_wait = time() + 60 * int(wait_minutes)
            self.want_reconnect = True
        except:
            self.time_plus_wait = 0
        
    def get_file_url(self):
        """ returns the absolute downloadable filepath
        """
        if self.html == None:
            self.download_html()
        if not self.want_reconnect: 
            file_url_pattern = r".*<form name=\"download_form\" method=\"post\" action=\"(.*)\">"
            return re.search(file_url_pattern, self.html).group(1)
        else:
            return False
        
    def get_file_name(self):
        if self.html == None:
            self.download_html()
        if not self.want_reconnect:
            file_name_pattern = r"<title>\s*(.*?)\s+\.\.\."
            return re.search(file_name_pattern, self.html).group(1)
        else:
            return self.parent.url
        
    def file_exists(self):
        """ returns True or False 
        """
        if self.html == None:
            self.download_html()
        if re.search(r"(File doesn't exist .*)", self.html) != None:
            return False
        else:
            return True

    def wait_until(self):
        if self.html == None:
            self.download_html()
        return self.time_plus_wait
    
    def __call__(self):
        return self.plugin_name
