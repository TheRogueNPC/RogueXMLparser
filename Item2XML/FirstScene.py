from FirstWLO import FirstWLO

def load_default_settings():
    """Load the default settings from default_settings.xml."""
    try:
        with open('Settings/Defaults/default_settings.xml', 'r') as file:
            default_settings = file.read()
    except FileNotFoundError:
        default_settings = ''

    return default_settings

def main():
    default_settings = load_default_settings()
    wlo = FirstWLO(default_settings)
    wlo.run()

if __name__ == '__main__':
    main()
