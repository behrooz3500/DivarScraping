class TabWidgetConstants:
    TAB_1_NAME = "main"
    TAB_2_NAME = "Result"
    TAB_3_NAME = "Settings"
    RESUME_BUTTON_TEXT = "Resume"
    PAUSE_BUTTON_TEXT = "Pause"
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 400
    WINDOWS_TITLE = "Web Scraping"
    FILL_THE_BLANKS_ERROR = "Please fill in the blanks"
    WRONG_INPUT = "Please enter valid inputs"


class MainTabConstants:
    URL_LABEL_TEXT = "Add url      "
    PATTERN_LABEL_TEXT = "Url pattern"
    DEFAULT_URL_PATTERN = "https://divar.ir/v"
    URL_EDIT_BOX_WIDTH = 440
    PATTERN_EDIT_BOX_WIDTH = 440
    URL_LIST_WIDTH = 550
    URL_LIST_HEIGHT = 300
    URL_ADD_BUTTON = "Add"
    START_BUTTON_TEXT = "Start"
    PAUSE_BUTTON_TEXT = "Pause"
    STOP_BUTTON_TEXT = "Stop"


class ResultTabConstants:
    SHOW_BUTTON_TEXT = "Show links"
    COMBO_BOX_WIDTH = 440


class SettingsTabConstants:
    AUTOMATIC_RADIO_BUTTON_TEXT = "Automatic"
    MANUAL_RADIO_BUTTON_TEXT = "Manual"
    SCROLL_MODE_TEXT = "Scroll mode"
    SCROLL_NUMBER_TEXT = "Number of scrolls"
    TIME_OUT_TEXT = "Time out (tries)"
    SCROLL_WAIT_TIME_TEXT = "Scroll wait time"
    PAGE_SIZE_TEXT = "Page size(%)"
    HIDE_IMAGE_TEXT = "Hide images"
    MAXIMIZED_WINDOW_TEXT = "Maximize window"
    TEXT_EDIT_WIDTH = 50
    SAVE_BUTTON_TEXT = "Save"
    DEFAULT_BUTTON_TEXT = "Restore to defaults"
    ERROR_LOADING_WAIT_TIME_TEXT = "Time before page refresh"


class SettingsParameterConstants:
    SCROLL_MODE = "scroll_mode"
    SCROLL_COUNT = "number_of_scrolls"
    SCROLL_MODE_AUTO = "automatic"
    SCROLL_MODE_MANUAL = "manual"
    SCROLL_WAIT_TIME = "scroll_wait_time"
    SCROLL_TIME_OUT = "time_out"
    ERROR_TIME_OUT = "time_before_refresh_button"
    HIDE_IMAGE_SETTING = "hide_image"
    MAXIMIZE_PAGE_SETTING = "maximize_page"


class GlobalConstants:
    URLS_TEXT = "urls"
    SETTINGS_FILE_NAME = "settings.json"
    PATTERN_TEXT = "pattern"


class ScrapperConstants:
    FIREFOX_BROWSER_NAME = "Firefox"
    DIVAR_STORE_CLASS_NAME = "kt-post-card__bottom-description"
    DIVAR_ATT1 = "پیش"
    DIVAR_ATT2 = "روز"
    FIREFOX_32_DRIVER_DIR = "./Drivers/geckodriver32.exe"
    FIREFOX_64_DRIVER_DIR = "./Drivers/geckodriver64.exe"


class MessageBoxConstants:
    NO_URL_EXIST = "Please enter new urls to scrape!"
    SCRAPING_FINISHED = "Scraping urls finished!"
    BOX_TITLE = "Attention"
    SAVE_SETTINGS = "Save Complete!"

