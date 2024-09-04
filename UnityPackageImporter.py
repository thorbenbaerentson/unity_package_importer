import bpy
import toml
import tarfile
import os
import tarfile
import shutil

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from pathlib import Path

# Import local package
import sys
packages_path = "c:\\users\\dirk\\appdata\\roaming\\python\\python311\\site-packages"
sys.path.insert(0, packages_path)
import yaml

class AssetDescriptor:    
    def __init__(self, guid, asset_extension, relative_path):
        self.guid = guid
        self.asset_extension = asset_extension
        self.relative_path = relative_path

class UnityPackageImporter(Operator, ImportHelper):
    """Allows to import unity package files directly into blender"""
    bl_idname = "import.unity_package_importer"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Unity Importer (.unitypackage)"

    # ImportHelper mix-in class uses this.
    filename_ext = ".unitypackage"

    tmp_directory : StringProperty(
        default = 'C:\\tmp\\',
        description = 'Temporary path to extract the package to.',
        subtype = 'DIR_PATH'
    )
    
    target_directory : StringProperty(
        default = 'C:\\tmp\\',
        description = 'Path to copy unpacked assets to.',
        subtype = 'DIR_PATH'
    )
    
    import_textures : BoolProperty(
        name = "Import textures",
        default = True,
        description = 'Import textures?'
    )
    
    import_materials : BoolProperty(
        name = "Import materials",
        default = True,
        description = 'Import materials?'
    )
    
    import_prefabs : BoolProperty(
        name = "Import prefabs",
        default = True,
        description = 'Import prefabs?'
    )
    
    import_scenes : BoolProperty(
        name = "Import scenes",
        default = True,
        description = 'Import scenes?'
    )
    
    # Returns the file name without the file extension. This will be used as subdirectory
    # inside the tmp directory.
    def get_project_name(self):
        return os.path.basename(self.filepath).replace(self.filename_ext, "")
    
    # Returns the path that is used to extract the package to.
    def get_absolute_tmp_dir(self):
        return os.path.join(self.tmp_directory, self.get_project_name())
    
    # Creates the tmp directory. That means the directory will be created if it does not exists.
    # If it exists, the directory will be removed and then recreated.
    def prepare_tmp_directory(self):
        path = Path(self.get_absolute_tmp_dir())
        dir = self.get_absolute_tmp_dir()
        if path.is_dir():
            try:
                files = os.listdir(dir)
                for file in files:
                    file_path = os.path.join(dir, file)
                
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                
                path.rmdir()

            except OSError:
               print("Error occurred while deleting files.")
               return False
               
        path.mkdir(parents = True, exist_ok = True)
        return True
    
    # Extracts the package to the tmp directory
    def extract_package(self):
        path = self.get_absolute_tmp_dir()
        try:
            tar = tarfile.open(self.filepath)
            for file in tar:
                try:
                    tar.extract(file, path = path)
                except IOError: 
                    os.remove(file.name)
                    tar.extract(file, path = path)
                finally:
                    os.chmod(os.path.join(path, file.name), file.mode)
                    
            tar.close()

        except IOError as e:
            print("Error occurred while unpacking files.")
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

            return False
       
        return True
    
    # Returns the content of the pathname file inside an
    # asset directory. 
    def get_pathname_content(self, asset_directory):
        pathname_file = os.path.join(asset_directory, "pathname")
        data = ""
        with open(pathname_file, 'r') as file:
            data = file.read()
            
        return data.replace("Assets/", "")
    
    # Helper to copy over files.
    # Creates the entire path to the target if it does not exist.
    def copy_file(self, source, target):        
        print("Coping file: " + source + " -> " + target)
        if os.path.exists(target):
            os.remove(target)

        os.makedirs(os.path.dirname(target), exist_ok = True)
        shutil.copyfile(source, target)

    # Returns true, if the given meta file contains
    # the folderAsset entry and this entry is true, False otherwise
    def is_folder_asset(self, abs_path_to_meta):
        print("Parsing: " + abs_path_to_meta)
        data = ""
        with open(abs_path_to_meta, 'r') as f:
            meta_data = yaml.safe_load(f)
            if 'folderAsset' in meta_data:
                return meta_data['folderAsset']

        return False 
    
    # Copies all assets from the tmp directory to its original location.
    def copy_files(self):
        path = self.get_absolute_tmp_dir()
        try:
            for f in os.listdir(path):
                uuid = f
                asset_dir = os.path.join(path, f)
                asset_file = os.path.join(asset_dir, "asset")
                meta_file = os.path.join(asset_dir, "asset.meta")
                
                # If a path points to a file, then it is not an asset directory.
                if os.path.isfile(asset_dir):
                    continue

                asset_target_path = os.path.join(self.target_directory, self.get_pathname_content(asset_dir))
                meta_target_path = asset_target_path + ".meta"
                if self.is_folder_asset(meta_file):
                    print(f + " is a directory.")
                    continue
                
                self.copy_file(asset_file, asset_target_path)                
                self.copy_file(meta_file, meta_target_path)
                
        except OSError as e:
            print("Error occurred while coping files.")
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
           
            return False
       
        return True

    def execute(self, context):        
        print("Extracting package to '" + self.get_absolute_tmp_dir() + "'")
        
        if not self.extract_package():
            print("Stop - Could not unpack unity package.")
            return
        
        if not self.copy_files():
            print("Stop - Could not copy files.")
            return
        
        return { 'FINISHED' }


# Only needed if you want to add into a dynamic menu.
def menu_func_import(self, context):
    self.layout.operator(UnityPackageImporter.bl_idname, text = UnityPackageImporter.bl_label)


# Register and add to the "file selector" menu (required to use F3 search "Text Import Operator" for quick access).
def register():
    bpy.utils.register_class(UnityPackageImporter)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(UnityPackageImporter)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
