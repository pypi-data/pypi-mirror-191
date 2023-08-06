import dash_extensions
from dash_extensions import Keyboard as kb

dash_ex_urls = {
    "dash_extensions.min.js": "https://sicsapps.com/dmp/scripts/dash_extensions.min.js",
    "dash_extensions.min.js.map": "https://sicsapps.com/dmp/scripts/dash_extensions.min.js.map"
}

for k, v in dash_ex_urls.items():
    for i in range(len(dash_extensions._js_dist)):
        if k in dash_extensions._js_dist[i]['relative_package_path']:
            dash_extensions._js_dist[i].update({"relative_package_path": k, "external_url": v})

class Keyboard(kb):
    def __init__(self,*args,**kwargs):
        kb.__init__(self, *args, **kwargs)
