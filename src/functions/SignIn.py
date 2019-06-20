from urllib import parse
from jinja2 import Environment, FileSystemLoader
from src.models import User
from src.models.AuthorizationCode import AuthorizationCode
from src.utils.decorators import database, validate
# need to do the same checking as before for the parameters
@database
def sign_in(event, context,session):
    post_body = parse.parse_qs(event["body"])
    # TODO: validate post_body using a schema
    parse.un

    email = post_body["email"][0]
    password = post_body["password"][0]
    redirect_uri = post_body["redirect_uri"][0]
    code_challenge_method = post_body["code_challenge_method"][0]
    code_challenge = post_body["code_challenge"][0]

    # TODO: check whether python's not got some wierd string comparrison stuff with types
    user = session.query(User.email == email)[0]
    if not user:
        # TODO: use the right statuscode
        return {"statusCode":400, "error":"email or password is incorrect"}

    if not user.verify_password(password):
        # TODO: use the right statuscode
        return {"statusCode": 400, "error": "email or password is incorrect"}

    code = AuthorizationCode(user.id,code_challenge_method, code_challenge)

    session.add(code)
    session.commit()

    # TODO: find if there's a better way to do this or if this is insecure
    complete_redirect_uri = "{}?redirect_uri={}".format(redirect_uri,str(code.authorization_code))

    j2_env = Environment(loader=FileSystemLoader("templates"),
                         trim_blocks=True)

    webpage = j2_env.get_template('redirect.html').render(redirect_uri=complete_redirect_uri)

    return {"statusCode": 200, "headers": {"Content-Type": "text/html"},"body":webpage}


