""" Fanstatic lib"""
import os

from arche.fanstatic_lib import common_js
from arche.fanstatic_lib import pure_js
from arche.interfaces import IBaseView
from arche.interfaces import IViewInitializedEvent
from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from voteit.core.fanstaticlib import voteit_main_css
from voteit.core.fanstaticlib import watcher_js


voteit_irl_lib = Library('voteit_irl', 'static')

# voteit_irl_projector_js = Resource(voteit_irl_lib, 'voteit_irl_projector.js', depends = (common_js, pure_js))
# voteit_irl_projector_css = Resource(voteit_irl_lib, 'voteit_irl_projector.css', depends = (voteit_main_css,))
# voteit_irl_projector = Group((voteit_irl_projector_js, voteit_irl_projector_css))
meeting_presence = Resource(voteit_irl_lib, 'meeting_presence.js', depends = (watcher_js, common_js))
meeting_presence_moderator = Resource(voteit_irl_lib, 'meeting_presence_moderator.js', depends = (watcher_js, common_js, pure_js))
voteit_irl_print_css = Resource(voteit_irl_lib, 'print.css', depends = (voteit_main_css,))
main_proposal = Resource(voteit_irl_lib, 'main_proposal.js', depends=(common_js,))


def dynamic_generator(*resources):
    for (path, extension, depends) in resources:
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(voteit_irl_lib.path, path)):
            for fn in filenames:
                if fn.endswith(extension):
                    yield Resource(voteit_irl_lib, os.path.join(path, fn), depends=depends)


dynamic_resources = dynamic_generator(
    ('vue/js', '.js', (common_js,)),
    ('vue/css', '.css', (voteit_main_css,))
)
voteit_irl_projector = Group(dynamic_resources)


def always_needed(view, event):
    meeting_presence.need()
    main_proposal.need()


def includeme(config):
    config.add_subscriber(always_needed, [IBaseView, IViewInitializedEvent])
