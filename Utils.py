def generate_schema_type(element):
    # Check for file path
    if element.text and ('\\' in element.text or '/' in element.text):
        return 'FilePath'

    # Check for boolean value
    if element.text and element.text.lower() in ['true', 'false']:
        return 'Bool'

    # Check for integer value
    try:
        if element.text:
            int(element.text)
            return 'Int'
    except ValueError:
        pass

    # Default to string
    return 'String'
