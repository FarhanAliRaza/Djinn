SECRET_KEY = "django-insecure-tspss7)m%r!w$ha6@#ik_&tz(k&d_3yk49hpyha-5df_kd#hl8"
DEBUG = True
LOGGING["formatters"]["colored"] = {  # noqa: F821
    "()": "colorlog.ColoredFormatter",
    "format": "%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s",
}
LOGGING["loggers"]["djinn"]["level"] = "DEBUG"  # noqa: F821
LOGGING["handlers"]["console"]["level"] = "DEBUG"  # noqa: F821
LOGGING["handlers"]["console"]["formatter"] = "colored"  # noqa: F821
