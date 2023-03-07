# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# This file is included in the final Docker image and SHOULD be overridden when
# deploying the image to prod. Settings configured here are intended for use in local
# development environments. Also note that superset_config_docker.py is imported
# as a final step as a means to override "defaults" configured here
#
import logging
import os
from datetime import timedelta
from typing import Optional

from cachelib.file import FileSystemCache
from celery.schedules import crontab

from superset.superset_typing import CacheConfig
from superset.constants import CHANGE_ME_SECRET_KEY
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Type,
    TYPE_CHECKING,
    Union,
)

logger = logging.getLogger()


def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)

# TODO: Change the following in deployment config:
SECRET_KEY = CHANGE_ME_SECRET_KEY

SMTP_HOST = "localhost"
SMTP_STARTTLS = True
SMTP_SSL = False
SMTP_USER = "superset"
SMTP_PORT = 25
SMTP_PASSWORD = "superset"
SMTP_MAIL_FROM = "superset@superset.com"

MAPBOX_API_KEY = os.environ.get("MAPBOX_API_KEY", "")

SLACK_API_TOKEN: Optional[Union[Callable[[], str], str]] = None
SLACK_PROXY = None

# This is an important setting, and should be lower than your
# [load balancer / proxy / envoy / kong / ...] timeout settings.
# You should also make sure to configure your WSGI server
# (gunicorn, nginx, apache, ...) timeout setting to be <= to this setting
SUPERSET_WEBSERVER_TIMEOUT = int(timedelta(minutes=1).total_seconds())

WEBDRIVER_BASEURL = "http://0.0.0.0:8080/"
# The base URL for the email report hyperlinks.
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL

# BJC - Possibly Look at in the future
# Send user to a link where they can read more about Superset
DOCUMENTATION_URL = None
DOCUMENTATION_TEXT = "Documentation"
DOCUMENTATION_ICON = None  # Recommended size: 16x16




DATABASE_DIALECT = get_env_variable("DATABASE_DIALECT")
DATABASE_USER = get_env_variable("DATABASE_USER")
DATABASE_PASSWORD = get_env_variable("DATABASE_PASSWORD")
DATABASE_HOST = get_env_variable("DATABASE_HOST")
DATABASE_PORT = get_env_variable("DATABASE_PORT")
DATABASE_DB = get_env_variable("DATABASE_DB")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (
    DATABASE_DIALECT,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_DB,
)

