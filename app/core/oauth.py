from authlib.integrations.starlette_client import OAuth
from app.core.config import settings


oauth = OAuth()

oauth.register(
    name='google',
    client_id= settings.GOOGLE_CLIENT_ID,
    client_secret= settings.GOOGLE_CLIENT_SECRET,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v3/userinfo',
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    redirect_uri=settings.OAUTH_REDIRECT_URI,
    client_kwargs={'scope': 'openid profile email'}
)
