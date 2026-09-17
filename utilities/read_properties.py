import configparser
import os

config = configparser.RawConfigParser()

# 1. Get the directory of the current script (utilities/read_properties.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up one level to root, then into configurations/config.ini
config_file_path = os.path.join(current_dir, '..', 'configurations', 'config.ini')

config.read(config_file_path)

class ReadConfig:
    @staticmethod
    def get_application_url():
        url = config.get('common info', 'baseURL')
        return url
    
    @staticmethod
    def get_browser():
        browser = config.get('common info', 'browser')
        return browser

    @staticmethod
    def get_browsers():
        # Supports a comma-separated list e.g. "chrome, firefox" for cross-browser runs
        browsers = config.get('common info', 'browser')
        return [b.strip().lower() for b in browsers.split(',') if b.strip()]

    @staticmethod
    def get_implicit_wait():
        implicit_wait = config.get('common info', 'implicit_wait')
        return implicit_wait

    @staticmethod
    def get_page_load_timeout():
        page_load_timeout = config.get('common info', 'page_load_timeout')
        return page_load_timeout
    
    
    @staticmethod
    def get_headless_mode():
        try:
            headless = config.get('common info', 'headless')
            return headless.lower() == 'true'
        except:
            return False
    