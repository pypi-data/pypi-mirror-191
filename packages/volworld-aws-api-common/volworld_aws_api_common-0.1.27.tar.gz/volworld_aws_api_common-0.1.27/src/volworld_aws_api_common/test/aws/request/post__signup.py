
from volworld_aws_api_common.api.enum.HttpStatus import HttpStatus
from volworld_common.util.id_util import new_rand_test_user_name
from volworld_aws_api_common.api.AA import AA
from volworld_aws_api_common.api.Aws import Aws
from volworld_aws_api_common.api.url import authUrl
from volworld_aws_api_common.test.aws.ATestRequest import ATestRequest
from volworld_aws_api_common.test.request import post_request
from volworld_aws_api_common.test.aws.request.request_util import response_to_dict


def post__signup(
        name: str, pw: str,
        req: ATestRequest,
        ):
    resp_json, resp = post_request(
        authUrl.doSignupUrl, {
            AA.Name: name,
            AA.Password: pw,
        }, req,
        )
    return response_to_dict(resp_json, resp)


def act__signup(name: str = None, pw: str = None) -> dict:
    if name is None:
        name = new_rand_test_user_name()
    if pw is None:
        pw = 'password'
    resp = post__signup(name, pw, ATestRequest(True))
    if resp[AA.Data] is not None:
        assert resp[AA.HttpStatus] == HttpStatus.Created_201.value
        resp[AA.Name] = name
        resp[AA.Password] = pw
        resp[AA.UserId] = resp[AA.Data][AA.UserId]
        return resp
    else:
        assert AA.___Error___ in resp
    return resp

# def act__signup___error(name: str = None, pw: str = None) -> dict:
#     if name is None:
#         name = new_rand_test_user_name()
#     if pw is None:
#         pw = 'password'
#     resp = post__signup(name, pw, ATestRequest(True))
#     assert AA.___Error___ in resp
#     return resp
