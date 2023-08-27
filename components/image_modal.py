from kivy.uix.modalview import ModalView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class ImageModal(Widget):
    image_modal = ObjectProperty()

    def open_modal(self, instance):
        self.image_modal = ModalView(auto_dismiss=True)
        self.image_modal.background_color = (0, 0, 1, .3)
        parent_box = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, 1),
            spacing=20,
            padding=10,
        )
        close_button = MDIconButton(
            icon="close",
            theme_text_color="Custom",
            icon_color=(1, 0, 0, 1),
        )
        image_box = MDBoxLayout(
            size_hint=(1, .9),
            padding=5,
        )

        image = AsyncImage(
            source=instance.source,

        )

        image_box.add_widget(image)

        close_button.bind(on_release=self.close_modal)
        parent_box.add_widget(close_button)
        parent_box.add_widget(image_box)
        self.image_modal.add_widget(parent_box)
        self.image_modal.open()

    def close_modal(self, instance):
        self.image_modal.dismiss()
