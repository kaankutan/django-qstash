> :warning: **BETA Software**: Working on being production-ready soon.

# Django QStash `pip install django-qstash`

A drop-in replacement for Celery's shared_task leveraging Upstash QStash for a truly serverless Django application to run background tasks asynchronously from the request/response cycle.

## Installation

```bash
pip install django-qstash
```

Depends on:

- [Python 3.10+](https://www.python.org/)
- [Django 5+](https://docs.djangoproject.com/)
- [qstash-py](https://github.com/upstash/qstash-py)

## Usage

```python
# from celery import shared_task
from django_qstash import shared_task

@shared_task
def math_add_task(a, b, save_to_file=False):
    logger.info(f"Adding {a} and {b}")
    if save_to_file:
        with open("math-add-result.txt", "w") as f:
            f.write(f"{a} + {b} = {a + b}")
    return a + b
```

```python
math_add_task.apply_async(args=(12, 454), save_to_file=True)

# or

math_add_task.delay(12, 454, save_to_file=True)
```


## Configuration

### Environment variables


```python
QSTASH_TOKEN="your_token"
QSTASH_CURRENT_SIGNING_KEY="your_current_signing_key"
QSTASH_NEXT_SIGNING_KEY="your_next_signing_key"

# required for django-qstash
DJANGO_QSTASH_DOMAIN="https://example.com"
DJANGO_QSTASH_WEBHOOK_PATH="/qstash/webhook/"
```



`DJANGO_QSTASH_DOMAIN`: Must be a valid and publicly accessible domain. For example `https://djangoqstash.net`

In development mode, we recommend using a tunnel like [Cloudflare Tunnels](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) with a domain name you control. You can also consider [ngrok](https://ngrok.com/). 


`DJANGO_QSTASH_WEBHOOK_PATH`: The path where QStash will send webhooks to your Django application. Defaults to `/qstash/webhook/`


`DJANGO_QSTASH_FORCE_HTTPS`: Whether to force HTTPS for the webhook. Defaults to `True`.
