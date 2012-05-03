# pharc v0.5

PHARC is a photo archiving system designed to organize physicians'
photos. It allows users to import photos, collect them into photosets
tagged by diagnoses and treatments, and view, export, and edit the
photos in a structured manner.

This file describes pharc and how to get it to run. At this stage no
configuration is necessary beyond the original installation.

This program was originally written in for a senior design course at
the Georgia Institute of Technology.

### About

* Authors:      Check the copyright notices in each source file
* License:      GNU General Public License Version 2

* Website:      http://github.com/shroff/pharc
* Download:     https://github.com/shroff/pharc/downloads
* Bug reports:  https://github.com/shroff/pharc/issues
* git clone:    https://saulrh@github.com/shroff/pharc.git

### Design Goals

* Intuitive and cross-platform photo manager designed for physicians
* All data is human-readable and human-writable; no opaque databases
* Easily maintainable so it can be continued for future senior design
  projects

### Features

* Maintains all information in flat text files and human-readable
  directories
* Export to opendocument presentation (openable by MS Office) and as
  email attachments.
* Scales to 10000+ patients, though initial loading is slow.
* Mass photo import by dumping photos into an import directory

### Dependencies

* Python (tested with versions 2.7 and 3.2)
* Qt4 and PyQt4
* odfpy
* dnspython
* PIL (for developers)

## Installation

### Windows and OSX users

Go to the downloads tab (https://github.com/shroff/pharc/downloads)
and select the appropriate zip file. These zip files comes with all of
the required dependencies packaged together. Extract the contents into
the location of your choice, locate the .exe or .app, and run the
program.

## Windows and OSX developers

## Linux users and developers

You can use your package manager to install Python and PyQt4 if they
aren't already installed. odfpy and dnspython are in PyPI and can be
installed using PIP; if you want to install them for Python3 instead
use pip to install odfpy3 and dnspython3. Also note that the Ubuntu
repositories do not include PyQt4 packages for Python3.

If you need to create a test database, you will also need the Python
Imaging Library. Keep in mind that at the current time (April 2012)
PIL does not work with python3.


## Using the software

### Getting started

When you run the program, it will spend some time loading the database
and then present you with a main window showing a list of all
patients. Currently, each item shows a random photo from the most
recently taken set of photos and the patient's name, treatment tags,
and diagnosis tags. You can sort each column alphabetically by
clicking the column header, and you can use the keyboard to move to
patients by typing the start of their names.

### Importing

If there is a directory named "import", any images
in this directory will be loaded for importing and can be accessed by
going file->check for imports.

### Searching

Simply start typing in the search bar. More advanced searches don't
work and spaces make things break, but you can find people by their
name or their treatment or diagnosis tags.

### More details

If you double-click on a patient's entry, you will get a window that
shows patient details. In this view you will find a list of photosets,
each line displaying the photoset's date and the treatment and
diagnosis tags associated with each photoset. A patient's treatment
and diagnosis tags are just all of their photosets' tags put
together. Clicking on an item will bring up a photos area that
displays all of the photos in that photoset.

Double-clicking on a treatment or diagnosis entry will allow you to
edit it; each tag is a sequence of letters and different tags are
separated by commas. For example, "foo, bar" is two tags, "foo" and
"bar". You can change a patient's name using the indicated button in
the upper-right. Typos aren't a problem anywhere; no changes will be
made to disk until and unless the "save changes" button in the
lower-right is pressed.

### The Selection

You'll see a checkbox under each photo in the details window. This is
the Selection, a program-wide list of selected photos that persists
until cleared or the program is closed. After selecting the photos you
want to work with from as many or as few patients as you want, go to
the "selection" menu item at the top and choose your action.

"View" will open a window where you can see large versions of each
photo. You can cycle through all selected photos using the buttons at
the right, and clicking the "open in external viewer" button will open
that photo in your operating system's default photo viewer so that you
can edit it.

The "export" options will export your selected photos to various
formats. For example, the "presentation" option will create an
opendocument presentation file with the photos in it and open it in
your preferred presentation software for you to save in a more
suitable location. The "email" option will ask you for an email
address; put yours in and it will send you an email with your selected
photos attached (check your junk mail folder). Check the lower-left
corner of the program for status information during lengthy
exports.

Unfortunately, neither option currently works on windows.

### Importing Photos

Simply drop all your photos into the "import" directory in pharc's
main directory (the one with the program in it). Open pharc and select
file->check for imports. This will open a window where you can create
patients and photosets and import photos into the organized
system. The list of patients behaves exactly like the list in the main
window, and the list of photosets behaves exactly like the list in the
details window. Hit the checkboxes under your photos, select a patient
and a photoset, and hit "add to photoset". The photos and have been
moved into the "patients" directory and will disappear from both the
import list and the import directory.

## Known Problems

Many. This is alpha-quality software. The big ones:

* The application only searches for photos to import on program
  startup.
* Does not currently display or allow editing of patient notes.
* Searching does not break queries into individual words.
* Many updates are not reflected elsewhere in the program unless the
  program is closed and restarted.
* The "add" and "do this later" buttons in the import window are
  improperly labeled. "Add" does nothing; changes are committed on
  hitting "add to photoset". Hit "do this later" to go back to the
  main window.
