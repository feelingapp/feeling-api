from urllib import parse
# need to do the same checking as before for the parameters
def sign_in(event, context,session):
    my_dict = parse.parse_qs(event["body"])
    print(my_dict)



    return {"statusCode": 200}


