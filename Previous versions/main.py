import flet as ft
import tkinter as tk

def main(page: ft.Page):
    page.title = "RADgeni Mario"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Get screen dimensions
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    page.window_width = screen_width
    page.window_height = screen_height
    page.window_top = 0
    page.window_left = 0

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    def change_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        theme_button.icon = "dark_mode_outlined" if page.theme_mode == ft.ThemeMode.LIGHT else "wb_sunny_outlined"
        page.update()

    def toggle_sidebar(e):
        sidebar.visible = not sidebar.visible
        page.update()

    theme_button = ft.IconButton("dark_mode_outlined", on_click=change_theme)

    page.appbar = ft.AppBar(
        leading=ft.IconButton("menu", on_click=toggle_sidebar),
        leading_width=40,
        title=ft.Text("RADgeni Mario"),
        center_title=False,
        bgcolor="purple",
        actions=[
            theme_button,
        ],
    )

    # Chat messages
    chat_messages = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    # Load previous chats
    chat_messages.controls.append(ft.Text("Bot: Hello! How can I help you today?"))
    chat_messages.controls.append(ft.Text("You: What is Flet?"))
    chat_messages.controls.append(ft.Text("Bot: Flet is a framework for building interactive multi-user web, desktop and mobile applications in Python."))


    def send_message(e):
        if new_message.value != "":
            chat_messages.controls.append(ft.Text(f"You: {new_message.value}"))
            new_message.value = ""
            page.update()

    # New message input
    new_message = ft.TextField(hint_text="Type a message...", expand=True)
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

    # Sidebar
    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        leading=ft.FloatingActionButton(icon="create", text="New Chat"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon="chat_bubble_outline",
                selected_icon="chat_bubble",
                label="Chat 1",
            ),
            ft.NavigationRailDestination(
                icon="chat_bubble_outline",
                selected_icon="chat_bubble",
                label="Chat 2",
            ),
        ],
        on_change=lambda e: print(f"Selected: {e.control.selected_index}"),
        visible=True,
    )

    # Main layout
    main_layout = ft.Row(
        expand=True,
        controls=[
            sidebar,
            ft.VerticalDivider(width=1),
            chat_view,
        ],
    )

    page.add(main_layout)

ft.app(target=main)