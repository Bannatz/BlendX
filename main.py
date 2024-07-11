import dearpygui.dearpygui as dpg
import os
from utils.textutils import Text_Edit
from utils.proxyscraper import ProxyScraper
from utils.proxychecker import ProxyChecker

def register_fonts():
    fonts_dir = "Fonts"
    if not os.path.isdir(fonts_dir):
        print(f"Directory '{fonts_dir}' not found.")
        return
    with dpg.font_registry():
        for root, _, files in os.walk(fonts_dir):
            for file in files:
                if file.endswith(".ttf") or file.endswith(".otf"):
                    font_path = os.path.join(root, file)
                    if os.path.exists(font_path):
                        try:
                            dpg.add_font(font_path, 12)
                        except Exception as e:
                            print(f"Failed to add font {font_path}: {e}")
                    else:
                        print(f"Font file '{font_path}' not found.")

def file_dialog(sender, app_data):
    file_path = app_data["file_path_name"]
    lines = Text_Edit.load_txt(file_path)
    dpg.configure_item("combo_list", items=lines)

def context_menu_callback(sender, app_data):
    print("Hello World!")  # Placeholder for context menu functionality

def save_callback(sender, app_data):
    file_path = app_data["file_path_name"]
    if dpg.is_item_shown("proxy_list"):
        proxy_list = dpg.get_item_configuration('proxy_list')["items"]
        Text_Edit.save_txt(file_path, proxy_list)
    if dpg.is_item_shown("combo_list"):
        combo_list = dpg.get_item_configuration('combo_list')["items"]
        Text_Edit.save_txt(file_path=file_path, combo_list)
    if dpg.is_item_shown("proxy_list") and dpg.is_item_shown("combo_list"):
        proxy_file_path = file_path.replace(".txt", "_proxy.txt")
        combo_file_path = file_path.replace(".txt", "_combo.txt")
        Text_Edit.save_txt(combo_file_path, combo_list)
        Text_Edit.save_txt(proxy_file_path, proxy_list)

def callback_scrape(sender, app_data):
    dpg.configure_item("proxy_list", items=[])
    method = dpg.get_value('proxyscrape_lb')
    timeout = dpg.get_value('timeout_inp_int')
    prots = dpg.get_value('protocols_inp_txt')
    ssl = dpg.get_value('ssl_bool')
    ps = ProxyScraper(method)
    if method == "Proxyscrape":
        proxy_list = ps.proxy_scrape(timeout, prots, ssl)
        dpg.configure_item("proxy_list", items=proxy_list)
        dpg.configure_item("proxy_list", label=f"Proxies: {len(proxy_list)}")
    if method == "All":
        proxy_list = ps.all_apis("http", prots, "fast", 500)
        dpg.configure_item("proxy_list", items=proxy_list)
        dpg.configure_item("proxy_list", label=f"Proxies: {len(proxy_list)}")

def del_dupes_callback(sender, app_data):
    lines = dpg.get_item_configuration("combo_list")["items"]
    Text_Edit.del_dupes(lines)
    dpg.configure_item("combo_list", items=lines)

def sort_items_callback(sender, app_data):
    lines = dpg.get_item_configuration("combo_list")["items"]
    Text_Edit.sort_items(lines)
    dpg.configure_item("combo_list", items=lines)

def callback_check(sender, app_data):
    prots = dpg.get_value('protocols_inp_txt')
    timeout = dpg.get_value('ctimeout_inp_int')
    proxies = dpg.get_item_configuration('proxy_list')["items"]
    dpg.configure_item("proxy_scrape_window_id", label="ProxyChecker (COULD TAKE A WHILE)")
    checker = ProxyChecker()
    working_proxies, failed_proxies, errored_proxies = checker.check_proxy(prots, timeout, proxies)
    dpg.configure_item("proxy_list", label=f"Working Proxies: {len(working_proxies)}\nFailed Proxies: {len(failed_proxies)}\nErrored Proxies: {len(errored_proxies)}")
    dpg.configure_item("proxy_list", items=working_proxies)

