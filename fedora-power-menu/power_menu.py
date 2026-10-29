#!/usr/bin/env python3
"""GTK 4 power menu for Fedora."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Final

from gi.repository import Adw, Gio, Gtk

APP_ID: Final = "com.example.FedoraPowerMenu"
WINDOW_TITLE: Final = "Menú de sesión"
WINDOW_SIZE: Final = (420, 300)
COMMAND_TIMEOUT_SECONDS: Final = 10


@dataclass(frozen=True)
class PowerAction:
    title: str
    description: str
    icon_name: str
    command: tuple[str, ...]


ACTIONS: Final = (
    PowerAction(
        title="Apagar",
        description="Apaga el equipo completamente.",
        icon_name="system-shutdown-symbolic",
        command=("systemctl", "poweroff"),
    ),
)


class PowerMenu(Adw.Application):
    """Application that presents a confirmable power-off action."""

    def __init__(self) -> None:
        super().__init__(
            application_id=APP_ID,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self.connect("activate", self._on_activate)

    def _on_activate(self, _application: Adw.Application) -> None:
        dialog = Gtk.Dialog(title=WINDOW_TITLE, application=self)
        dialog.set_modal(True)
        dialog.set_resizable(False)
        dialog.set_default_size(*WINDOW_SIZE)
        dialog.add_button("Cancelar", Gtk.ResponseType.CANCEL)
        dialog.connect("response", self._on_menu_response)
        dialog.get_content_area().append(self._build_menu_content())
        dialog.present()

    def _build_menu_content(self) -> Gtk.Widget:
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        content.set_margin_top(28)
        content.set_margin_bottom(28)
        content.set_margin_start(28)
        content.set_margin_end(28)

        heading = Gtk.Label(label="¿Qué quieres hacer?")
        heading.add_css_class("title-2")
        content.append(heading)

        subtitle = Gtk.Label(label="Elige una acción para tu sesión de Fedora.")
        subtitle.add_css_class("dim-label")
        content.append(subtitle)

        for action in ACTIONS:
            content.append(self._build_action_button(action))

        return content

    def _build_action_button(self, action: PowerAction) -> Gtk.Button:
        button = Gtk.Button(child=self._build_action_row(action))
        button.add_css_class("power-action")
        button.connect("clicked", self._on_action_clicked, action)
        return button

    @staticmethod
    def _build_action_row(action: PowerAction) -> Gtk.Widget:
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=14)
        row.set_margin_top(12)
        row.set_margin_bottom(12)
        row.set_margin_start(14)
        row.set_margin_end(14)

        icon = Gtk.Image.new_from_icon_name(action.icon_name)
        icon.set_pixel_size(32)
        row.append(icon)

        labels = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        labels.set_hexpand(True)

        title = Gtk.Label(label=action.title, xalign=0)
        title.add_css_class("heading")
        labels.append(title)

        description = Gtk.Label(label=action.description, xalign=0)
        description.add_css_class("dim-label")
        labels.append(description)

        row.append(labels)
        return row

    @staticmethod
    def _on_menu_response(dialog: Gtk.Dialog, _response: int) -> None:
        dialog.close()

    def _on_action_clicked(self, _button: Gtk.Button, action: PowerAction) -> None:
        parent = self.props.active_window
        if parent is not None:
            self._show_action_confirmation(parent, action)

    def _show_action_confirmation(
        self, parent: Gtk.Window, action: PowerAction
    ) -> None:
        dialog = Adw.MessageDialog(
            transient_for=parent,
            heading=f"¿{action.title}?",
            body=f"Esta acción {action.description.lower()}",
        )
        dialog.add_response("cancel", "Cancelar")
        dialog.add_response("confirm", action.title)
        dialog.set_response_appearance(
            "confirm", Adw.ResponseAppearance.DESTRUCTIVE
        )
        dialog.connect("response", self._on_confirmation_response, action)
        dialog.present()

    def _on_confirmation_response(
        self,
        _dialog: Adw.MessageDialog,
        response: str,
        action: PowerAction,
    ) -> None:
        if response != "confirm":
            return

        try:
            subprocess.run(
                action.command,
                check=True,
                timeout=COMMAND_TIMEOUT_SECONDS,
            )
        except (OSError, subprocess.SubprocessError) as error:
            self._show_error(str(error))

    def _show_error(self, message: str) -> None:
        parent = self.props.active_window
        if parent is None:
            return

        dialog = Adw.MessageDialog(
            transient_for=parent,
            heading="No se pudo ejecutar la acción",
            body=f"El sistema devolvió un error: {message}",
        )
        dialog.add_response("close", "Cerrar")
        dialog.present()


def main() -> int:
    return PowerMenu().run(None)


if __name__ == "__main__":
    raise SystemExit(main())
