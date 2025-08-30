import flet as ft
import tkinter as tk
import time

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
            alignment=ft.MainAxisAlignment.START,
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
        self.bgcolor = page.theme.color_scheme.primary_container if is_selected else page.theme.color_scheme.surface
        self.content = ft.Column(
            [
                ft.Text(chat_name, weight="bold", color=page.theme.color_scheme.on_surface),
                ft.Text(last_message_time, size=10, color=page.theme.color_scheme.on_surface_variant),
            ]
        )

def main(page: ft.Page):
    page.title = "AI Chat"
    page.theme_mode = ft.ThemeMode.DARK

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

    def change_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        theme_button.icon = "dark_mode_outlined" if page.theme_mode == ft.ThemeMode.LIGHT else "wb_sunny_outlined"
        page.update()

    def toggle_sidebar(e):
        expanded_sidebar.visible = not expanded_sidebar.visible
        collapsed_sidebar.visible = not collapsed_sidebar.visible
        page.update()

    theme_button = ft.IconButton("wb_sunny_outlined", on_click=change_theme)

    page.appbar = ft.AppBar(
        leading=ft.IconButton("menu", on_click=toggle_sidebar),
        title=ft.Text("AI Chat"),
        center_title=False,
        actions=[],
        bgcolor="surfacevariant",
    )

    # Chat messages
    chat_messages = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    def send_message(e):
        if new_message.value != "":
            chat_messages.controls.append(ChatMessage(new_message.value, "You", time.strftime("%I:%M %p"), page))
            new_message.value = ""
            page.update()

    # New message input
    new_message = ft.TextField(hint_text="Test", expand=True, border_radius=10)
    send_button = ft.IconButton("send", on_click=send_message, icon_color="purple")
    attachment_button = ft.IconButton("attach_file", icon_color="grey")

    # Main content
    chat_view = ft.Column(
        expand=True,
        controls=[
            chat_messages,
            ft.Row(
                controls=[
                    attachment_button,
                    new_message,
                    send_button,
                ]
            )
        ],
    )

    # Collapsed Sidebar
    collapsed_sidebar = ft.Container(
        width=50,
        border=ft.border.all(1, "grey200"),
        border_radius=10,
        content=ft.Column(
            [
                ft.IconButton(icon="arrow_right", on_click=toggle_sidebar),
                ft.IconButton(icon="add", on_click=lambda e: print("New Chat"))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # Expanded Sidebar
    expanded_sidebar = ft.Container(
        width=250, # Increased width to accommodate content
        padding=10,
        content=ft.Column(
            [
                ft.FilledButton(
                    content=ft.Row([ft.Icon("add"), ft.Text("New Chat")], alignment=ft.MainAxisAlignment.CENTER),
                    on_click=lambda e: print("New Chat"),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                ),
                ft.Divider(),
                ft.Text("Recent", weight="bold"),
                ft.ListView(
                    [
                        RecentChatItem("Welcome Chat", "Today", True, page),
                        RecentChatItem("Chat 2", "Yesterday", False, page),
                        RecentChatItem("Chat 3", "2 days ago", False, page),
                        RecentChatItem("Chat 4", "3 days ago", False, page),
                        RecentChatItem("Chat 5", "4 days ago", False, page),
                        RecentChatItem("Chat 6", "5 days ago", False, page),
                        RecentChatItem("Chat 7", "6 days ago", False, page),
                        RecentChatItem("Chat 8", "1 week ago", False, page),
                        RecentChatItem("Chat 9", "1 week ago", False, page),
                        RecentChatItem("Chat 10", "1 week ago", False, page),
                        RecentChatItem("Chat 11", "2 weeks ago", False, page),
                        RecentChatItem("Chat 12", "2 weeks ago", False, page),
                    ],
                    expand=True,
                ),
                ft.Divider(),
                ft.Row(
                    [
                        ft.IconButton(icon="dark_mode_outlined", on_click=change_theme),
                        ft.IconButton(icon="settings", on_click=lambda e: print("Settings"))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            ],
            spacing=10,
        ),
        visible=False,
    )

    # Load previous chats
    chat_messages.controls.append(ChatMessage("Hello! How can I assist you today?", "Bot", "04:50 PM", page))
    chat_messages.controls.append(ChatMessage("I'm a demo AI assistant. In a real implementation, this would connect to an actual AI service like OpenAI's GPT or Claude.", "Bot", "04:50 PM", page))
    chat_messages.controls.append(ChatMessage("Great, can you tell me more about Flet?", "You", "04:51 PM", page))
    chat_messages.controls.append(ChatMessage("Of course! Flet allows you to build real-time web, mobile and desktop apps in Python. It has a simple component-based model and a rich set of built-in controls.", "Bot", "04:52 PM", page))
    chat_messages.controls.append(ChatMessage("That sounds interesting. I will give it a try.", "You", "04:53 PM", page))

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

ft.app(target=main)