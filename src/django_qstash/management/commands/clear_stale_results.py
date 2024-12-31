from __future__ import annotations

from datetime import timedelta

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

DJANGO_QSTASH_RESULT_TTL = getattr(settings, "DJANGO_QSTASH_RESULT_TTL", 604800)


class Command(BaseCommand):
    help = f"""Clears stale task results older than\n
    {DJANGO_QSTASH_RESULT_TTL} seconds (settings.DJANGO_QSTASH_RESULT_TTL)"""

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-input",
            action="store_true",
            help="Do not ask for confirmation",
        )
        parser.add_argument(
            "--since",
            type=int,
            help="The number of seconds ago to clear results for",
        )

    def handle(self, *args, **options):
        no_input = options["no_input"]
        since = options.get("since") or DJANGO_QSTASH_RESULT_TTL
        cutoff_date = timezone.now() - timedelta(seconds=since)
        try:
            TaskResult = apps.get_model("django_qstash_results", "TaskResult")
        except LookupError:
            self.stdout.write(
                self.style.ERROR(
                    "Django QStash Results not installed.\nAdd `django_qstash.results` to INSTALLED_APPS and run migrations."
                )
            )
            return
        to_delete = TaskResult.objects.filter(date_done__lt=cutoff_date)

        if not to_delete.exists():
            self.stdout.write("No stale Django QStash task results found")
            return

        # use input to confirm  deletion
        self.stdout.write(
            f"Deleting {to_delete.count()} task results older than {cutoff_date} ({DJANGO_QSTASH_RESULT_TTL} seconds)"
        )
        if not no_input:
            if input("Are you sure? (y/n): ") != "y":
                self.stdout.write("Skipping deletion")
                return

        deleted_count, _ = to_delete.delete()

        self.stdout.write(
            self.style.SUCCESS(f"Successfully deleted {deleted_count} stale results.")
        )
