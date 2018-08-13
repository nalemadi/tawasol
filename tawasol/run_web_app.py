#!flask/bin/python
import os
from tawasol import app

port = int(os.environ.get('PORT', 5009))
app.run(host='0.0.0.0', port=port, use_reloader=True, debug=True)

