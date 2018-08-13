#!flask/bin/python
import os
from tawasol import tawasol

port = int(os.environ.get('PORT', 5009))
tawasol.app.run(host='0.0.0.0', port=port, use_reloader=False, threaded=True, debug=True)