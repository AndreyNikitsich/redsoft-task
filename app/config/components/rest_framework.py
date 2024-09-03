REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication",
    ],
    "TOKEN_OBTAIN_SERIALIZER": "mentors.api.v1.serializers.CustomObtainPairSerializer",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Mentors management API",
    "DESCRIPTION": "Mentors management system",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}