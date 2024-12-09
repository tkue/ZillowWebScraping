from . import Config


def enable_download_in_headless_chrome(driver, download_dir):
    # add missing support for chrome "send_command"  to selenium webdriver
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    command_result = driver.execute("send_command", params)


def get_chrome_options(is_headless = False):
    from selenium.webdriver.chrome.options import Options as ChromeOptions

    options = [
        '--start-maximized'
    ]

    if is_headless:
        for o in ['--headless', '--disable-gpu']:
            options.append(o)

    opts = ChromeOptions()

    for o in options:
        opts.add_argument(o)

    if not is_headless:
        prefs = {"download.default_directory": Config.download_path}
        opts.add_experimental_option("prefs", prefs)

    return opts