REDIS_HOST = get_env_variable("REDIS_HOST")
REDIS_PORT = get_env_variable("REDIS_PORT")
REDIS_CELERY_DB = get_env_variable("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = get_env_variable("REDIS_RESULTS_DB", "1")

RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

CACHE_CONFIG = {
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}
DATA_CACHE_CONFIG = CACHE_CONFIG


class CeleryConfig(object):
    BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    CELERY_IMPORTS = ("superset.sql_lab",)
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    CELERYD_LOG_LEVEL = "DEBUG"
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_ACKS_LATE = False
    CELERYBEAT_SCHEDULE = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig

FEATURE_FLAGS = {
    # allow dashboard to use sub-domains to send chart request
    # you also need ENABLE_CORS and
    # SUPERSET_WEBSERVER_DOMAINS for list of domains
    "ALLOW_DASHBOARD_DOMAIN_SHARDING": True,
    # Experimental feature introducing a client (browser) cache
    "CLIENT_CACHE": False,
    "DISABLE_DATASET_SOURCE_EDIT": False,
    # When using a recent version of Druid that supports JOINs turn this on
    "DRUID_JOINS": True,
    "DYNAMIC_PLUGINS": False,
    # With Superset 2.0, we are updating the default so that the legacy datasource
    # editor no longer shows. Currently this is set to false so that the editor
    # option does show, but we will be depreciating it.
    "DISABLE_LEGACY_DATASOURCE_EDITOR": True,
    # For some security concerns, you may need to enforce CSRF protection on
    # all query request to explore_json endpoint. In Superset, we use
    # `flask-csrf <https://sjl.bitbucket.io/flask-csrf/>`_ add csrf protection
    # for all POST requests, but this protection doesn't apply to GET method.
    # When ENABLE_EXPLORE_JSON_CSRF_PROTECTION is set to true, your users cannot
    # make GET request to explore_json. explore_json accepts both GET and POST request.
    # See `PR 7935 <https://github.com/apache/superset/pull/7935>`_ for more details.
    "ENABLE_EXPLORE_JSON_CSRF_PROTECTION": True,
    "ENABLE_TEMPLATE_PROCESSING": False,
    "ENABLE_TEMPLATE_REMOVE_FILTERS": False,
    # Allow for javascript controls components
    # this enables programmers to customize certain charts (like the
    # geospatial ones) by inputing javascript in controls. This exposes
    # an XSS security vulnerability
    "ENABLE_JAVASCRIPT_CONTROLS": False,
    "KV_STORE": False,
    # When this feature is enabled, nested types in Presto will be
    # expanded into extra columns and/or arrays. This is experimental,
    # and doesn't work with all nested types.
    "PRESTO_EXPAND_DATA": False,
    # Exposes API endpoint to compute thumbnails
    "THUMBNAILS": True,
    "DASHBOARD_CACHE": True,
    "REMOVE_SLICE_LEVEL_LABEL_COLORS": False,
    "SHARE_QUERIES_VIA_KV_STORE": False,
    "TAGGING_SYSTEM": False,
    "SQLLAB_BACKEND_PERSISTENCE": True,
    "LISTVIEWS_DEFAULT_CARD_VIEW": True,
    # When True, this flag allows display of HTML tags in Markdown components
    "DISPLAY_MARKDOWN_HTML": True,
    # When True, this escapes HTML (rather than rendering it) in Markdown components
    "ESCAPE_MARKDOWN_HTML": False,
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": False,
    # Feature is under active development and breaking changes are expected
    "DASHBOARD_NATIVE_FILTERS_SET": False,
    "DASHBOARD_FILTERS_EXPERIMENTAL": False,
    "GLOBAL_ASYNC_QUERIES": False,
    "VERSIONED_EXPORT": True,
    "EMBEDDED_SUPERSET": False,
    # Enables Alerts and reports new implementation
    "ALERT_REPORTS": True,
    "DASHBOARD_RBAC": False,
    "ENABLE_EXPLORE_DRAG_AND_DROP": True,
    "ENABLE_FILTER_BOX_MIGRATION": False,
    "ENABLE_ADVANCED_DATA_TYPES": False,
    "ENABLE_DND_WITH_CLICK_UX": True,
    # Enabling ALERTS_ATTACH_REPORTS, the system sends email and slack message
    # with screenshot and link
    # Disables ALERTS_ATTACH_REPORTS, the system DOES NOT generate screenshot
    # for report with type 'alert' and sends email and slack message with only link;
    # for report with type 'report' still send with email and slack message with
    # screenshot and link
    "ALERTS_ATTACH_REPORTS": True,
    # FORCE_DATABASE_CONNECTIONS_SSL is depreciated.
    "FORCE_DATABASE_CONNECTIONS_SSL": False,
    # Enabling ENFORCE_DB_ENCRYPTION_UI forces all database connections to be
    # encrypted before being saved into superset metastore.
    "ENFORCE_DB_ENCRYPTION_UI": False,
    # Allow users to export full CSV of table viz type.
    # This could cause the server to run out of memory or compute.
    "ALLOW_FULL_CSV_EXPORT": True,
    "UX_BETA": False,
    "GENERIC_CHART_AXES": False,
    "ALLOW_ADHOC_SUBQUERY": False,
    "USE_ANALAGOUS_COLORS": True,
    # Apply RLS rules to SQL Lab queries. This requires parsing and manipulating the
    # query, and might break queries and/or allow users to bypass RLS. Use with care!
    "RLS_IN_SQLLAB": False,
    # Enable caching per impersonation key (e.g username) in a datasource where user
    # impersonation is enabled
    "CACHE_IMPERSONATION": False,
}

ALERT_REPORTS_NOTIFICATION_DRY_RUN = True
WEBDRIVER_BASEURL = "http://superset:8088/"
# The base URL for the email report hyperlinks.
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL

SQLLAB_CTAS_NO_LIMIT = True


# Cache Configs
THUMBNAIL_CACHE_CONFIG: CacheConfig = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 24*60*60,
    'CACHE_KEY_PREFIX': 'thumbnail_',
    'CACHE_NO_NULL_WARNING': True,
    'CACHE_REDIS_URL': f"redis://{REDIS_HOST}:{REDIS_PORT}"
}
# WebDriver configuration
# If you use Firefox, you can stick with default values
# If you use Chrome, then add the following WEBDRIVER_TYPE and WEBDRIVER_OPTION_ARGS
WEBDRIVER_TYPE = "chrome"
WEBDRIVER_OPTION_ARGS = [
    "--force-device-scale-factor=2.0",
    "--high-dpi-support=2.0",
    "--headless",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-extensions",
]
EXPLORE_FORM_DATA_CACHE_CONFIG: CacheConfig = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_KEY_PREFIX': 'superset_form_',
    'CACHE_NO_NULL_WARNING': True,
    'CACHE_REDIS_URL': f"redis://{REDIS_HOST}:{REDIS_PORT}"
}

