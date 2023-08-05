=====
BCMR
=====

BCMR or Bitcoin Cash Metadata Registry is a Django app for storing, accessing and managing CashToken BCMRs.

Quick start
-----------

1. Add "bcmr" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'bcmr',
    ]

2. Include the bcmr URLconf in your project urls.py like this::

    path('bcmr/', include('bcmr.urls')),

3. Run ``python manage.py migrate`` to create the bcmr models.

4. Start the development server and visit http://localhost:8000/admin/
   to access the DB (you'll need the Admin app enabled).

5. Visit http://localhost:8000/bcmr/ to check API endpoints for BCMRs and tokens.
