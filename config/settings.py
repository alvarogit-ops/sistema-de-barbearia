"""
Django settings for config project.

Variáveis sensíveis (SECRET_KEY, DEBUG etc.) vêm do arquivo .env na raiz
do projeto ou do ambiente. Veja o .env.example.
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def carregar_env(caminho):
    """Carrega pares CHAVE=valor de um .env simples, sem dependências.

    Variáveis já definidas no ambiente têm prioridade.
    """
    if not caminho.exists():
        return

    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()

        if not linha or linha.startswith("#") or "=" not in linha:
            continue

        chave, valor = linha.split("=", 1)
        os.environ.setdefault(
            chave.strip(), valor.strip().strip('"').strip("'")
        )


carregar_env(BASE_DIR / ".env")


def env_bool(nome, padrao=False):
    valor = os.environ.get(nome)

    if valor is None:
        return padrao

    return valor.strip().lower() in ("1", "true", "yes", "on")


# SECURITY: a chave nunca fica no código nem no repositório.
SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY:
    raise ImproperlyConfigured(
        "Defina SECRET_KEY no arquivo .env (copie de .env.example)."
    )

# SECURITY: em produção, DEBUG deve ser False (padrão).
DEBUG = env_bool("DEBUG", False)

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "ALLOWED_HOSTS", "localhost,127.0.0.1"
    ).split(",")
    if host.strip()
]

LOGIN_URL = "login"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'barber_grid.apps.BarberGridConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Recife'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# Os arquivos ficam em barber_grid/static/, encontrados automaticamente
# pelo AppDirectoriesFinder; não é preciso STATICFILES_DIRS.

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # usado por collectstatic (deploy)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email
# Em desenvolvimento os e-mails são impressos no terminal.
# Em produção, defina EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# e as variáveis EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD.

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "noreply@barbergrid.com"
)


# Segurança extra quando DEBUG=False

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)