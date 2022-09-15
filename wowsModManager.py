import requests
import os
import zipfile
import shutil
import distutils
from distutils import dir_util
from xml.dom import minidom
from colorama import Fore

version = "1.0.0"

modTypes = {
    "crosshair" : "Crosshair",
    "hudlib" : "HudLib",
    "shipicons" : "ShipIcons",
    "shipshell" : "ShipShell",
    "ui" : "UI",
    "port" : "Port",
    "other" : "Other"
}

modTags = {
    "crosshair" : "CH",
    "hudlib" : "HL",
    "shipicons" : "SI",
    "shipshell" : "SS",
    "ui" : "UI",
    "port" : "PM",
    "other" : "OT"
}

fileObject = open("wowsModManager.txt", "r") #read game location from txt
gameloc = fileObject.read().replace("\\", "/").strip("\n") #Strip newlines that appeared on Linux, not Windows
resmods = ""

dirlist = [ item for item in os.listdir(gameloc + "/bin") if os.path.isdir(os.path.join(gameloc + "/bin", item)) ]

#Hardcoded backup game version
version = "0.11.8.0"

#Check latest game version from wargaming servers, we assume EU
try:
    gameurl = "http://csis.worldoftanks.eu/csis/wowseu/"
    gameinfo = requests.get(gameurl)
    xmldoc = minidom.parseString(gameinfo.text)
    models = xmldoc.getElementsByTagName('version')
    latestversion = models[0].firstChild.nodeValue
    splitversion = latestversion.split(".")
    #Clean off game version to 0.0.0.0 format
    version = latestversion[:-(len(splitversion[4])+1)]
    print("Latest version from server is " + version)
except:
    print("Failed to retrieve latest game version from wargaming servers, defaulting to hardcoded version of 0.11.8.0")

#Find latest bin
highest = "0"
for name in dirlist:
    if int(name) > int(highest):
        highest = name
print("highest bin name is " + highest)
resmods = gameloc + "/bin/" + highest + "/res_mods/"
print("res_mods is " + resmods)

#Get url for game version
baseurl = "http://dl-wows-cdx.wargaming.net/projects/mods/ModStation/release/%version%_2/.Cache/%version%/"

baseurl = baseurl.replace("%version%", version)

print("Welcome to pyStation.")

