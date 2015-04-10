""" Fanstatic lib"""
from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from arche.fanstatic_lib import common_js
from voteit.core.fanstaticlib import data_loader
from voteit.core.fanstaticlib import voteit_main_css
#from voteit.core.fanstaticlib import watcher_js
from arche.fanstatic_lib import pure_js


#from voteit.core.fanstaticlib import voteit_common_js
#from voteit.core.fanstaticlib import voteit_main_css


voteit_irl_lib = Library('voteit_irl', 'static')

#FIXME

voteit_irl_projector_js = Resource(voteit_irl_lib, 'voteit_irl_projector.js', depends = (common_js, pure_js))
voteit_irl_projector_css = Resource(voteit_irl_lib, 'voteit_irl_projector.css', depends = (voteit_main_css,))
voteit_irl_set_as_present = Resource(voteit_irl_lib, 'voteit_irl_set_as_present.js', depends = (common_js, data_loader,))
voteit_irl_projector = Group((voteit_irl_projector_js, voteit_irl_projector_css))
