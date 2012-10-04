""" Fanstatic lib"""
from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource

from voteit.core.fanstaticlib import voteit_common_js
from voteit.core.fanstaticlib import voteit_main_css
from voteit.core.fanstaticlib import qtip


voteit_irl_lib = Library('voteit_irl', 'static')

voteit_irl_projector_js = Resource(voteit_irl_lib, 'voteit_irl_projector.js', depends=(voteit_common_js, qtip))
voteit_irl_projector_css = Resource(voteit_irl_lib, 'voteit_irl_projector.css', depends=(voteit_main_css,))

voteit_irl_projector = Group((voteit_irl_projector_js, voteit_irl_projector_css))
