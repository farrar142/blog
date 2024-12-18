# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "blog",
        "USER": "sandring",
        "PASSWORD": "gksdjf452@",
        "HOST": "localhost",
        "PORT": "5432",
        "TEST": {"MIRROR": "default"},
    }
}
