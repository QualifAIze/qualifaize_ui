from datetime import datetime


def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"


def format_date(date_string):
    """Format ISO date string to readable format"""
    try:
        if date_string:
            if date_string.endswith('Z'):
                date_string = date_string[:-1] + '+00:00'
            dt = datetime.fromisoformat(date_string)
            return dt.strftime("%b %d, %Y")
    except (ValueError, TypeError):
        pass
    return "Unknown"


def truncate_text(text, max_length=20):
    """Truncate text to specified length with ellipsis"""
    if not text:
        return "N/A"
    return text if len(text) <= max_length else text[:max_length - 3] + "..."


def get_role_display(roles):
    """Convert roles list to display string"""
    if not roles:
        return "Guest"

    # Show all roles, prioritizing highest
    role_priority = {"ADMIN": 3, "USER": 2, "GUEST": 1}
    sorted_roles = sorted(roles, key=lambda x: role_priority.get(x, 0), reverse=True)

    if len(sorted_roles) == 1:
        role = sorted_roles[0]
        if role == "ADMIN":
            return "Administrator"
        elif role == "USER":
            return "User"
        else:
            return "Guest"
    else:
        # Multiple roles - show highest priority
        return get_role_display([sorted_roles[0]])


def get_role_color(roles):
    """Get color for role badge"""
    if not roles:
        return "#6b7280"

    if "ADMIN" in roles:
        return "#dc2626"  # Red for admin
    elif "USER" in roles:
        return "#059669"  # Green for user
    else:
        return "#6b7280"  # Gray for guest
