# Garpix FAQ

Auth module for Django/DRF projects. Part of GarpixCMS.

Used packages: 

* [django rest framework](https://www.django-rest-framework.org/api-guide/authentication/)
* [social-auth-app-django](https://github.com/python-social-auth/social-app-django)
* [django-rest-framework-social-oauth2](https://github.com/RealmTeam/django-rest-framework-social-oauth2)
* etc; see setup.py

## Quickstart

Install with pip:

```bash
pip install garpix_faq
```

Add the `garpix_faq` to your `INSTALLED_APPS`:

```python
# settings.py

# ...
INSTALLED_APPS = [
    # ...
    'garpix_faq',
]
```

and to migration modules:

```python
# settings.py

# ...
MIGRATION_MODULES = {
    'garpix_faq': 'app.migrations.garpix_faq',
}
```

Add to `urls.py`:

```python

# ...
urlpatterns = [
    # ...
    # garpix_faq
    path('', include(('garpix_faq.urls', 'faq'), namespace='garpix_faq')),

]
```

Enjoy!

See `garpix_faq/tests.py` for examples.

# Changelog

See [CHANGELOG.md](backend/garpix_faq/CHANGELOG.md).

# Contributing

See [CONTRIBUTING.md](backend/garpix_faq/CONTRIBUTING.md).

# License

[MIT](LICENSE)

---

Developed by Garpix / [https://garpix.com](https://garpix.com)