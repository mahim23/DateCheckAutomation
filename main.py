from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import randint
from email.message import EmailMessage
import coloredlogs, logging
import yagmail


# ================= ENVIRONMENT CONFIG =================

SLEEP_TIME = 10    # in minutes

MAIN_URL = "https://www.vfsvisaonline.com/Netherlands-Global-Online-Appointment_Zone1/AppScheduling/AppWelcome.aspx?P=c%2F75XIhVUvxD%2BgDk%2BH%2BCGBV5n9rG51cpAkEXPymduoQ%3D"
AVAILABLE_LOCATIONS = ["New Delhi", "Mumbai CG"]
APPLICATION_CATEGORY = "MVV – Study"
NO_DATE_TEXT = "No date(s) available for appointment."

FROM_EMAIL = ""
TO_EMAIL = ""

# ======================================================


def is_available(driver, location):
    if location not in AVAILABLE_LOCATIONS:
        return
    driver.get(MAIN_URL)
    assert "Netherlands Appointment" in driver.title

    try:
        elem = driver.find_element_by_id("plhMain_lnkSchApp").click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "plhMain_lblVAC"))
        )
        select = Select(driver.find_element_by_id('plhMain_cboVAC'))
        select.select_by_visible_text(location)
        driver.find_element_by_id("plhMain_btnSubmit").click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "plhMain_lblVisaCat"))
        )
        select = Select(driver.find_element_by_id('plhMain_cboVisaCategory'))
        select.select_by_visible_text(APPLICATION_CATEGORY)
        driver.find_element_by_id("plhMain_btnSubmit").click()
        driver.implicitly_wait(10)
        try:
            elem = driver.find_element_by_id("plhMain_lblMsg")
            if elem.text != NO_DATE_TEXT:
                raise NoSuchElementException
            return False
        except NoSuchElementException:
            return True
    except Exception as err:
        print()
        logging.error(str(err))
        logging.error("Problem with the web page. Quiting.")
        notify("", error=True, err_desc=err)
        driver.close()
        exit(1)


def notify(location, error=False, err_desc=""):
    yag = yagmail.SMTP(FROM_EMAIL)
    if error == False:
        content = f"Dates possibly found in {location}. Open now {MAIN_URL}"
        subject = "Dates possibly found"
    else:
        subject = "Problem with script"
        content = ["There is some problem with the script. Check your internet and run the script again.",
            "", f"Following error occured:", "", str(err_desc)]
    yag.send(TO_EMAIL, subject, content)


def main():
    while True:
        logger = logging.getLogger(__name__)
        level_styles = coloredlogs.DEFAULT_LEVEL_STYLES
        level_styles["info"] = {'bold': True, 'color': 'blue'}
        coloredlogs.install(
            level='INFO',
            fmt='%(asctime)s %(levelname)s - %(message)s',
            datefmt='%d-%b-%y %H:%M:%S',
            level_styles=level_styles)

        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(options=op)

        logger.info("Chrome driver started.")

        for location in AVAILABLE_LOCATIONS:
            logger.info(f"Starting to check for availability in {location}.")
            res = is_available(driver, location)
            if res is True:
                logger.info("Date found! Notifying via email.")
                notify(location)
                logger.info("Email sent. Quiting.")
                exit(0)
            logger.info("Date not found. Will check again after some time.")
        
        sleep_time = SLEEP_TIME * 60
        sleep_time = randint(sleep_time - 30, sleep_time + 30)
        sleep(sleep_time)


if __name__ == "__main__":
    main()
