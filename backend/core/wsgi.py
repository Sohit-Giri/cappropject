import os
import sys
from django.core.wsgi import get_wsgi_application

# 1. Get the absolute path to the directory containing this file (backend/core)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Get the path to the parent directory (backend/)
backend_dir = os.path.dirname(current_dir)

# 3. Append the backend folder path into Python's global search path array if it isn't already there
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# 4. Set the default Django settings module environment variable pointer
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 5. Initialize the application engine
application = get_wsgi_application()

# 6. Expose the serverless app runner hook for Vercel
app = application