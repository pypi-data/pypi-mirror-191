import json

from .bottle import request, response


def response_json(data, **kwargs):
    # 解决字符编码问题: ensure_ascii=False
    return json.dumps(data, default=str, ensure_ascii=False, sort_keys=True, **kwargs)

def enable_cors(fn):
    # 参考文档:
    # https://stackoverflow.com/a/17262900
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Headers
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Methods
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin
    def _enable_cors(*args, **kwargs):
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.headers['Access-Control-Allow-Methods'] = '*'
        response.headers['Access-Control-Allow-Origin'] = '*'
        if request.method != 'OPTIONS':
            return fn(*args, **kwargs)
    return _enable_cors
