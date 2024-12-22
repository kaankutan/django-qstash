from django.conf import settings


def pytest_configure():
    """Configure Django settings for tests"""
    settings.configure(
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=[
            "django_qstash",
        ],
        MIDDLEWARE=[
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
        ],
        ROOT_URLCONF="tests.urls",
        QSTASH_TOKEN="test-token",
        DJANGO_QSTASH_DOMAIN="example.com",
        QSTASH_CURRENT_SIGNING_KEY="current-key",
        QSTASH_NEXT_SIGNING_KEY="next-key",
    )
