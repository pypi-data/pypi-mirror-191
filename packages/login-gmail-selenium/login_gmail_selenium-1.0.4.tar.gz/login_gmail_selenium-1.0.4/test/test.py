import login_gmail_selenium.util as LGS_util
import login_gmail_selenium.common as LGS_common
import time
import os

if __name__ == '__main__':
    # profile = ChromeProfile('glanmum12@gmail.com', 'q2R1EcNi4', 'grahamma057449@hotmail.com')
    proxy_folder = os.path.join(LGS_common.constant.PROXY_FOLDER, f'proxy_auth')
    profile = LGS_util.profile.ChromeProfile('glanmum12@gmail.com', 'q2R1EcNi4',
                                             'grahamma057449@hotmail.com',
                                             'private', None, 'user22996:SKB3RN@51.81.141.133:22996', 'http',
                                             proxy_folder)
    driver = profile.retrieve_driver()
    profile.start()
    driver.get('https://www.google.com/')
    time.sleep(100)
