# django-structlog-duration

If you use [django-structlog](https://github.com/jrobichaud/django-structlog), this is a little extension that will populate the `request_finished` log with the duration of the request (`request_duration`).

## Installation

Install the package.

```sh
pip install django-structlog-duration
```

Configure the middleware.

```python
MIDDLEWARE = [
    "django_structlog_duration.StartTimer",
    # ...
    "django_structlog.middlewares.RequestMiddleware",
    "django_structlog_duration.StopTimer",
]
```