#!/usr/bin/python
import os
from pathlib import Path

usuario="Elena"
app = os.getcwd()
print ("Current working directory %s" % app)
app_path=Path(app)
public_html_path=Path(app_path.parent)
print(public_html_path)

path_user=os.path.join(public_html_path, usuario)
print(path_user)

