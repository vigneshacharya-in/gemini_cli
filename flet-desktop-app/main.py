import flet as ft
import tkinter as tk
import time
import pathlib

class ChatMessage(ft.Row):
    def __init__(self, message: str, user: str, timestamp: str, page: ft.Page):
        super().__init__()
        self.vertical_alignment = "start"
        
        message_column = ft.Column(
            [
                ft.Container(
                    ft.Text(message, color=page.theme.color_scheme.on_primary if user == "You" else page.theme.color_scheme.on_primary_container),
                    bgcolor=page.theme.color_scheme.primary if user == "You" else page.theme.color_scheme.primary_container,
                    padding=10,
                    border_radius=10,
                ),
                ft.Text(timestamp, size=8, color="grey"),
            ],
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.END if user == "You" else ft.CrossAxisAlignment.START,
        )

        avatar = ft.CircleAvatar(
            content=ft.Icon("person_rounded" if user == "You" else "auto_awesome", size=10),
            color=page.theme.color_scheme.on_primary if user == "You" else page.theme.color_scheme.on_primary_container,
            bgcolor=page.theme.color_scheme.primary if user == "You" else page.theme.color_scheme.primary_container,
            radius=12,
        )

        if user == "You":
            self.controls = [message_column, avatar]
            self.alignment = ft.MainAxisAlignment.END
        else:
            self.controls = [avatar, message_column]
            self.alignment = ft.MainAxisAlignment.START

class RecentChatItem(ft.Container):
    def __init__(self, chat_name: str, last_message_time: str, is_selected: bool, page: ft.Page):
        super().__init__()
        self.padding = 10
        self.border_radius = 10
        
        if page.theme_mode == ft.ThemeMode.LIGHT:
            if is_selected:
                self.bgcolor = "#E7DDFF"
                self.border = ft.border.all(1, "purple")
                text_color = "black"
                time_color = "grey600"
            else:
                self.border = None
                text_color = "black"
                time_color = "grey600"
        else:
            if is_selected:
                self.bgcolor = "#553B6C"
                self.border = ft.border.all(1, "purple")
                text_color = "white"
                time_color = "grey400"
            else:
                self.border = None
                text_color = "white"
                time_color = "grey400"
            
        self.content = ft.Column(
            [
                ft.Text(chat_name, weight="bold", color=text_color),
                ft.Text(last_message_time, size=10, color=time_color),
            ]
        )

script_dir = pathlib.Path(__file__).parent 
# Construct the full, absolute path to your icon
icon_path = str(script_dir / "assets" / "icon.ico")

