# -------------------
## Holds various constants
class Constants:
    ## the module version
    version = None

    # -------------------
    ## initialize the version string
    #
    # @return None
    @staticmethod
    def init():
        import os
        import json
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'version.json')
        with open(path, 'r', encoding='utf-8') as fp:
            j = json.load(fp)
            Constants.version = j['version']
