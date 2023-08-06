import asyncclick as ac
from .. import click_backend as cb
from ...exceptions import *


cs = {"help_option_names": ["-h", "--help"]}


@ac.group(cls=cb.XenaGroup)
def xoa_utils():
    pass
