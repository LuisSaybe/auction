import functools
import aiohttp
from jsonschema import validate

def validate_schema(schema):
    def result(func):
        @functools.wraps(func)
        async def wrapper(request):
            try:
                body = await request.json()
            except:
                raise aiohttp.web.HTTPUnsupportedMediaType(
                    text='unable to parse body as json')

            try:
                validate(instance=body, schema=schema)
            except:
                raise aiohttp.web.HTTPBadRequest(
                    text='body does not conform to schema')
            return await func(request)
        return wrapper
    return result
