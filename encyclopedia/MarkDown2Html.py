from re import compile, sub, search, match

class MarkDown2Html():
    
    def __init__(self):		
        self.paragraph = compile(r"(?P<paragraph>.+)")
        self.allAfterHash = compile(r"^#(?P<hash>[^#]+)")
        self.allAfterDoubleHash = compile(r"^[ ]*#{2}(?P<hash>.+)")
        self.boldStar =  compile(r"\*{2}(?P<bold>[a-zA-Z0-9,!,.,?, ,-]+)\*{2}")
        self.boldUnderscore = compile(r"_{2}(?P<bold>[a-zA-Z0-9,!,.,?, ]+)_{2}")
        self.boldUnderscoreTriple = compile(r"_{2}(?P<bold>(_?[a-zA-Z0-9,!,.,?, ]+(?=___)_?)+)_{2}")
        self.italicStar = compile(r"\*(?P<italic>[a-zA-Z0-9,!,.,?, ]+)\*")
        self.italicUnderscore = compile(r"_(?P<italic>[a-zA-Z0-9,!,.,?, ]+)_")
        self.listItem = compile(r"^[-,*](?P<listitem>.+)")
        self.link = compile(r"\[(?P<value>[^]]+)\]\((?P<link>[^)]+)\)")
        
        
        
    def splitInput(self, entry):
        lineList = entry.splitlines();
            
        return lineList;
     
          
    def docheckOfHtmlString(self, htmlString):
        htmlString = htmlString.replace("</ul><ul>", "")
        htmlString = self.boldStar.sub("<b>\g<1></b>", htmlString)
        htmlString = self.link.sub("<a href=\g<2>>\g<1></a>", htmlString)
        return htmlString;     
        
    def convertMarkdown2Html(self, entry):  
        htmlString = ""
        for line in self.splitInput(entry):
            if (self.listItem.search(line) is not None):              
                newItem = self.listItem.sub("<li><p>\g<1></p></li>",line)               
                htmlString = htmlString + "<ul>" + newItem + "</ul>"
                print(htmlString)
                
            elif (self.allAfterHash.match(line) is not None):
                newItem = self.allAfterHash.sub("<h1>\g<1></h1>", line)
                htmlString = htmlString  + newItem
                print(htmlString)
                
            elif (self.allAfterDoubleHash.match(line) is not None):
                newItem = self.allAfterDoubleHash.sub("<h2>\g<1></h2>", line)
                htmlString = htmlString  + newItem
                print(htmlString)
                
            elif (self.paragraph.match(line) is not None):
                newItem = self.paragraph.sub("<p>\g<1></p>", line)
                htmlString = htmlString  + newItem
                print(htmlString)
        
        return self.docheckOfHtmlString(htmlString);
            
                

        
            
            
