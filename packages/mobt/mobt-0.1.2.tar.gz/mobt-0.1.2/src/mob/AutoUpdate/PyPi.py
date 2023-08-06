import pkg_resources
import requests

from mob.Logging import mob_logger

APP_NAME = 'mobt'


def check_for_updates():
    # Get the installed version of the app
    installed_version = pkg_resources.get_distribution(APP_NAME).version

    # Get the latest version available on PyPI
    url = f'https://pypi.python.org/pypi/{APP_NAME}/json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latest_version = data['info']['version']
    else:
        latest_version = installed_version  # Fallback to installed version if unable to check for updates

    # Compare the installed and latest versions
    # if latest_version != installed_version:
    # Print a yellow message to the console
    mob_logger().warning(f'New version {latest_version} is available. Please upgrade to the latest version.')
