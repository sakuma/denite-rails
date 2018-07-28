import os
import finder_utils
from assets_file import AssetsFile


class AssetsFinder:
    GLOB_PATTERN = 'app/assets/**/*'

    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def find_files(self):
        files = finder_utils.glob_project(self.root_path, self.GLOB_PATTERN)
        files = [filename for filename in files if os.path.isfile(filename)]
        return [AssetsFile(filename) for filename in files]
