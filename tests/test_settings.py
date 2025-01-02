# from django.conf import settings
# from django.test import TestCase


from __future__ import annotations

# class SettingsTestCase(TestCase):
#     def test_required_settings_present(self):
#         """Test that all required QStash settings are present"""
#         self.assertTrue(hasattr(settings, "QSTASH_TOKEN"))
#         self.assertTrue(hasattr(settings, "DJANGO_QSTASH_DOMAIN"))
#         self.assertTrue(hasattr(settings, "QSTASH_CURRENT_SIGNING_KEY"))
#         self.assertTrue(hasattr(settings, "QSTASH_NEXT_SIGNING_KEY"))
#     def test_settings_values(self):
#         """Test that settings have expected test values"""
#         self.assertEqual(settings.QSTASH_TOKEN, "test-token")
#         self.assertEqual(settings.DJANGO_QSTASH_DOMAIN, "example.com")
#         self.assertEqual(settings.QSTASH_CURRENT_SIGNING_KEY, "current-key")
#         self.assertEqual(settings.QSTASH_NEXT_SIGNING_KEY, "next-key")

#     def test_required_apps_installed(self):
#         """Test that required apps are in INSTALLED_APPS"""
#         required_apps = [
#             "django_qstash",
#             "django_qstash.results",
#             "django_qstash.schedules",
#         ]
#         for app in required_apps:
#             self.assertIn(app, settings.INSTALLED_APPS)
