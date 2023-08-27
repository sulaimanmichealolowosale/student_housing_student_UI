from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.clock import Clock

import requests
import threading
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivy.config import platform
from kivymd.app import MDApp
import os

Builder.load_string('''
<DefaultLabel@MDLabel>:
    font_style:"H6"

<Account>:
    orientation: "vertical"


    MDBoxLayout:
        id:main_box
        orientation: 'vertical'
        size_hint: 1, .9
        spacing: '20dp'
        padding: ('10dp', '20dp', '10dp', '10dp')

        MDBoxLayout:
            # md_bg_color:rgba(26, 62, 255, 255)
            id:image_box
            size_hint:None, None
            size: '170dp','170dp'
            pos_hint: {'center_x': .5 }
            FitImage:
                source:root.image_url
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                size_hint: 1, 1
                mipmap:True
                allow_stretch: False
                radius: [100]

        MDBoxLayout:
            orientation: 'vertical'
            spacing: '25dp'
            size_hint:1, None
            height:self.minimum_height
            # height: dp(70)

            MDRectangleFlatIconButton:
                icon:"update"
                text: 'Change Picture'
                pos_hint: {'center_x': .5 }
                # font_size:"15dp"
                icon_color:1,1,1,1
                text_color:1,1,1,1
                line_color:1,1,1,1
                on_release: root.choose_file()

            MDLabel:
                text:root.full_name
                halign:"center"
                font_style:"H6"
                color: 1 , 1 , 1 , 1
            MDLabel:
                text:root.email
                halign:"center"
                font_style:"Subtitle1"
                color: 1 , 1 , 1 , 1
            MDLabel:
                text:root.nick_name
                halign:"center"
                font_style:"Subtitle2"
                color: 1 , 1 , 1 , 1
            MDLabel:
                text:root.phone
                halign:"center"
                font_style:"Subtitle2"
                color: 1 , 1 , 1 , 1

        MDBoxLayout:
            size_hint:1, .2
            spacing: '20dp'
            orientation: 'horizontal'

            MDRectangleFlatIconButton:
                icon: "update"
                text: 'Update details'
                size_hint_x:.5
                icon_color: 1 , 1 , 0 , 1
                text_color:1 , 1 , 0 , 1
                line_color:1 , 1 , 0 , 1
                on_release: root.to_update()

            MDRectangleFlatIconButton:
                icon:"delete-outline"
                text: 'Delete Profile'
                size_hint_x: .5
                icon_color: 1 , 0 , 0 , 1
                text_color:1 , 0 , 0 , 1
                line_color:1 , 0 , 0 , 1
                on_release: root.delete_user()

    
    ''')


class Account(MDScreen, MDBoxLayout):
    name = "account"
    first_name = StringProperty()
    last_name = StringProperty()
    nick_name = StringProperty()
    access_token = StringProperty()
    role = StringProperty()
    selectet_user_role = StringProperty()
    email = StringProperty()
    phone = StringProperty()
    user_id: int
    base_url = StringProperty()
    image_base_url = StringProperty()
    image_url = StringProperty()
    full_name = StringProperty()
    file_manager = ObjectProperty()
    file_path = StringProperty()
    dialog = ObjectProperty()


    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Upload Image?",
                buttons=[
                    MDFlatButton(
                        text="YES",
                        on_release=self.submit_image
                    ),
                    MDFlatButton(
                        text="NO",
                        on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()

    def select_path(self, path: str):
        try:
            self.file_path = path
            self.exit_manager()
            self.show_alert_dialog()
        except Exception as e:
            pass

    def exit_manager(self, *args):
        self.file_manager.close()

    def choose_file(self):
        # self.select_pic_state = not self.select_pic_state
        try:
            self.file_manager = MDFileManager(
                exit_manager=self.exit_manager,
                select_path=self.select_path,
                icon_selection_button="",
                background_color_selection_button=(0, 0, 0, 0),
                preview=True,
                ext=['.png', '.jpg', '.jpeg', '.gif'],
            )
            file_manager_path = ""
            if platform == 'android':
                from android.permissions import request_permissions, Permission
                from android.storage import primary_external_storage_path
                request_permissions(
                    [
                        Permission.READ_EXTERNAL_STORAGE,
                        Permission.WRITE_EXTERNAL_STORAGE
                    ]

                )

                file_manager_path = primary_external_storage_path()
            else:
                file_manager_path = os.path.expanduser("~")

            self.file_manager.show(file_manager_path)
        except:
            pass

    def _on_image_submit(self, response):
        self.image_url = f"{self.image_base_url}/{response.json()['image_url']}"
        app = MDApp.get_running_app()
        picture = app.root.ids.profile_picture
        picture.source = f"{self.image_base_url}/{response.json()['image_url']}"

    def submit_image(self, instance):
        t = threading.Thread(target=self._submit_image)
        t.start()

    def _submit_image(self):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        try:
            file = open(self.file_path, "rb")
            response = requests.put(
                self.base_url+f"/user/update-profile-picture/{self.user_id}",
                headers=headers,
                files={"file": file}
            )

            if response.ok:
                self.dialog.dismiss()

            Clock.schedule_once(lambda dt: self._on_image_submit(response))
        except Exception as e:
            print(e)

    def to_update(self):
        self.parent.get_screen("update_user").id = str(self.user_id)
        self.parent.current = "update_user"

    def on_message(self, message, background_color):
        toast(message, duration=5, background=background_color)

    def on_get_user(self, res):
        self.image_url = f"{self.image_base_url}/{res['image_url']}"
        self.full_name = f"{res['first_name']} {res['last_name']}"
        self.nick_name = res['nick_name']
        self.category_count = str(len(res['categories']))
        self.property_count = str(len(res['properties']))
        self.rating = str(res['rating'])
        self.selectet_user_role = res['role']
        self.email = res['email']
        self.phone = res['phone']

    def _get_user(self):
        try:
            response = requests.get(
                url=f"{self.base_url}/user/{self.user_id}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                },
            )

            if response.ok:
                res = response.json()
                Clock.schedule_once(lambda x: self.on_get_user(res))
        except Exception as e:
            print(e)

    def get_user(self):
        t = threading.Thread(target=self._get_user)
        t.start()

    def _delete_user(self):
        try:
            response = requests.delete(
                url=f"{self.base_url}/user/{self.id}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                },
            )

            Clock.schedule_once(lambda x: self.on_delete())
        except Exception as e:
            return

    def delete_user(self):
        t = threading.Thread(target=self._delete_user)
        t.start()

    def on_delete(self):
        self.parent.current = "login"

    def on_enter(self):
        self.get_user()