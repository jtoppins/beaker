
import os
import webassets
from webassets.filter.jst import JST
import threading
from turbogears import config

# Custom filter to use external ycssmin
# (There is a python cssmin implementation, we could use that instead)
from webassets.filter import ExternalTool
class YCSSMin(ExternalTool):
    name = 'ycssmin'
    def input(self, in_, out, source_path, **kwargs):
        self.subprocess(['cssmin'], out, in_)


# Environment is lazily initialised because it requires config to be loaded
_env = None
_env_lock = threading.Lock()

def _create_env():
    directory = config.get('basepath.assets',
            # default location is at the base of our source tree
            os.path.join(os.path.dirname(__file__), '..', '..', 'assets'))
    debug = config.get('assets.debug')
    auto_build = config.get('assets.auto_build')
    env = webassets.Environment(directory=directory, url='/assets',
            manifest='file', debug=debug, auto_build=auto_build)
    env.register('css',
            'style.less',
            filters=['less', 'cssrewrite', YCSSMin()],
            output='generated/beaker-%(version)s.css',
            depends=['*.less', 'bootstrap/less/*.less'])
    env.register('js',
            # third-party
            'bootstrap/js/bootstrap-transition.js',
            'bootstrap/js/bootstrap-modal.js',
            'bootstrap/js/bootstrap-dropdown.js',
            'bootstrap/js/bootstrap-tab.js',
            'bootstrap/js/bootstrap-alert.js',
            'bootstrap/js/bootstrap-button.js',
            'bootstrap/js/bootstrap-collapse.js',
            'typeahead.js/dist/typeahead.js',
            'jquery.cookie.js',
            'underscore-1.5.1.js',
            'backbone-1.0.0.js',
            # ours
            webassets.Bundle(
                'jst/*/*.html',
                'jst/*.html',
                filters=[JST(template_function='_.template')],
                output='generated/beaker-jst-%(version)s.js'),
            'local-datetime.js',
            'link-tabs-to-anchor.js',
            'beaker-typeaheads.js',
            'recipe-tasks.js',
            'access-policy.js',
            filters=['uglifyjs'],
            output='generated/beaker-%(version)s.js')
    return env

def get_assets_env():
    global _env
    if _env is None:
        with _env_lock:
            if _env is None:
                _env = _create_env()
    return _env