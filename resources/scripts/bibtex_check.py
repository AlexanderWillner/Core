#!/usr/bin/env python

"""
BibTeX check on missing fields and consistent name conventions (no BibTeX validator),
especially developed for requirements in Computer Science. 
"""

__author__ = "Fabian Beck"
__version__ = "0.1.2"
__license__ = "MIT"

####################################################################
# Properties (please change according to your needs)
####################################################################

import sys

try:
   file_name = sys.argv[1]
except IndexError:
   print 'Syntax: bibtex_check.py FILENAME'
   sys.exit(1)

# files
bibFile = file_name + ".bib"
auxFile = file_name + ".aux"                # use "" to deactivate restricting the check to the entries listed in the aux file
htmlOutput = "bibtex_check.html"

try:
   with open(bibFile): pass
except IOError:
   print "ERROR: Could not find '" + bibFile + "'"

# links
citeulikeUsername = ""              # if no username is profided, no CiteULike links appear
citeulikeHref = "http://www.citeulike.org/user/"+citeulikeUsername+"/article/"
scholarHref = "http://scholar.google.de/scholar?hl=en&q="
googleHref = "https://www.google.de/search?q="
dblpHref = "https://www.google.de/search?q=dblp "

# fields that are required for a specific type of entry 
requiredFields = (("inproceedings",("author","booktitle","pages","publisher","title","year")),
                ("article",("author","journal","number","pages","title","volume","year")),
                ("techreport",("author","institution","title","year")),
                ("incollection",("author","booktitle","pages","publisher","title","year")),
                ("book",("author","publisher","title","year")),
                ("inbook",("author","booktitle","pages","publisher","title","year")),
                ("proceedings",("editor","publisher","title","year")),
                ("phdthesis",("author","school","title","year")),
                ("mastersthesis",("author","school","title","year")),
                ("electronic",("author","title","url","year")),
                ("misc",("author","howpublished","title","year")),
                )
				
####################################################################

usedIds = set()

try: 
    fInAux = open(auxFile, 'r')
    for line in fInAux:
        if line.startswith("\\citation"):
            ids = line.split("{")[1].rstrip("} \n").split(",")
            for id in ids:
                if (id != ""):
                    usedIds.add(id)
    fInAux.close()
except IOError as e:
    print("no aux file '"+auxFile+"' exists -> do not restrict entities")

fIn = open(bibFile, 'r')
currentId = ""
currentType = ""
currentArticleId = ""
currentTitel = ""
fields = []
problems = []
subproblems = []

counterMissingFields = 0
counterFlawedNames = 0
counterWrongTypes = 0

for line in fIn:
    line = line.strip("\n")
    if line.startswith("@"):
        if currentId in usedIds or not usedIds:
            for requiredFieldsType in requiredFields:
                if requiredFieldsType[0] == currentType:
                    for field in requiredFieldsType[1]:
                        if field not in fields:
                            subproblems.append("missing field '"+field+"'")
                            counterMissingFields += 1
        else:
            subproblems = []
        if subproblems:
            problem = "<div id='"+currentId+"' class='problem severe"+str(len(subproblems))+"'>"
            problem += "<h2>"+currentId+" ("+currentType+")</h2> "
            problem += "<div class='links'>"
            if citeulikeUsername:
                problem += "<a href='"+citeulikeHref+currentArticleId+"'>CiteULike</a>"
            problem += " | <a href='"+scholarHref+currentTitle+"'>Scholar</a>"
            problem += " | <a href='"+googleHref+currentTitle+"'>Google</a>"
            problem += " | <a href='"+dblpHref+currentAuthor+"'>DBLP</a>"
            problem += "</div><ul>"
            for subproblem in subproblems:
                problem += "<li>"+subproblem+"</li>"
            problem += "</ul></div>"
            problems.append(problem)
        currentId = line.split("{")[1].rstrip(",\n")
        currentType = line.split("{")[0].strip("@ ")
        fields = []
        subproblems = []
    else:
        if currentId in usedIds or not usedIds:
            if "=" in line:
                field = line.split("=")[0].strip()
                fields.append(field)
                value = line.split("=")[1].strip("{} ,\n")
                if field == "author":
                    currentAuthor = value
                if field == "citeulike-article-id":
                    currentArticleId = value
                if field == "title":
                    currentTitle = value
                if currentType == "inproceedings" and field == "booktitle":
                    if ":" not in line or "(" in line or ("Proceedings" not in line and "Companion" not in line) or "." in line or " '" not in line or "workshop" in line or "conference" in line or "symposium" in line:
                        subproblems.append("flawed name: '"+value+"'")
                        counterFlawedNames += 1
                if currentType == "article" and field == "journal":
                    if "." in line:
                        subproblems.append("flawed name: '"+value+"'")
                        counterFlawedNames += 1
                if currentType == "proceedings" and field == "pages":
                    subproblems.append("wrong type: should be 'inproceedings'")
                    counterWrongTypes += 1
fIn.close()

html = open(htmlOutput, 'w')
html.write("""<html>
<head>
<title>BibTeX Check</title>
<style>
body {
   font-family: Calibri, Arial, Sans;
   padding: 10px;
}

h1 a {
    color: black;
    text-decoration: none;
}

.info {
    margin: 10px;
    padding: 10px;
    border-radius: 5px;
    background: #EEEEEE;
    width: 250px;
    left: 750px;
    top: 68px;
    border: 1px solid black;
    position: fixed;
}

.info h2 {
    font-size: 12pt;
    padding: 0px;
    margin: 0px;
}

.problem {
    margin-top: 10px;
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 5px;
    background: #FFBBAA;
    counter-increment: problem;
    width: 700px;
    border: 1px solid black;
}

.severe1 {
    background: #FFEEDD;
}

.severe2 {
    background: #FFDDCC;
}

.severe3 {
    background: #FFCCBB;
}

.problem h2:before {
    content: counter(problem) ". "; color: gray;
}

.problem h2 {
    font-size: 12pt;
    padding: 0px;
    margin: 0px;
}

.problem .links {
    float: right;
    position:relative;
    top: -22px;
}

.problem a:visited {
    color: #888888;
    text-decoration: none;
}

.problem ul {
    clear: both;
}
</style>
</head>
<body>
<h1><a href='http://code.google.com/p/bibtex-check'>BibTeX Check</a></h1>""")
html.write("<div class='info'><h2>Info</h2><ul>")
html.write("<li>bib file: "+bibFile+"</li>")
html.write("<li>aux file: "+auxFile+"</li>")
html.write("<li># entries with problems: "+str(len(problems))+"</li>")
html.write("<li># problems: "+str(counterMissingFields+counterFlawedNames+counterWrongTypes)+"</li><ul>")
html.write("<li># missing fields: "+str(counterMissingFields)+"</li>")
html.write("<li># flawed names: "+str(counterFlawedNames)+"</li>")
html.write("<li># wrong types: "+str(counterWrongTypes)+"</li></ul>")
html.write("</ul></div>")

problems.sort()
for problem in problems:
    html.write(problem)
html.write("</body></html>")
html.close()

print "Done. Have a look at " + htmlOutput