FILTER_STATE_CACHE_CONFIG: CacheConfig = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_KEY_PREFIX': 'superset_filter_',
    'CACHE_NO_NULL_WARNING': True,
    'CACHE_REDIS_URL': f"redis://{REDIS_HOST}:{REDIS_PORT}"
}

PREFERRED_DATABASES: List[str] = [
    "PostgreSQL",
    "Apache Druid",
    "Google Sheets",
    "MySQL",
    "SQLite",
    "Presto",
    # etc.
]
EXTRA_CATEGORICAL_COLOR_SCHEMES = [
     {
         "id": 'switchdin',
         "description": 'Switchdin Colours',
         "label": 'SwitchDin',
         "isDefault": True,
         "colors":
          ['#00B299', '#40C5B2', '#80D8CC', '#C0EBE5', '#CDD0D2', '#9BA0A4', '#697177',
          '#37424A']
     },
     # {
     #     "id": 'acciona',
     #     "description": '',
     #     "label": 'Acciona',
     #     "isDefault": False,
     #     "colors":
     #      ['#FF6464', '#FF0000', '#9B0000', '#7F7E7E', '#464646', '#000000']
     # },
     {
         "id": 'ausgrid',
         "description": 'AusGrid Colours',
         "label": 'AusGrid',
         "isDefault": False,
         "colors":
          ['#73B818', '#69AC40', '#008BC0', '#006095', '#1D9CA6']
     },
     {
         "id": 'jacana',
         "description": 'Jacana Colours',
         "label": 'Jacana',
         "isDefault": False,
         "colors":
          ['#b8c496', '#D9C796', '#F3643D', '#F68224', '#213E52']
     },
     {
         "id": 'origin',
         "description": 'Origin Colours',
         "label": 'Origin',
         "isDefault": False,
         "colors":
          ['#FF373C', '#FA4616', '#FF8133', '#FFB92D', '#D44500']
     },
     {
         "id": 'sapn',
         "description": 'SAPN Colours',
         "label": 'SAPN',
         "isDefault": False,
         "colors":
          ['#284051', '#1F4C71', '#FA7A0A', '#535353', '#1A1614']
     },
     {
         "id": 'simplyenergy',
         "description": 'Simply Energy Colours',
         "label": 'Simply Energy',
         "isDefault": False,
         "colors":
          ['#2CC5F3', '#00A3E2', '#006CB7', '#FDF859', '#62A833']
     },
     {
         "id": 'yurika',
         "description": 'Yurika Colours',
         "label": 'Yurika',
         "isDefault": False,
         "colors":
          ['#5e2590', '#b12d76', '#f03f52', '#F37229', '#a13421']
     },
     {
        "id": 'synergy',
        "description": 'Synergy Colours',
        "label": 'Synergy',
        "isDefault": False,
        "colors":
        ['#009B77', '#00968F', '#00A9E0', '#41B6E6', '#E5E6E5']
     }
    ]

# This is merely a default
# EXTRA_CATEGORICAL_COLOR_SCHEMES: List[Dict[str, Any]] = []

# THEME_OVERRIDES is used for adding custom theme to superset
# example code for "My theme" custom scheme
THEME_OVERRIDES = {
  "borderRadius": 4,
  "colors": {
    "primary": {
      "base": '#00B299',
      "dark1": '#007564',
      "dark2": '#00584F',
      "light1": '#7ED3C3',
      "light2": '#B2E4DA',
      "light3": '#E0F4F1',
      # "light4": '#E9F6F9',
      # "light5": '#F3F8FA',
    },
    "secondary": {
        "base": '#007564',
        "dark1": '#363E63',
        "dark2": '#282E4A',
        "dark3": '#1B1F31',
        "light1": '#8E94B0',
        "light2": '#B4B8CA',
        "light3": '#D9DBE4',
        "light4": '#ECEEF2',
        "light5": '#F5F5F8',
    },
    "grayscale": {
        "base": '#1f1f1f',
        "dark1": '#4b4b4b',
        "dark2": '#5c5c5c',
        "light1": '#B1BAC1',
        "light2": '#D0D6D9',
        # "light3": '#F0F0F0',
        # "light4": '#F7F7F7',
        # "light5": '#FFFFFF',
    }#,
    #"link": '#00B299'
  }
}


#
# Optionally import superset_config_docker.py (which will have been included on
# the PYTHONPATH) in order to allow for local settings to be overridden
#
try:
    import superset_config_docker
    from superset_config_docker import *  # noqa

    logger.info(
        f"Loaded your Docker configuration at " f"[{superset_config_docker.__file__}]"
    )
except ImportError:
    logger.info("Using default Docker config...")
