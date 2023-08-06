from .typeConverter import convertParameters,typeNameConvert
from ..setup_browser import VERSION
from json import dumps

__VERSION__=VERSION

def defineExpose(input, output):
    def decorator(func):
        def wrapper(*args):
            inBrowser=False
            try:
                __file__
            except:
                inBrowser=True
            if inBrowser:
                inputTypes=list(map(typeNameConvert,input))
                outputTypes=list(map(typeNameConvert,output))
                return dumps(convertParameters(outputTypes,func(*convertParameters(inputTypes,args))))
            return func(*args)
        return wrapper
    return decorator
