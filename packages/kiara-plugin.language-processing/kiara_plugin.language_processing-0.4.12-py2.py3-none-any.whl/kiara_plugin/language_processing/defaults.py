# -*- coding: utf-8 -*-
import os

from appdirs import AppDirs

#  Copyright (c) 2021, University of Luxembourg / DHARPA project
#  Copyright (c) 2021, Markus Binsteiner
#
#  Mozilla Public License, version 2.0 (see LICENSE or https://www.mozilla.org/en-US/MPL/2.0/)


kiara_app_dirs = AppDirs("kiara_plugin.language_processing", "DHARPA")

NLTK_DOWNLOAD_DIR = os.path.join(kiara_app_dirs.user_data_dir, "nltk_data")
