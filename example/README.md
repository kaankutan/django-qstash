Example Django Application
===================

Use Python 3.13 to set up and run with these commands:

```
echo "QSTASH_TOKEN=your_token" >> .env
echo "QSTASH_CALLBACK_URL=your_callback_url" >> .env
```

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt -e ..
DEBUG=1 python manage.py runserver
```

Open it at http://127.0.0.1:8000/ .

Browse the individual examples, and take them apart!

In your browser’s devtools, you can read the  `debug log <https://.org/extensions/debug/>`__ in your browser’s console, and see the requests made in the network tab.
In the source code, check out the HTML comments via “view source” or templates, and the view code in ``example/views.py``.