def main(page: ft.Page):
    page.title = "AI Chat"
    page.window_icon = "icon.ico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.update()

    # Theme settings
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="purple",
            on_primary="white",
            primary_container="purple100",
            on_primary_container="black",
            surface="white",
            on_surface="black",
            on_surface_variant="grey",
        )
    )
    page.dark_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="purple",
            on_primary="white",
            primary_container="purple900",
            on_primary_container="white",
            surface="grey800",
            on_surface="white",
            on_surface_variant="grey",
        )
    )

    # State for RAG toggle
    is_rag_enabled = True # Start with enabled state
    
    # --- ALL APP FUNCTIONS DEFINED FIRST ---

    def update_sidebar_colors():
        expanded_sidebar.content.controls[3] = ft.ListView(
            [
                RecentChatItem("Welcome Chat", "Today", True, page),
                RecentChatItem("Chat 2", "Yesterday", False, page),
                RecentChatItem("Chat 3", "2 days ago", False, page),
            ],
            expand=True,
        )

    def update_rag_button_style():
        nonlocal is_rag_enabled
        if is_rag_enabled:
            rag_button_icon.name = "flash_on"
            rag_button_text.value = "RAG Enabled"
            rag_description.visible = True
            if page.theme_mode == ft.ThemeMode.DARK:
                rag_button.bgcolor = "#3a2d4f"
                rag_button.border = ft.border.all(1, "#6d5291")
                rag_button_icon.color = "white"
                rag_button_text.color = "white"
                rag_description.color = "#ad99cc"
            else:
                rag_button.bgcolor = "#E7DDFF"
                rag_button.border = ft.border.all(1, "purple")
                rag_button_icon.color = "black"
                rag_button_text.color = "black"
                rag_description.color = "purple"
        else:
            rag_button_icon.name = "flash_off"
            rag_button_text.value = "RAG Disabled"
            rag_description.visible = False
            rag_button.bgcolor = None
            if page.theme_mode == ft.ThemeMode.DARK:
                rag_button.border = ft.border.all(1, "grey600")
                rag_button_icon.color = "white"
                rag_button_text.color = "white"
            else:
                rag_button.border = ft.border.all(1, "grey400")
                rag_button_icon.color = "black"
                rag_button_text.color = "black"

    def toggle_rag(e):
        nonlocal is_rag_enabled
        is_rag_enabled = not is_rag_enabled
        update_rag_button_style()
        page.update()

    def change_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        
        new_icon = "wb_sunny_outlined" if page.theme_mode == ft.ThemeMode.DARK else "dark_mode_outlined"
        theme_button_collapsed.icon = new_icon
        theme_button_expanded.icon = new_icon
        theme_text.value = "Light Mode" if page.theme_mode == ft.ThemeMode.DARK else "Dark Mode"
        new_message.border_color = "grey700" if page.theme_mode == ft.ThemeMode.DARK else "grey400"
        
        update_sidebar_colors()
        update_rag_button_style()
        page.update()

    def toggle_sidebar(e):
        expanded_sidebar.visible = not expanded_sidebar.visible
        collapsed_sidebar.visible = not collapsed_sidebar.visible
        page.update()

    def send_message(e):
        if new_message.value != "":
            chat_messages.controls.append(ChatMessage(new_message.value, "You", time.strftime("%I:%M %p"), page))
            new_message.value = ""
            page.update()

    # --- ALL UI CONTROLS DEFINED HERE ---

    theme_button_collapsed = ft.IconButton(
        icon="wb_sunny_outlined" if page.theme_mode == ft.ThemeMode.DARK else "dark_mode_outlined",
        on_click=change_theme
    )
    
    theme_button_expanded = ft.IconButton(
        icon="wb_sunny_outlined" if page.theme_mode == ft.ThemeMode.DARK else "dark_mode_outlined"
    )

    theme_text = ft.Text(
        "Dark Mode" if page.theme_mode == ft.ThemeMode.LIGHT else "Light Mode",
        color="purple",
        weight="bold"
    )

    theme_switcher = ft.Container(
        content=ft.Row([theme_button_expanded, theme_text], spacing=10),
        on_click=change_theme,
        padding=ft.padding.symmetric(horizontal=10, vertical=5),
        border_radius=10,
        ink=True,
    )

    page.appbar = ft.AppBar(
        leading=ft.IconButton("menu", on_click=toggle_sidebar),
        title=ft.Text("AI Chat"),
        center_title=False,
        actions=[],
        bgcolor="surfacevariant",
    )

    chat_messages = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    new_message = ft.TextField(hint_text="Start typing a prompt...", expand=True, border_color="grey400")
    send_button = ft.IconButton("send", on_click=send_message, icon_color="purple")

    # RAG Toggle Components
    rag_button_icon = ft.Icon(size=16)
    rag_button_text = ft.Text(size=12, weight="bold")
    rag_description = ft.Text("Enhanced responses with context retrieval", size=12, italic=True)

    rag_button = ft.Container(
        content=ft.Row([rag_button_icon, rag_button_text], tight=True, spacing=5),
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        border_radius=20,
        on_click=toggle_rag,
    )

    rag_toggle_row = ft.Row(
        controls=[
            rag_button,
            ft.Container(rag_description, margin=ft.margin.only(left=10)),
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    chat_view = ft.Column(
        expand=True,
        controls=[
            chat_messages,
            ft.Container(rag_toggle_row, padding=ft.padding.only(left=5, bottom=5)),
            ft.Row(controls=[new_message, send_button])
        ],
    )

    collapsed_sidebar = ft.Container(
        width=50,
        content=ft.Column(
            [
                ft.Container(
                    content=ft.IconButton(icon="add", icon_color="white"),
                    bgcolor="purple",
                    width=40,
                    height=40,
                    border_radius=10,
                    alignment=ft.alignment.center,
                ),
                ft.Container(expand=True),
                theme_button_collapsed,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    expanded_sidebar = ft.Container(
        width=250,
        padding=10,
        visible=False,
        content=ft.Column(
            spacing=10,
            controls=[
                ft.FilledButton(
                    content=ft.Row([ft.Icon("add"), ft.Text("New Chat")], alignment=ft.MainAxisAlignment.CENTER),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                ),
                ft.Divider(),
                ft.Text("Recent", weight="bold"),
                ft.ListView(
                    [
                        RecentChatItem("Welcome Chat", "Today", True, page),
                        RecentChatItem("Chat 2", "Yesterday", False, page),
                        RecentChatItem("Chat 3", "2 days ago", False, page),
                    ],
                    expand=True,
                ),
                ft.Divider(),
                ft.Row(
                    [
                        theme_switcher,
                        # ft.IconButton(icon="settings", on_click=lambda e: print("Settings"))
                    ],
                )
            ],
        ),
    )
    
    # --- FINAL LAYOUT AND APP START ---

    # Set initial style for the RAG button on startup
    update_rag_button_style()

    # Load previous chats
    chat_messages.controls.append(ChatMessage("Hello! How can I assist you today?", "Bot", "04:50 PM", page))
    chat_messages.controls.append(ChatMessage("I'm a demo AI assistant.", "Bot", "04:50 PM", page))
    chat_messages.controls.append(ChatMessage("Great, can you tell me more about Flet?", "You", "04:51 PM", page))

    main_layout = ft.Row(
        expand=True,
        controls=[
            collapsed_sidebar,
            expanded_sidebar,
            ft.VerticalDivider(width=1),
            chat_view,
        ],
    )

    page.add(main_layout)

ft.app(target=main, assets_dir="assets")