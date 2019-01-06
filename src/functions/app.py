def app(event, context):
    response = {"statusCode": 200, "body": "Hello, world!"}

    return response


if __name__ == "__main__":
    app(None, None)
