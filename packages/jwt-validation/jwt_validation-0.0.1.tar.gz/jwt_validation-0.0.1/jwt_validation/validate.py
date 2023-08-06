"""
Description:
    Layer used for JWT validation

Problem:
    The problem I am trying to solve is the JWT validation.

Scenarios List:
    - A request from OnPrem needs to validated by an AWS Lambda
"""
import http.client
import json
import jwt

def is_jwt_valid(jwt_encoded, hostname, uri):
    """
    Method used for JWT validation.

    Parameters:
        jwt_encoded (str): an encoded JWT
        hostname (str): the hostname of the endpoint which returns the JWKS
        uri (str): the URI of the endpoint which returns the JWKS

    Returns:
        none
    """
    jwt_decoded_header = jwt.get_unverified_header(jwt_encoded)
    kid = jwt_decoded_header['kid']

    connection = http.client.HTTPSConnection(hostname)
    connection.request('GET', uri)
    response = connection.getresponse()
    jwks_json = response.read().decode('utf-8')
    print(jwks_json)

    jwks = json.loads(jwks_json)['keys']

    public_keys = {}
    for jwk in jwks:
        print(jwk['kid'])
        if kid == jwk['kid']:
            print("ok")
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
        else:
            print("nok")

    print(public_keys[kid])

    key = public_keys[kid]

    try:
        payload = jwt.decode(jwt_encoded, key=key, options={"verify_aud": False}, \
                             algorithms=['RS256'])
    except (jwt.InvalidTokenError, jwt.ExpiredSignature, jwt.DecodeError) as exception:
        print("An exception occurred:")
        print(exception)
        return False

    print("payload")
    print(payload)

    return True
