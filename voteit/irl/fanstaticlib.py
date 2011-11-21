""" Fanstatic lib"""
from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource

from voteit.core.fanstaticlib import voteit_common_js
from voteit.core.fanstaticlib import voteit_main_css
from voteit.core.fanstaticlib import qtip


voteit_irl_lib = Library('voteit_irl', '')

voteit_irl_js = Resource(voteit_irl_lib, 'voteit_irl.js', depends=(voteit_common_js, qtip))
voteit_irl_css = Resource(voteit_irl_lib, 'voteit_irl.css', depends=(voteit_main_css,))

voteit_irl = Group((voteit_irl_js, voteit_irl_css))
