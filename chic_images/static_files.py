"""
Custom static files handler for Vercel deployment
"""
import os
from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_http_methods
import mimetypes

@cache_control(max_age=31536000)  # Cache for 1 year
@require_http_methods(["GET"])
def serve_static(request, path):
    """
    Custom static file serving for Vercel deployment
    """
    # Security check - prevent directory traversal
    if '..' in path or path.startswith('/'):
        raise Http404("Not found")
    
    # Try multiple static file locations
    possible_paths = [
        os.path.join(settings.STATIC_ROOT, path),
        os.path.join(settings.BASE_DIR, 'static', path),
    ]
    
    # For Django admin files, also check the admin static directory
    if path.startswith('admin/'):
        from django.contrib import admin
        admin_static_path = os.path.join(os.path.dirname(admin.__file__), 'static', 'admin', path[6:])
        possible_paths.insert(0, admin_static_path)
    
    static_path = None
    for possible_path in possible_paths:
        if os.path.exists(possible_path):
            static_path = possible_path
            break
    
    if static_path is None:
        raise Http404("Static file not found")
    
    # Determine content type
    content_type, _ = mimetypes.guess_type(static_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    # Read and serve the file
    try:
        with open(static_path, 'rb') as f:
            content = f.read()
        
        response = HttpResponse(content, content_type=content_type)
        response['Content-Length'] = len(content)
        
        # Set appropriate headers for different file types
        if path.endswith(('.css', '.js')):
            response['Cache-Control'] = 'public, max-age=31536000'
        elif path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')):
            response['Cache-Control'] = 'public, max-age=31536000'
        
        return response
        
    except Exception as e:
        raise Http404(f"Error serving static file: {str(e)}")