def font_selection_callback(sender, app_data):
    selected_font = dpg.get_value(sender)
    dpg.bind_font(selected_font)

def main():
    dpg.create_context()  # Initialize DearPyGui context
    register_fonts()
    # Calculate listbox size based on content
    num_items = 20
    item_height = 20
    listbox_width = 240
    listbox_height = num_items * item_height
    
    with dpg.window(label="Proxy Scraper", width=600, height=300, no_resize=False, show=False, tag="proxy_scrape_window_id"):
        dpg.add_listbox(items=["Proxyscrape", "All"], label="Method", tag="proxyscrape_lb", width=150, num_items=2)
        dpg.add_listbox(items=[], label="Proxies", tag="proxy_list", pos=[250, 40], width=150, num_items=10)
        dpg.add_checkbox(label="SSL", tag="ssl_bool", pos=[200, 150])
        dpg.add_spacer()
        dpg.add_listbox(label="Protocols", tag="protocols_inp_txt", items=["http", "socks4", "socks5"], width=150)
        dpg.add_spacer()
        dpg.add_input_int(label="Timeout", tag="timeout_inp_int", default_value=10000, min_value=1000, max_value=10000, width=100)
        dpg.add_input_int(label="Checker Timeout", tag="ctimeout_inp_int", default_value=10, min_value=10, max_value=10000, width=100)
        dpg.add_spacer()
        dpg.add_button(label="Scrape..", callback=callback_scrape, tag="button_ps")
        dpg.add_button(label="Check", callback=callback_check, tag="button_cp")

    with dpg.window(label="Combo Editor", width=600, height=300, no_resize=True, no_title_bar=False, no_move=False, show=False, tag="combo_window"):
        dpg.set_item_pos("combo_window", [0, 20])
        with dpg.viewport_menu_bar():
            with dpg.menu(label="General"):
                dpg.add_menu_item(label="Open File..", callback=lambda: dpg.show_item("file_dialog_id"))
                dpg.add_menu_item(label="Save..", callback=lambda: dpg.show_item("save_dialog_id"))
                dpg.add_menu_item(label="Exit", callback=dpg.stop_dearpygui)
            with dpg.menu(label="Edit"):
                dpg.add_menu_item(label="Delete Dupes", callback=del_dupes_callback)
                dpg.add_menu_item(label="Sort", callback=sort_items_callback)
            with dpg.menu(label="Utils"):
                dpg.add_menu_item(label="Combo Editor", callback=lambda: dpg.show_item("combo_window"))
                dpg.add_menu_item(label="Proxy Scraper", callback=lambda: dpg.show_item("proxy_scrape_window_id"))
            with dpg.menu(label="Theming"):
                dpg.add_menu_item(label="Open Theme Editor..", tag="theme_editor_mitem", callback=lambda: dpg.show_style_editor())
                dpg.add_menu_item(label="Show Font Manager..", callback=lambda: dpg.show_font_manager())
        with dpg.file_dialog(directory_selector=False, show=False, callback=file_dialog, tag='file_dialog_id'):
            dpg.add_file_extension(".txt", color=(150, 255, 150, 255))

        with dpg.file_dialog(directory_selector=False, show=False, callback=save_callback, tag='save_dialog_id'):
            dpg.add_file_extension(".txt", color=(150, 255, 150, 255))

        dpg.add_separator()
        dpg.add_text("Combo List:")
        dpg.add_listbox(items=[], tag="combo_list", width=240, num_items=20, callback=context_menu_callback)
        dpg.add_text(f"Length: {len(dpg.get_item_configuration('combo_list')['items'])}", tag="debug_text")
        dpg.add_button(label="refresh", callback=lambda: dpg.set_value("debug_text", len(dpg.get_item_configuration("combo_list")["items"])))

    dpg.create_viewport(title='ComboEdit', width=600, height=400)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()