#Uninstall a mod
def uninstall(modname):
    print("Starting uninstall of " + modname + "...")
    #Form the mod zip url
    file = minidom.parse('modlist.xml')
    models = file.getElementsByTagName('Item')

    modurl = "NULL"
    for elem in models:
        if(elem.attributes['Name'].value == modname):
            modurl = elem.getElementsByTagName("Path")[0].firstChild.data

    if(modurl == "NULL"):
        print("Failed to find mod url for " + modname + "!")
        return

    #modurl = "UI/UI_ShipList/UI_ShipList_v2/UI_ShipList_v2.zip"
    url = baseurl + modurl

    #Download mod
    print("Downloading zip...")
    try:
        myfile = requests.get(url)

        tempfile = os.path.dirname(__file__)+"/tempdownload.zip"
        open(os.path.dirname(__file__)+"/tempdownload.zip", 'wb').write(myfile.content)

        #Prepare to extract deleting possible old files
        if os.path.isdir(os.path.dirname(__file__)+"/extract"):
            shutil.rmtree(os.path.dirname(__file__)+"/extract")
        os.mkdir(os.path.dirname(__file__)+"/extract")

        print("Extracting files...")
        #Extract
        with zipfile.ZipFile(tempfile, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(__file__)+"/extract")

        print("Deleting installed mod files...")
        for filename in os.listdir(os.path.dirname(__file__)+"/extract"):
            file_path = os.path.join(resmods, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        print("Cleaning up...")
        #Clean
        shutil.rmtree(os.path.dirname(__file__)+"/extract")
        os.remove(os.path.dirname(__file__)+"/tempdownload.zip")
    except:
        print("Error!") #Very generic

#Install a mod
def install(modname):
    print("Starting install of " + modname + "...")
    #Form the mod zip url
    file = minidom.parse('modlist.xml')
    models = file.getElementsByTagName('Item')

    modurl = "NULL"
    for elem in models:
        if(elem.attributes['Name'].value == modname):
            modurl = elem.getElementsByTagName("Path")[0].firstChild.data
            if elem.getElementsByTagName("Patch"):
                print(Fore.RED + "WARNING: This mod has a patch file. Patches may require extensive manual file edits." + Fore.WHITE)

    

    if(modurl == "NULL"):
        print("Failed to find mod url for " + modname + "!")
        return

    #modurl = "UI/UI_ShipList/UI_ShipList_v2/UI_ShipList_v2.zip"
    url = baseurl + modurl

    #Download mod
    print("Downloading zip...")
    try:
        myfile = requests.get(url)

        tempfile = os.path.dirname(__file__)+"/tempdownload.zip"
        open(os.path.dirname(__file__)+"/tempdownload.zip", 'wb').write(myfile.content)

        #Prepare to extract deleting possible old files
        if os.path.isdir(os.path.dirname(__file__)+"/extract"):
            shutil.rmtree(os.path.dirname(__file__)+"/extract")
        os.mkdir(os.path.dirname(__file__)+"/extract")

        print("Extracting files...")
        #Extract
        with zipfile.ZipFile(tempfile, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(__file__)+"/extract")

        print("Copying files...")
        #Copy extracted files
        distutils.dir_util.copy_tree(os.path.dirname(__file__)+"/extract", resmods)

        print("Cleaning up...")
        #Clean
        shutil.rmtree(os.path.dirname(__file__)+"/extract")
        os.remove(os.path.dirname(__file__)+"/tempdownload.zip")
    except:
        print("Error!") #Very generic

#Install mods based on the installed.txt file 
def installList(): #Install from list, currently installed.txt
    print("Starting list install...")
    with open("installed.txt", "r") as f:
        for item in f:
            print("Starting list entry " + item + ":")
            install(item)
    print("List install complete.")

#Uninstall mods based on the installed.txt file
def uninstallList(): #Uninstall from list, currently installed.txt
    print("Starting list uninstall...")
    with open("installed.txt", "r") as f:
        for item in f:
            print("Starting list entry " + item + ":")
            uninstall(item)
    print("List uninstall complete.")

#Download a mods patch file
def downloadPatch(modname): #Download a mods patch file for manual use
    print("Downloading patch file for " + modname + "...")
    #Form the mod patch url
    file = minidom.parse('modlist.xml')
    models = file.getElementsByTagName('Item')

    modurl = "NULL"
    for elem in models:
        if(elem.attributes['Name'].value == modname):
            modurl = elem.getElementsByTagName("Patch")[0].firstChild.data
    

    if(modurl == "NULL"):
        print("Failed to find mod patch url for " + modname + "!")
        return

    url = baseurl + modurl

    #Download mod
    print("Downloading .patch...")
    try:
        myfile = requests.get(url)
        open(os.path.dirname(__file__)+"/" + modname + ".patch", 'wb').write(myfile.content)
    except:
        print("Error!")
    print("Done downloading patch file for " + modname + "!")

#Check if a string starts with a mod tag
def startsWithTag(msg):
    for tag in modTags:
        if msg.startswith(modTags[tag]):
            return True
    return False

#Print the mod list based on modlist.xml
def printList(type):
    # parse an xml file by name
    file = minidom.parse('modlist.xml')

    models = file.getElementsByTagName('Item')

    # all names
    print('\nAll names:')
    if(type == ""):
        listingSkins = False
        for elem in models:
            #print(elem.attributes['Name'].value + " " + elem.getElementsByTagName("Path")[0].firstChild.data)
            name = elem.attributes['Name'].value
            if name == "ShipShell":
                listingSkins = True
            if name == "UI":
                listingSkins = False
            if(startsWithTag(name) and name != "UI"): #Mod names
                if(listingSkins):
                    print(Fore.RED + name)
                else:
                    print(Fore.LIGHTBLUE_EX + name)
            elif(listingSkins and name != "ShipShell"): #Categories, or in listing ships specific ship skin names
                print(Fore.LIGHTBLUE_EX + name)
            else:
                print(Fore.YELLOW + name)
    else:
        for elem in models:
            name = elem.attributes['Name'].value
            path = elem.getElementsByTagName("Path")[0].firstChild.data
            if(name.startswith(modTags[type]) or path.startswith(modTypes[type])):
                if(type == "shipshell"):
                    #if(elem.getElementsByTagName("Item")[0].attributes["Kind"].value == "OR"):
                        #print(name)
                    if(name.startswith("SS")):
                        print(Fore.RED + name)
                    else:
                        print(Fore.GREEN + name)
                else:  
                    print(name)
    print(Fore.WHITE)

#The main command line loop.
def cmdline(): #Recursion :)
    print("Give command:")
    cmd = input()
    #print("Running " + cmd)
    if(cmd == "install"):
        print("What mod would you like to install:")
        name = input()
        install(name)
    elif(cmd == "uninstall"):
        print("What mod would you like to uninstall:")
        name = input()
        uninstall(name)
    elif(cmd == "downloadpatch"):
        print("What mod patch file would you like to download:")
        name = input()
        downloadPatch(name)
    elif(cmd == "list" or cmd == "ls"):
        print("What type of mods to list: (all, crosshair, hudlib, shipicons, shipshell, ui, port, other)")
        type = input()
        type = type.lower()
        print("Listing...")
        if(type == "all"):
            printList("")
        else:
            printList(type)
    elif(cmd == "listinstall"):
        installList()
    elif(cmd == "listuninstall"):
        uninstallList()
    elif(cmd == "exit" or cmd == "quit"):
        print("Thank you for choosing pyStation.")
        exit()
    elif(cmd == "help" or "man"):
        print("Help:")
        print("install")
        print("uninstall")
        print("downloadpatch")
        print("list")
        print("listinstall")
        print("listuninstall")
        print("exit")
        print("help")
    else:
        print("Invalid command '" + cmd + "'.")
    cmdline()


cmdline()