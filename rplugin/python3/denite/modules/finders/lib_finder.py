import os
import finder_utils
from lib_file import LibFile


class LibFinder:
    GLOB_PATTERN = 'lib/**/*'

    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def find_files(self):
        files = finder_utils.glob_project(self.root_path, self.GLOB_PATTERN)
        files = [filename for filename in files if os.path.isfile(filename)]
        return [LibFile(filename) for filename in files]
