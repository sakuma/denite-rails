import os
import finder_utils
from config_file import ConfigFile


class ConfigFinder:
    GLOB_PATTERN = 'config/**/*'

    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def find_files(self):
        files = finder_utils.glob_project(self.root_path, self.GLOB_PATTERN)
        files = [filename for filename in files if os.path.isfile(filename)]
        return [ConfigFile(filename) for filename in files]
