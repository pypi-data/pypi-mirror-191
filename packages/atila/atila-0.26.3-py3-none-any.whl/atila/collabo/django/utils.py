import sys, os
from rs4 import pathtool

BACKEND_DIR = 'backend'
APPS_DIR = 'orm'

MODEL_INIT = """import sys, os
from rs4 import pathtool

def __config__ (pref):
    import skitai
    import settings

    pathtool.mkdir (settings.STATIC_ROOT)
    skitai.mount (settings.STATIC_URL, settings.STATIC_ROOT)
    skitai.log_off (settings.STATIC_URL)
    pref.config.SETTINGS = settings
"""

APP_INIT = """import os
import sys
import atila
import skitai

BASE_DIR = os.path.dirname (__file__)

def __config__ (pref):
    sys.path.insert (0, os.path.join (BASE_DIR, 'models'))
    skitai.mount ("/", os.path.join (BASE_DIR, 'models/wsgi:application'), pref, name = 'models')
    skitai.mount ("/static", os.path.join (BASE_DIR, 'models/static'))
    skitai.mount ("/media", os.path.join (BASE_DIR, 'models/media'))

def __app__ ():
    return atila.Atila (__name__)
"""

ATILA_INIT = """import atila

def __app__ ():
    return atila.Atila (__name__)
"""

SKITAID = f"""#! /usr/bin/env python3

import os
import sys
import skitai

if __name__ == '__main__':
    import %s

    with skitai.preference () as pref:
        pref.config.MAX_UPLOAD_SIZE = 1 * 1024 * 1024 * 1024
        skitai.mount ('/', %s, pref)

    skitai.run (ip = '0.0.0.0', port = 5000, name = 'atila-vue', workers = 1)
""" % (BACKEND_DIR, BACKEND_DIR)

def customized_management (manage_main):
    def fixed ():
        APP_ROOT = os.path.abspath (f'./{BACKEND_DIR}/models')
        sys.path.insert (0, APP_ROOT)

        try:
            cmd = sys.argv [1]
        except IndexError:
            return manage_main ()

        if cmd == 'runserver':
            os.system ("./skitaid.py --devel")
            return

        if cmd in ('startproject', 'startatila'):
            assert not os.path.isfile ("./skitaid.py"), "skitaid.py already exists"
            with open (os.path.join ("./skitaid.py"), "w") as f:
                f.write (SKITAID)
            pathtool.mkdir (f"./{BACKEND_DIR}")
            PROJECT_ROOT = os.path.abspath (f'./{BACKEND_DIR}')

            if cmd == 'startatila':
                with open (os.path.join (PROJECT_ROOT, "__init__.py"), "w") as f:
                    f.write (ATILA_INIT)
                return

            with open (os.path.join (PROJECT_ROOT, "__init__.py"), "w") as f:
                f.write (APP_INIT)

            assert len (sys.argv) == 2, "do not give [project name]"
            sys.argv.append ("models")
            sys.argv.append (PROJECT_ROOT)
            manage_main ()
            os.remove (os.path.join (PROJECT_ROOT, "manage.py"))
            os.mkdir (os.path.join (PROJECT_ROOT, "models", APPS_DIR))
            os.mkdir (os.path.join (PROJECT_ROOT, "models", "static"))
            os.mkdir (os.path.join (PROJECT_ROOT, "models", "media"))

            with open (os.path.join (PROJECT_ROOT, "models", "settings.py"), "r") as f:
                d = f.read ()
            with open (os.path.join (PROJECT_ROOT, "models", "settings.py"), "w") as f:
                d = d.replace ("models.urls", "urls")
                d = d.replace ("models.wsgi.application", "wsgi.application")
                d = d.replace ("parent.parent", "parent")
                d += "\nimport os\nSTATIC_ROOT = os.getenv ('STATIC_ROOT') or os.path.join (BASE_DIR, 'static/')\n\n"
                d += "MEDIA_URL = '/media/'\nMEDIA_ROOT = os.path.join(BASE_DIR, 'media/')\n"
                f.write (d)

            with open (os.path.join (PROJECT_ROOT, "models", "wsgi.py"), "r") as f:
                d = f.read ()
            with open (os.path.join (PROJECT_ROOT, "models", "wsgi.py"), "w") as f:
                f.write (d.replace ("models.settings", "settings"))
            with open (os.path.join (PROJECT_ROOT, "models", "urls.py"), "r") as f:
                d = f.read ()

            with open (os.path.join (PROJECT_ROOT, "models", "__init__.py"), "w") as f:
                f.write (MODEL_INIT)

            return

        APP_ROOT = os.path.abspath (f'./{BACKEND_DIR}/models')
        os.chdir (APP_ROOT)

        if cmd == 'startapp':
            path = os.path.join (APP_ROOT, 'orm', sys.argv [2])
            pathtool.mkdir (path)
            sys.argv.insert (3, path)

        manage_main ()

        if cmd == 'startapp':
            path = os.path.join (APP_ROOT, APPS_DIR, sys.argv [2])
            with open (os.path.join (path, 'apps.py')) as f:
                d = f.read ()
                d = d.replace ("name = '", f"name = '{APPS_DIR}.")
            with open (os.path.join (path, 'apps.py'), 'w') as f:
                f.write (d)
            os.remove (os.path.join (path, 'tests.py'))
            os.remove (os.path.join (path, 'views.py'))

    return fixed