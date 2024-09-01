# Table of Contents
- [Introduction](#blender-extension-template)
- [Usage](#usage)
- [Tips](#tips)
    - [Development extras](#development-extras)
    - [Searching for UI-Elements](#searching-for-ui-Elements)
    - [Using python packages](#using-python-packages)
    - [Use Visual Studio Code](#use-visual-studio-code)

# Blender Extension Template
This template is intended to help speed up blender extension development with python. The template is itself a working operator, that demonstrates how to:
- implement an extension
- interact with Blender UI
- divide code into separate modules and utilize them

'__init__.py' contains further information on the topics above.

# Usage
Place your code in separate files. Best pratice is to put operators, menus, views etc. everything that needs a register and unregister function into its own file and let '__init__.py' initialize the modules by adding the module to the 'modulesNames' array inside '__init__.py'.

Usually you can remove the lines:
```python
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)
```
These lines add your extension folder to the path. This is necessary if you´re using source files in your project, that are not registered with Blender. In order for Blender to find these files thy need to be on the path.

# Tips
## Development extras
If you start out with add-on development make sure to enable 'Python Tooltips' and 'Development Extras' under:

*Edit -> Preferences -> Interface*.

With that functionality enabled you can right click on a menu item and review its code. This is helpful, if you want to integrate your operators with the existing blender UI. As it is done in *OBJECT_MT_ExampleMenu.py*. The name of the menu 'VIEW3D_MT_object_asset' was found by inspecting the source code of the corresponding menu script. 

## Searching for UI-Elements
Make sure 'Development Extras' and 'Python Tooltips' are enabled (refer to [Development extras](#development-extras)). Next, navigate to the 'Scripting' tTab and right-click on the menu item you wish to investigate. This will open the UI-Script for the selected UI element in the scripting editor. You can then search for it using Ctrl + F. The display name of the menu or sub-menu item is encoded in the menu class under the 'bl_label' field, for example:
```python
bl_label = "Align View to Active"
```

## Using python packages
It is possible (although, not very convenient) to use pip packages with the python installation that comes with blender. Pip is by default part of the bundled python installation. 

### Installing a package
In order to install a package locate your Blender installation. Under Windows this is 
```
C:\Program Files\Blender Foundation\Blender {blender_version}\
```
by default. 
Inside your Blender folder should be a folder called 'python' and inside that folder a another one called 'bin'. This is where the bundled python interpreter is located. Open a terminal, cd into that folder and than run a regular pip install command from that folder:
```
python -m pip install atudomain-git --user
```
Replace 'atudomain-git' with the name of the package you want to install. Pip should download the package and its dependencies and return with a message indicating success. In Winwdows it should look like this:
![successfully installation](https://github.com/thorbenbaerentson/blender_extension_template/blob/main/images/install_package.png "Successfull installation")

### Locate the package on disk
In order to use the newly installed package we must tell python where to look for that package. To find out where the package was installed we can use the command pip show <package>.
```
python -m pip show atudomain-git
```
Again replace atudomain-git with the name of the package you want to install. This command returns some information about the package. Among these information is value called 'Location'. This is the path where pip installed the package to. 
![show package](https://github.com/thorbenbaerentson/blender_extension_template/blob/main/images/show_package.png "Show package")

### Importing the package
Using the loacation obtained using the 'show'-Command we can tell python where to look for the newly installed package. 
```python
# Add the path to sys.path, so the interpreter finds the package.
import sys
packages_path = "c:\\users\\{user}}\\appdata\\roaming\\python\\python311\\site-packages"
sys.path.insert(0, packages_path)
# Then import the module
from atudomain.git import Git
```
Now we can use the package in our code.

## Use Visual Studio Code
If you are serious about developing extensions for Blender consider using Visual Studio Code with [Blender Development Extension](https://github.com/JacquesLucke/blender_vscode). This allows you to use the python debugger while running a Blender instance and testing your extension.The extension will install the python debugger for Blender once you start Blender from inside Visual Studio Code. In order for this install to succeed you might have to run Visual Studio Code as an administrator. After the debugger has been installed successfully VS Code can be run with normal privileges.
