#!/usr/bin/env python

import os, sys, random, Image, ImageDraw, ImageFont


"""
These three arrays are for randomly selecting a name and diagnosis.
Diags includes a list of possible diagnoses.
firstNames and lastNames are possible names to choose from.
All lists may be expanded upon, and code will continue to select any random option from the list.
"""
diags = ["Facial Damage", "Birth Defect", "Cosmetic", "Burns", "Surgical Damage"]
treats = ["Nose Reduction", "Nose Enlargement", "Liposuction", "Face Lift", "Facial Reconstruction", "Face Transplant"]
firstNames = ["Isabella", "Sophia", "Emma", "Olivia", "Ava", "Emily", "Abigail", "Madison", "Chloe", "Mia", "Sarah", "Kelly", "Rebecca", "Sam", "Christina", "Angelica"]
lastNames = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Jackson", "White", "Harris", "Martin", "Thompson"]

# UID from which doctor UIDs begin
docUID = 65536
# Number of Doctors you wish to have in the database:
numDocs = 5
# UID from which photoset UIDs begin
photosetUID = 70000
# Maximum number of Photosets per patient
numPhotosets = 5
# Minimum number of Photos in a Photoset
minPhotos = 3
# Maximum number of Photos is a Photoset
maxPhotos = 6

"""
Generate a database with (numPatients) randomly generated patients at the (databaseDir) directory - creates a Database folder at the designated directory
"""
def generateDatabase(numPatients, databaseDir):
        global photosetUID
        
        if not os.path.exists(databaseDir):
                os.makedirs(databaseDir)
        os.chdir(databaseDir)
        physicians = []
        # Generate a list of physicians using randomly generated names, and assign them UIDs (starting at 65536)
        for x in range(0, numDocs):
                physicians.append("%s, %s#%d" %(firstNames[random.randint(0, len(firstNames)-1)],lastNames[random.randint(0, len(lastNames)-1)], docUID+x))
        # Generate patient folders and all associated files, as well as a random number of photosets
        for x in range(1, numPatients+1):
                patientDir = createPatient(databaseDir, x)
                tempDiag = createDiagnosis(patientDir)
                tempTreat = createTreatment(patientDir)
                tempNote = createNotes(patientDir)
                tempPhys = createPhysicians(patientDir, physicians[random.randint(0, len(physicians)-1)])
                for x in range(1, random.randint(1, numPhotosets)):
                        createPhotoset(patientDir, photosetUID, random.randint(minPhotos, maxPhotos), tempDiag, tempTreat, tempNote, tempPhys)
                        photosetUID += 1
                        os.chdir("..")
                os.chdir("..")

"""
Generate the Patient's Folder at the given database directory, with the given UID.
Generates a random name from the list of first and last names.
Generates the name.txt file in this folder, returns the patient's folder directory.
"""
def createPatient(databaseDir, UID):
        myFirstName = '%s' %firstNames[random.randint(0, len(firstNames)-1)]
        myLastName = '%s' %lastNames[random.randint(0, len(lastNames)-1)]
        dirname = '%s, %s#%d' %(myLastName, myFirstName, UID)
        try:
                os.makedirs(dirname)
        except OSError:
                pass
        os.chdir(dirname)
        filename = "name.txt"
        File = open(filename,"w")
        File.writelines("%s, %s#%d" %(myFirstName, myLastName, UID))
        return dirname

"""
Generates a diagnoses.txt file in the patient's directory, selecting a random diagnosis for the patient
from the list of diagnoses
"""
def createDiagnosis(dirname):
        filename = "diagnoses.txt"
        File = open(filename,"w")
        thisDiag = str(random.choice(diags)) + "\n"
        if (random.randint(0, 5) == 3):
                thisDiag += random.choice(diags) + "\n"
        File.writelines(thisDiag)
        return thisDiag

"""
Generates a treatment.txt file in the patient's directory, selecting the same treatment as the diagnosis this patient has
"""
def createTreatment(dirname):
        filename = "treatments.txt"
        File = open(filename,"w")
        thisTreat = str(random.choice(treats)) + "\n"
        if (random.randint(0, 5) == 3):
                thisTreat += random.choice(treats) + "\n"
        File.writelines(thisTreat)
        return thisTreat

"""
Generates a notes.txt file in the patient's directory, writing string into the file
"""
def createNotes(dirname):
        filename = "notes.txt"
        File = open(filename,"w")
        randomNotes = "This is some random gibberish for notes.  Muahahaha."
        File.writelines(randomNotes)
        return randomNotes

"""
Generates a physicians.txt file in the patient's directory
Writes the doctors' name in that file
"""
def createPhysicians(dirname, docName):
        filename = "physicians.txt"
        File = open(filename,"w")
        File.writelines(docName)
        return docName

"""
Generates a folder to contain the patients' photos sets
Selects a random date for the photoset (in the year 2012)
Generates all necessary .txt files (and writes the relevant info to the files
Generates the given number of .jpg pictures in the photoset folder
All .jpg files are empty (and thus cannot be displayed), but do exist
"""
def createPhotoset(dirname, UID, numPics, myDiagnosis, myTreatment, myNotes, myDoc):
        # dd-mm-yyyy : day and month generated randomly (1-29 and 1-12 respectively).  Year is 2012 always
        photosetDir = "%02d-%02d-2012#%d" %(random.randint(1, 29), random.randint(1, 12), UID)
        try:
                os.makedirs(photosetDir)
        except OSError:
                pass
        os.chdir(photosetDir)
        physFile = "physicians.txt"
        noteFile = "notes.txt"
        treatFile = "treatments.txt"
        diagFile = "diagnoses.txt"
        File = open(physFile,"w")
        File.writelines(myDoc)
        File = open(noteFile,"w")
        File.writelines(myNotes)
        File = open(treatFile,"w")
        File.writelines(myTreatment)
        File = open(diagFile,"w")
        File.writelines(myDiagnosis)
        for x in range(0, numPics):
                imgFile = "DSC%05d.png" %x
#                File = open(imgFile, "w")
        i = Image.new("RGB", (250,250))
        d = ImageDraw.Draw(i)
        f = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 18)
        d.text((0,0), dirname + imgFile, font=f)
        i.save(open(imgFile, "wb"), "PNG")
                

if __name__ == '__main__':
    generateDatabase(100, "../patients")
