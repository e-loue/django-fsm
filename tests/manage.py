#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
REQUIREMENTS = os.path.join(PROJECT_ROOT, 'tests', 'requirements.pip')

sys.path.insert(0, PROJECT_ROOT)

from django.core.management import execute_manager
try:
    import tests.settings
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv += ['test']
    execute_manager(tests.settings)
