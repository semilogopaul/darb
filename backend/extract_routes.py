import os
import django

# Ensure Django settings are properly configured
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")  # Change this if needed

django.setup()  # Setup Django before accessing any settings or URL patterns

from django.urls import get_resolver, URLPattern, URLResolver

# Extract routes from Django
def extract_django_routes():
    try:
        resolver = get_resolver()
        routes = []

        def extract_patterns(patterns, prefix=""):
            for pattern in patterns:
                if isinstance(pattern, URLPattern):  # Regular route
                    url = prefix + str(pattern.pattern)
                    
                    # Handle function-based and class-based views
                    callback = pattern.callback
                    if hasattr(callback, "__name__"):  # Function-based view
                        view_name = callback.__name__
                        module = callback.__module__
                    elif hasattr(callback, "view_class"):  # Class-based view
                        view_name = callback.view_class.__name__
                        module = callback.view_class.__module__
                    else:
                        view_name = "Unknown"
                        module = "Unknown"

                    routes.append(f"- `{url}` → **{module}.{view_name}**")

                elif isinstance(pattern, URLResolver):  # Included route (nested patterns)
                    extract_patterns(pattern.url_patterns, prefix + str(pattern.pattern))

        extract_patterns(resolver.url_patterns)
        return routes if routes else ["No routes found."]
    except Exception as e:
        return [f"Error extracting Django routes: {str(e)}"]

# Detect and document API routes
def main():
    print("# Django API Routes\n")
    routes = extract_django_routes()
    
    # Print the extracted routes
    for route in routes:
        print(route)

if __name__ == "__main__":
    main()
