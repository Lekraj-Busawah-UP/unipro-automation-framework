import subprocess
import sys
from utilities.read_properties import ReadConfig


def build_command(browser, output_dir, extra_args):
    # 1. Define the command
    # Runs behave for a single browser, using the Allure formatter, output to its own folder
    command = (
        f"behave -D browser={browser} -D allure_outdir={output_dir} "
        f"-f allure_behave.formatter:AllureFormatter -o {output_dir}"
    )

    # 2. Add any extra arguments passed to this script (like tags)
    # Example usage: python run.py --tags=@mobile
    if extra_args:
        command += " " + " ".join(extra_args)

    return command


def run_tests():
    browsers = ReadConfig.get_browsers()
    extra_args = sys.argv[1:]
    runs = []

    for browser in browsers:
        # Single browser keeps shared folder and multiple browsers get their own
        output_dir = "allure-results" if len(browsers) == 1 else f"allure-results-{browser}"
        command = build_command(browser, output_dir, extra_args)
        print(f"\nRunning on {browser.capitalize()}: {command}")

        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"Tests failed on {browser.capitalize()} (Check report)")

        runs.append((browser, output_dir))

    # 3. Optional: Ask to serve each report immediately
    for browser, output_dir in runs:
        choice = input(f"\nGenerate and serve Allure report for {browser.capitalize()} ({output_dir})? (y/n): ")
        if choice.lower() == 'y':
            try:
                subprocess.run(f"allure serve {output_dir}", shell=True)
            except KeyboardInterrupt:
                print("\nAllure server stopped.")

if __name__ == "__main__":
    run_tests()