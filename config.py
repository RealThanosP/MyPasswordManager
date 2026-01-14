import json
import os

def load_config(file_path="config.json"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    
    with open(file_path, "r") as f:
        config = json.load(f)
    return config

config_data = load_config()

# Constants
# Window
WIN_WIDTH = config_data["window"]["width"]
WIN_HEIGHT = config_data["window"]["height"]

# Paths
GENERATOR_BUTTON_IMG = config_data["paths"]["generator_button_img"]
COPY_BUTTON_IMG = config_data["paths"]["copy_button_img"]
APP_ICON = config_data["paths"]["app_icon"]
SAVE_IMG = config_data["paths"]["save_img"]
ADD_VAULT_IMG = config_data["paths"]["add_vault_img"]
ENTER_VAULT_IMG = config_data["paths"]["enter_vault_img"]
SEE_PASSWORD_IMG = config_data["paths"]["see_password_img"]
HIDE_PASSWORD_IMG = config_data["paths"]["hide_password_img"]
TRASH_CAN_IMG = config_data["paths"]["trash_can_img"]

# Sizes
BUTTON_SIZE = tuple(config_data["sizes"]["button"])
BUTTON_MEDIUM_SIZE = tuple(config_data["sizes"]["button_medium"])
BUTTON_BIG_SIZE = tuple(config_data["sizes"]["button_big"])

# Fonts and colors
BUTTON_COLOR = config_data["colors"]["button"]
BUTTON_TEXT_COLOR = config_data["colors"]["button_text"]
BUTTON_COLOR_ON_HOVER = config_data["colors"]["button_hover"]
FONT_NAME = config_data["fonts"]["name"]

# Password colors
RED = config_data["colors"]["password"]["red"]
YELLOW = config_data["colors"]["password"]["yellow"]
ORANGE = config_data["colors"]["password"]["orange"]
DARK_GREEN = config_data["colors"]["password"]["dark_green"]
GREEN = config_data["colors"]["password"]["green"]
LIGHT_GREEN = config_data["colors"]["password"]["light_green"]

SAVE_COLOR = config_data["colors"]["frames"]["save"]
SEE_COLOR = config_data["colors"]["frames"]["see"]
ADD_COLOR = config_data["colors"]["frames"]["add"]
DELETE_COLOR = config_data["colors"]["frames"]["delete"]

# Font sizes
FONT_SIZE_LABELS = config_data["fonts"]["size"]["labels"]
FONT_SIZE_COMBOBOX = config_data["fonts"]["size"]["combobox"]
FONT_SIZE_BUTTONS = config_data["fonts"]["size"]["buttons"]
FONT_SIZE_ENTRIES = config_data["fonts"]["size"]["entries"]
FONT_SIZE_SUB_TITLES = config_data["fonts"]["size"]["sub_titles"]
FONT_SIZE_TITLES = config_data["fonts"]["size"]["titles"]

# Paddings
PADDING_CHECKBOX = config_data["paddings"]["checkbox"]
PADDING_TEXT = config_data["paddings"]["text"]
PADDING_SLIDER = config_data["paddings"]["slider"]
PADDING_SAVE_GAP = config_data["paddings"]["save_gap"]
PADDING_COMBOBOX = config_data["paddings"]["combobox"]
PADDING_SLIDER_LABEL = config_data["paddings"]["slider_label"]
PADDING_VAULT_ENTRY = config_data["paddings"]["vault_entry"]

# Layout calculations
GENERATOR_ENTRY_WIDTH = WIN_WIDTH - (4.9 * BUTTON_SIZE[0])
SAVE_ENTRY_WIDTH = config_data["layout"]["save_entry_width"]

SAVE_TEXT_BOX_HEIGHT = config_data["layout"]["save_text_box_height"]
SAVE_COMBOBOX_SIZE = tuple(config_data["layout"]["save_combobox_size"])

SEE_ENTRY_WIDTH = config_data["layout"]["see_entry_width"]
SEE_COMBOBOX_SIZE = tuple(config_data["layout"]["see_combobox_size"])

ADD_ENTRY_WIDTH = config_data["layout"]["add_entry_width"]

DELETE_COMBOBOX_SIZE = tuple(config_data["layout"]["delete_combobox_size"])
