# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from os.path import normpath, join, abspath, basename, dirname

def resolve(fro, to):
    return normpath(join(fro, to))