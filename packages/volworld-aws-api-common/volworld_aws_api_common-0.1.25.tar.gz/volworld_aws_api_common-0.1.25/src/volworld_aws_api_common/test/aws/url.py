
from volworld_aws_api_common.api.AA import AA

URL_ROOT = "https://cxglkelavj.execute-api.ap-northeast-1.amazonaws.com/prod/"


def build_api_root_url(*elms) -> str:
    es = list()
    for e in elms:
        es.append(e)
    return f"{URL_ROOT}/{AA.Api}/{'/'.join(es)}"
    # return URL_ROOT + '/' + '/'.join(es)


def build_url(root, *elms) -> str:
    es = list()
    for e in elms:
        es.append(e)
    return f"{root}/{'/'.join(es)}"
    # return root + '/' + '/'.join(es)
