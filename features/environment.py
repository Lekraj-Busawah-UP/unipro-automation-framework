from datetime import datetime
from selenium import webdriver
from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from behave import *
import os
import platform
import allure

# Initialize the logger once
logger = LogGen.loggen()

SUPPORTED_BROWSERS = ('chrome', 'firefox')


def before_all(context):
    # Records which browser/OS produced this run for the Allure report
    output_dir = 'allure-results'
    os.makedirs(output_dir, exist_ok=True)

    env_properties = {
        'Browser': ReadConfig.get_browser().capitalize(),
        'Headless': ReadConfig.get_headless_mode(),
        'OS': f"{platform.system()} {platform.release()}",
        'Base_URL': ReadConfig.get_application_url(),
    }

    with open(os.path.join(output_dir, 'environment.properties'), 'w') as f:
        for key, value in env_properties.items():
            f.write(f"{key}={value}\n")


def before_feature(context, feature):
    try:
        # 1. Read the URL from Config
        context.base_url = ReadConfig.get_application_url()

        # 2. Setup browser    
        browser_name = ReadConfig.get_browser().lower()
        headless_mode = ReadConfig.get_headless_mode() 

        options = None
        if browser_name == 'chrome':
            options = webdriver.ChromeOptions()
            if headless_mode:
                options.add_argument("--headless=new") 
                options.add_argument("--window-position=-14000,-14000") 
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--window-size=1920,1080")
            context.driver = webdriver.Chrome(options=options)
        
        elif browser_name == 'firefox':
            options = webdriver.FirefoxOptions()
            if headless_mode:
                options.add_argument("--headless")
                options.add_argument("--width=1920")
                options.add_argument("--height=1080")
            context.driver = webdriver.Firefox(options=options)

        else:
            raise ValueError(
                f"Unsupported browser '{browser_name}'. Supported browsers: {', '.join(SUPPORTED_BROWSERS)}"
            )

        context.headless_mode = headless_mode

        if headless_mode:
            context.driver.set_window_size(1920, 1080)
        else:
            context.driver.maximize_window()

        context.driver.implicitly_wait(0) # Ensure no implicit wait
        logger.info(f"**** Started Feature: {feature.name} ****")
    
    except Exception as e:
        logger.error(f"Failed to start feature: {e}")
        assert False, f"Browser setup failed: {e}"


def before_scenario(context, scenario):
    # Reset viewport to desktop
    if hasattr(context, 'driver'):
        if context.headless_mode:
            context.driver.set_window_size(1920, 1080)
        else:
            context.driver.maximize_window()

    logger.info(f"---- Started Scenario: {scenario.name} ----")


def after_step(context, step):
    if step.status != 'passed':
        logger.error(f"Step FAILED: \"{step.name}\" ({step.status}) - {step.error_message}")
        if hasattr(context, 'driver'):
            try:
                # Take the screenshot in memory
                screenshot = context.driver.get_screenshot_as_png()
                
                # Attempt to attach to Allure
                try:
                    allure.attach(
                        screenshot,
                        name="Screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )
                except Exception:
                    logger.warning("Could not attach screenshot to Allure report (Context lost)")

            except Exception as e:
                logger.error(f"Failed to capture screenshot: {e}")


def after_scenario(context, scenario):
    logger.info(f"---- Finished Scenario: {scenario.name} - {scenario.status.name.upper()} ----")


def after_feature(context, feature):
    # Close Browser
    if hasattr(context, 'driver'):
        try:
            context.driver.quit()
            logger.info(f"**** Finished Feature: {feature.name} - Browser Closed ****")
        except Exception:
            pass