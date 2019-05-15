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

meeting_presence = Resource(voteit_irl_lib, 'meeting_presence.js', depends = (watcher_js, common_js))
meeting_presence_moderator = Resource(voteit_irl_lib, 'meeting_presence_moderator.js', depends = (watcher_js, common_js, pure_js))
voteit_irl_print_css = Resource(voteit_irl_lib, 'print.css', depends = (voteit_main_css,))
main_proposal = Resource(voteit_irl_lib, 'main_proposal.js', depends=(common_js,))


# Every resource needs (path, file_ending, depends)
def dynamic_generator(library, *resources):
    for (path, extension, depends) in resources:
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(voteit_irl_lib.path, path)):
            for fn in filenames:
                if fn.endswith(extension):
                    yield Resource(library, os.path.join(path, fn), depends=depends)


# dynamic_resources = dynamic_generator(
#     voteit_irl_lib,
#     ('vue/js', '.js', None),
#     ('vue/css', '.css', None)
# )
# voteit_irl_projector = Group(dynamic_resources)

voteit_irl_projector_vendor_js = Resource(voteit_irl_lib, 'vue/js/vendor_chunks.js')
voteit_irl_projector_vendor_css = Resource(voteit_irl_lib, 'vue/css/vendor_chunks.css')
voteit_irl_projector = Group((
    Resource(voteit_irl_lib, 'vue/js/bundle.js', depends=(voteit_irl_projector_vendor_js,)),
    Resource(voteit_irl_lib, 'vue/css/bundle.css', depends=(voteit_irl_projector_vendor_css,)),
))


def always_needed(view, event):
    meeting_presence.need()
    main_proposal.need()


def includeme(config):
    config.add_subscriber(always_needed, [IBaseView, IViewInitializedEvent])
