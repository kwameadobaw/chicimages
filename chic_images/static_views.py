"""
Static files API views for Vercel deployment
"""
import os
from django.http import HttpResponse, Http404, FileResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_http_methods
from django.conf import settings
import mimetypes

@cache_control(max_age=31536000)  # Cache for 1 year
@require_http_methods(["GET"])
def serve_static_api(request, path):
    """
    API endpoint for serving static files in Vercel
    """
    # Security check
    if '..' in path or path.startswith('/'):
        raise Http404("Not found")
    
    # Clean the path
    path = path.strip('/')
    
    # Try different static file locations
    locations = []
    
    # For admin files, try multiple locations
    if path.startswith('admin/'):
        admin_path = path[6:]  # Remove 'admin/' prefix
        from django.contrib import admin
        locations.extend([
            # Django admin package static files
            os.path.join(os.path.dirname(admin.__file__), 'static', 'admin', admin_path),
            # Collected static files
            os.path.join(settings.STATIC_ROOT, path),
            os.path.join(settings.BASE_DIR, 'staticfiles', path),
            os.path.join(settings.BASE_DIR, 'static', path),
        ])
    else:
        # Regular static files
        locations.extend([
            os.path.join(settings.STATIC_ROOT, path),
            os.path.join(settings.BASE_DIR, 'staticfiles', path),
            os.path.join(settings.BASE_DIR, 'static', path),
        ])
    
    # Find the file
    file_path = None
    for location in locations:
        try:
            if os.path.exists(location) and os.path.isfile(location):
                file_path = location
                break
        except Exception:
            continue
    
    if not file_path:
        # If still not found, try to serve admin files from Django's admin package
        if path.startswith('admin/'):
            admin_path = path[6:]
            try:
                from django.contrib import admin
                admin_file = os.path.join(os.path.dirname(admin.__file__), 'static', 'admin', admin_path)
                if os.path.exists(admin_file):
                    file_path = admin_file
            except Exception:
                pass
    
    if not file_path:
        raise Http404(f"Static file not found: {path}")
    
    # Determine content type
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        if file_path.endswith('.css'):
            content_type = 'text/css'
        elif file_path.endswith('.js'):
            content_type = 'application/javascript'
        elif file_path.endswith('.png'):
            content_type = 'image/png'
        elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
            content_type = 'image/jpeg'
        elif file_path.endswith('.gif'):
            content_type = 'image/gif'
        elif file_path.endswith('.svg'):
            content_type = 'image/svg+xml'
        elif file_path.endswith('.woff'):
            content_type = 'font/woff'
        elif file_path.endswith('.woff2'):
            content_type = 'font/woff2'
        elif file_path.endswith('.ttf'):
            content_type = 'font/ttf'
        else:
            content_type = 'application/octet-stream'
    
    try:
        # Read file content
        with open(file_path, 'rb') as f:
            content = f.read()
        
        response = HttpResponse(content, content_type=content_type)
        response['Cache-Control'] = 'public, max-age=31536000'
        response['Access-Control-Allow-Origin'] = '*'
        response['Content-Length'] = len(content)
        
        return response
        
    except Exception as e:
        raise Http404(f"Error serving file: {str(e)}")
