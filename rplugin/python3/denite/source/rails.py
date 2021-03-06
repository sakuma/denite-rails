# -*- coding: utf-8 -*-

from denite import util
from .base import Base

import os
import site

# Add external modules
path_to_parent_dir = os.path.abspath(os.path.dirname(__file__) + '/../')
path_to_modules = os.path.join(path_to_parent_dir, 'modules')
site.addsitedir(path_to_modules)
site.addsitedir(os.path.join(path_to_modules, 'inflection'))
site.addsitedir(os.path.join(path_to_modules, 'finders'))
site.addsitedir(os.path.join(path_to_modules, 'models'))

from dwim_finder import DwimFinder # noqa
from all_finder import AllFinder # noqa
from app_finder import AppFinder # noqa
from model_finder import ModelFinder # noqa
from controller_finder import ControllerFinder # noqa
from helper_finder import HelperFinder # noqa
from view_finder import ViewFinder # noqa
from frontend_finder import FrontendFinder # noqa
from test_finder import TestFinder # noqa
from spec_finder import SpecFinder # noqa
from config_finder import ConfigFinder # noqa
from db_finder import DbFinder # noqa
from lib_finder import LibFinder # noqa
from assets_finder import AssetsFinder # noqa


class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'rails'
        self.kind = 'file'

    def on_init(self, context):
        try:
            context['__target'] = context['args'][0]
        except IndexError:
            raise NameError('target must be provided')

        cbname = self.vim.current.buffer.name
        context['__cbname'] = cbname
        context['__root_path'] = util.path2project(self.vim, cbname, context.get('root_markers', ''))

    def highlight(self):
        # TODO syntax does not work as expected
        self.vim.command('syntax region deniteSource_railsConstant start=+^+ end=+^.\{-}\s+')
        self.vim.command('highlight link deniteSource_railsConstant Statement')
        self.vim.command('syntax match deniteSource_railsSeparator /::/ containedin=deniteSource_railsConstant')
        self.vim.command('highlight link deniteSource_railsSeparator Identifier')
        self.vim.command('syntax region deniteSource_railsPath start=+(+ end=+)+')
        self.vim.command('highlight link deniteSource_railsPath Statement')
        self.vim.command('syntax match deniteSource_railsController /Controller:/')
        self.vim.command('highlight link deniteSource_railsController Function')
        self.vim.command('syntax match deniteSource_railsModel /Model:/')
        self.vim.command('highlight link deniteSource_railsModel String')
        self.vim.command('syntax match deniteSource_railsHelper /Helper:/')
        self.vim.command('highlight link deniteSource_railsHelper Type')
        self.vim.command('syntax match deniteSource_railsView /View:/')
        self.vim.command('highlight link deniteSource_railsView Statement')
        self.vim.command('syntax match deniteSource_railsTest /Test:/')
        self.vim.command('highlight link deniteSource_railsTest Number')
        self.vim.command('syntax match deniteSource_railsSpec /Spec:/')
        self.vim.command('highlight link deniteSource_railsSpec Number')
        self.vim.command('syntax match deniteSource_railsConfig /Config:/')
        self.vim.command('highlight link deniteSource_railsConfig Statement')
        self.vim.command('syntax match deniteSource_railsDb /Db:/')
        self.vim.command('highlight link deniteSource_railsDb Statement')
        self.vim.command('syntax match deniteSource_railsLib /Lib:/')
        self.vim.command('highlight link deniteSource_railsLib Statement')
        self.vim.command('syntax match deniteSource_railsAssets /Assets:/')
        self.vim.command('highlight link deniteSource_railsAssets Statement')
        self.vim.command('syntax match deniteSource_railsApp /App:/')
        self.vim.command('highlight link deniteSource_railsApp Statement')
        self.vim.command('syntax match deniteSource_railsAll /All:/')
        self.vim.command('highlight link deniteSource_railsAll Statement')
        self.vim.command('syntax match deniteSource_railsFrontend /Frontend:/')
        self.vim.command('highlight link deniteSource_railsFrontend Statement')

    def gather_candidates(self, context):
        file_list = self._find_files(context)
        if file_list is not None:
            return [self._convert(context, x) for x in file_list]
        else:
            return []

    def _find_files(self, context):
        target = context['__target']

        if target == 'dwim':
            finder_class = DwimFinder
        elif target == 'app':
            finder_class = AppFinder
        elif target == 'all':
            finder_class = AllFinder
        elif target == 'model':
            finder_class = ModelFinder
        elif target == 'controller':
            finder_class = ControllerFinder
        elif target == 'helper':
            finder_class = HelperFinder
        elif target == 'view':
            finder_class = ViewFinder
        elif target == 'frontend':
            finder_class = FrontendFinder
        elif target == 'test':
            finder_class = TestFinder
        elif target == 'spec':
            finder_class = SpecFinder
        elif target == 'config':
            finder_class = ConfigFinder
        elif target == 'db':
            finder_class = DbFinder
        elif target == 'lib':
            finder_class = LibFinder
        elif target == 'assets':
            finder_class = AssetsFinder
        else:
            msg = '{0} is not valid denite-rails target'.format(target)
            raise NameError(msg)

        return finder_class(context).find_files()

    def _convert(self, context, file_object):
        result_dict = {
            'word': file_object.to_word(context['__root_path']),
            'action__path': file_object.filepath
        }

        return result_dict
