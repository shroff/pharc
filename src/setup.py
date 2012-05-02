import sys
from distutils.core import setup

if 'py2exe' in sys.argv:
    import py2exe

    kwargs = dict(windows=[{'script':'pharc.py', 'dest_base': 'gui'}],
                  options={'py2exe': dict(includes=["sip"], optimize=2, compressed=1)})

else:
    kwargs = dict(windows=['pharc.py'])

setup(name = 'PHARC',
      version = '1.0',
      packages=['cli', 'database', 'export', 'gui', 'logic'],
      package_data={'cli': ['cli/*'], 'gui': ['gui/*'], 'logic': ['logic/*'], 'database': ['database/*'], 'export': ['export/*']},
      **kwargs)
