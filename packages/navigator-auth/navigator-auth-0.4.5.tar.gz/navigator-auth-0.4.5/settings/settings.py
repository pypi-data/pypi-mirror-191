from navconfig import config

AUTH_MISSING_ACCOUNT = config.get(
    'AUTH_MISSING_ACCOUNT', fallback='create'
)

# List of function callbacks called (in order) when a user is
AUTH_SUCCESSFUL_CALLBACKS = (
    'resources.auth.last_login',
    'resources.auth.saving_troc_user'
)

AUTHORIZATION_MIDDLEWARES = (
    # 'navigator.auth.middlewares.django_middleware',
    # 'navigator.auth.middlewares.troctoken_middleware',
)

AUTHENTICATION_BACKENDS = (
 'navigator_auth.backends.GoogleAuth',
 'navigator_auth.backends.OktaAuth',
 'navigator_auth.backends.ADFSAuth',
 'navigator_auth.backends.GithubAuth',
 'navigator_auth.backends.AzureAuth',
 'navigator_auth.backends.APIKeyAuth',
 'navigator_auth.backends.TokenAuth',
 'navigator_auth.backends.TrocToken',
 'navigator_auth.backends.DjangoAuth',
 'navigator_auth.backends.BasicAuth',
 'navigator_auth.backends.NoAuth',
)

## AUTH_USER_MODEL: Model used for getting User Information
AUTH_USER_VIEW = 'resources.user.User'
