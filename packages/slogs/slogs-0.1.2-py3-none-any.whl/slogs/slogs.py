import colorama
from colorama import Fore, Style


class slogs():
    def __init__(self, autoprint=True):
        # set variables
        self.autoprint = autoprint
        
        # init colorama
        colorama.init()
    
    def alert(self, content, parent=None):
        output = ""

        # add parent
        if parent != None:   # if parent is defined
            if type(parent) == dict:   # if parent is in default list
                output = parent["color"] + parent["label"]   # add parent
            else:
                output = Fore.BLUE + parent   # add parent
            output += " : "   # add ":"
        
        # add content
        output += Fore.YELLOW + content + Style.RESET_ALL

        if self.autoprint:   # print if autoprint is enable
            print(output)
        
        return output
        
    def error(self, content, parent=None):
        output = ""

        # add parent
        if parent != None:   # if parent is defined
            if type(parent) == dict:   # if parent is in default list
                output = parent["color"] + parent["label"]   # add parent
            else:
                output = Fore.BLUE + parent   # add parent
            output += " : "   # add ":"
        
        # add content
        output += Fore.RED + Style.BRIGHT + "ERROR ! " + Style.NORMAL + content + Style.RESET_ALL
        
        if self.autoprint:   # print if autoprint is enable
            print(output)
            
        return output
        
    def success(self, content, parent=None):
        output = ""

        # add parent
        if parent != None:   # if parent is defined
            if type(parent) == dict:   # if parent is in default list
                output = parent["color"] + parent["label"]   # add parent
            else:
                output = Fore.BLUE + parent   # add parent
            output += " : "   # add ":"
        
        # add content
        output += Fore.GREEN + content + Style.RESET_ALL
        
        if self.autoprint:   # print if autoprint is enable
            print(output)
            
        return output
    
    def note(self, content, parent=None):
        output = ""

        # add parent
        if parent != None:   # if parent is defined
            if type(parent) == dict:   # if parent is in default list
                output = parent["color"] + parent["label"]   # add parent
            else:
                output = Fore.BLUE + parent   # add parent
            output += " : "   # add ":"
        
        # add content
        output += Fore.LIGHTBLACK_EX + content + Style.RESET_ALL
        
        if self.autoprint:   # print if autoprint is enable
            print(output)
            
        return output