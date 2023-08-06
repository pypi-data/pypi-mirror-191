from flask import Blueprint, Response

cat_blueprint = Blueprint('flask-cat', __name__)


@cat_blueprint.after_app_request
def cat_error(response):
    if response.status_code >= 400:
        return Response(f'''
            <img src="https://httpcats.com/{response.status_code}.jpg" height="90%" width="60%">
        '''.strip(), response.status_code)

    return response
