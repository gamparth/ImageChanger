from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('ImageChanger.py', base=base, targetName = 'Imagecgan')
]

setup(name='ImageChanger.py',
      version = '1.0',
      description = 'Application for basic Image Manipulation',
      options = dict(build_exe = buildOptions),
      executables = executables)
