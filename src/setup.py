import sys
from distutils.core import setup

#Modify this to be your own directory - or find a way to fetch the path to it
PyQt4imageformatDir = 'A:/Program Files/Python2/Lib/site-packages/PyQt4/plugins/imageformats/'

if 'py2exe' in sys.argv:
    import py2exe

    kwargs = dict(console=[{'script':'pharc.py', 'dest_base': 'gui'}],
                  options={'py2exe': dict(includes=["sip"], optimize=2, compressed=1)},
                  data_files=[('imageformats', [
                      PyQt4imageformatDir + 'qgif4.dll',
                      PyQt4imageformatDir + 'qjpeg4.dll',
                      PyQt4imageformatDir + 'qtga4.dll',
                      PyQt4imageformatDir + 'qtiff4.dll',
                      PyQt4imageformatDir + 'qico4.dll',
                      PyQt4imageformatDir + 'qmng4.dll',
                      PyQt4imageformatDir + 'qsvg4.dll'])])

else:
    kwargs = dict(windows=['pharc.py'])

setup(name = 'PHARC',
      version = '1.0',
      packages=['cli', 'database', 'export', 'gui', 'logic'],
      package_data={'cli': ['cli/*'], 'gui': ['gui/*'], 'logic': ['logic/*'], 'database': ['database/*'], 'export': ['export/*']},
      **kwargs)
