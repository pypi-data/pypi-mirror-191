=====
BCMR
=====

BCMR or Bitcoin Cash Metadata Registry is a Django app for storing, accessing and managing CashToken BCMRs.

Quick start
-----------

1. Add the following to your requirements.txt:
    Pillow==9.4.0
    django-bcmr==x.x.x

2. Add "bcmr" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'bcmr',
    ]

3. Include the bcmr URLconf in your project urls.py like this::

    path('bcmr/', include('bcmr.urls')),

4. Add media config on settings.py::

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

5. (upon deployment) Add media location path on nginx configuration file::

    location /media/ {
        autoindex on;
        alias /<your_path_to the_media_folder>/;
    }

4. Start the development server and visit https://<your_main_project_domain>/admin/
   to access the DB (you'll need the Admin app enabled).

5. Visit https://<your_main_project_domain>/bcmr/ to check API endpoints for BCMRs and tokens.
