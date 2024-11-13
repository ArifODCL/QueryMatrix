from django.core.exceptions import ValidationError
import re

def validate_url_protocol(value):
    # Check if the URL starts with any protocol (http, https, ftp, ws, wss, etc.)
    if not re.match(r'^[a-zA-Z][a-zA-Z\d+\-.]*://', value):
        raise ValidationError('URL must start with a valid protocol (e.g., http://, https://, ftp://, ws://)')