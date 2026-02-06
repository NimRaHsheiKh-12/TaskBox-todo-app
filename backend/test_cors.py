from src.config import settings

 HEAD
print("Backend CORS Origins from settings:", settings.backend_cors_origins)
print("Processed CORS Origins:", settings.cors_origins)
print("Type of cors_origins:", type(settings.cors_origins))

print("Current CORS origins:")
for origin in settings.cors_origins:
    print(f"  - {origin}")

print(f"\nBackend CORS origins setting: {settings.backend_cors_origins}")
 003-chatbot-taskbox
