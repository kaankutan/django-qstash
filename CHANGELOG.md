# Changelog

All notable changes to this project will be documented in this file.


## [0.0.6] - 2025-01-01

## Added
- `django_qstash.schedules` for QStash Schedules
- Added task schedule management command to sync QStash schedules with Django models
- Updated Tests for django_qstash.schedules

## [0.0.5] - 2025-01-01

No changes, testing bump2version.

## [0.0.4] - 2025-01-01

### Added
- moved configuration requirements to execution time


## [0.0.3] - 2024-12-30

### Added
- django-qstash results app to store task results
- webhook services to save task results
- decoupled webhook view into handlers and exceptions
- new sample django project (`sample_project/`)
- Added management command to clear old task results
- Add more tests for Django model, handlers, exceptions

### Removed
- Old sample django project (`example_project/`)

## [0.0.2] - Skipped

## [0.0.1] - 2024-12-23

### Added
- Proof of concept release
- Initialized django-qstash package
- Django integration for Upstash QStash message queue service
- Message verification using QStash signatures
- Support for handling QStash webhook requests
- Test suite with pytest
- GitHub Actions CI workflow
- Tox configuration for multiple Python and Django versions
- Documentation and examples

[0.0.3]: https://github.com/jmitchel3/django-qstash/compare/v0.0.3...HEAD
[0.0.2]: https://github.com/jmitchel3/django-qstash/compare/v0.0.2...v0.0.3
[0.0.1]: https://github.com/jmitchel3/django-qstash/compare/v0.0.1...v0.0.2
