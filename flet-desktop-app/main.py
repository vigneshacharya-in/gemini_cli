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
            # alignment=ft.MainAxisAlignment.START,
            # Conditionally set the alignment for the timestamp
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
        
        # Theme-specific colors for recent chat items
        if page.theme_mode == ft.ThemeMode.LIGHT:
            if is_selected:
                # Light theme selected: primary background with purple border
                self.bgcolor = "#E7DDFF"
                self.border = ft.border.all(1, "purple")
                text_color = "black"
                time_color = "grey600"
            else:
                # Light theme unselected: light grey background, no border
                # self.bgcolor = "grey100"
                self.border = None
                text_color = "black"
                time_color = "grey600"
        else:
            if is_selected:
                # Dark theme selected: primary background with purple border
                self.bgcolor = "#403847"
                self.border = ft.border.all(1, "purple")
                text_color = "white"
                time_color = "grey400"
            else:
                # Dark theme unselected: dark grey background, no border
                # self.bgcolor = "grey900"
                self.border = None
                text_color = "white"
                time_color = "grey400"
            
        self.content = ft.Column(
            [
                ft.Text(chat_name, weight="bold", color=text_color),
                ft.Text(last_message_time, size=10, color=time_color),
            ]
        )

def main(page: ft.Page):
    page.title = "AI Chat"
    page.window_icon = "assets/radgeni-tooltip.png"
    page.theme_mode = ft.ThemeMode.LIGHT

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

    # Create separate theme buttons for collapsed and expanded sidebars
    theme_button_collapsed = ft.IconButton(
        icon="wb_sunny_outlined" if page.theme_mode == ft.ThemeMode.DARK else "dark_mode_outlined"
    )
    
    theme_button_expanded = ft.IconButton(
        icon="wb_sunny_outlined" if page.theme_mode == ft.ThemeMode.DARK else "dark_mode_outlined"
    )

    def change_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        
        # Update both theme buttons
        new_icon = "wb_sunny_outlined" if page.theme_mode == ft.ThemeMode.DARK else "dark_mode_outlined"
        theme_button_collapsed.icon = new_icon
        theme_button_expanded.icon = new_icon
        
        # Recreate the expanded sidebar with updated theme colors
        update_sidebar_colors()
        
        page.update()

    def update_sidebar_colors():
        # Clear and recreate the ListView with updated theme colors
        expanded_sidebar.content.controls[3] = ft.ListView(
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
        )

    # Assign the same click handler to both buttons
    theme_button_collapsed.on_click = change_theme
    theme_button_expanded.on_click = change_theme

    def toggle_sidebar(e):
        expanded_sidebar.visible = not expanded_sidebar.visible
        collapsed_sidebar.visible = not collapsed_sidebar.visible
        page.update()

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
    new_message = ft.TextField(hint_text="Start typing a prompt...", expand=True, border_radius=10)
    send_button = ft.IconButton("send", on_click=send_message, icon_color="purple")

    # Main content
    chat_view = ft.Column(
        expand=True,
        controls=[
            chat_messages,
            ft.Row(
                controls=[
                    new_message,
                    send_button,
                ]
            )
        ],
    )

    # Collapsed Sidebar
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
                ft.Container(expand=True), # Spacer
                theme_button_collapsed, # Use separate theme button for collapsed sidebar
            ],
            alignment=ft.MainAxisAlignment.START,
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
                        theme_button_expanded, # Use separate theme button for expanded sidebar
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