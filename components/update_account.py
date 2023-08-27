from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, ListProperty
from kivy.clock import Clock

import requests
import threading
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton
from kivymd.toast import toast


Builder.load_string('''

<DefaultTextField@MDTextField>:
    helper_text_color_focus:"white"
    helper_text_color_normal:"white"
    text_color_normal:1 , 1 , 1 , 1
    text_color_focus:1 , 1 , 1 , 1

<UpdateUser>:
    orientation: "vertical"
                    
    MDTopAppBar:
        pos_hint: {'top':1 }
        left_action_items: [["arrow-left", lambda x: root.back()]]
        title:"Update Details"

    MDScrollView:
        id:scroll
        effect_cls: "ScrollEffect"
        size_hint: 1, .9
        MDBoxLayout:
            id:main_box
            orientation: 'vertical'
            size_hint: 1, .9
            pos_hint:{"center_y":.5}
            spacing: '20dp'
            padding: ('10dp', '20dp', '10dp', '10dp')
            size_hint_y:None
            height:self.minimum_height

            DefaultTextField:
                id:first_name
                text:root.first_name
                hint_text:"Firstname"
                hint_text_color_normal:"white"
                helper_text: "John"
                helper_text_mode: "persistent"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
            DefaultTextField:
                id:last_name
                text:root.last_name
                hint_text:"Lastname"
                hint_text_color_normal:"white"
                helper_text: "Doe"
                helper_text_mode: "persistent"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
            DefaultTextField:
                id:nick_name
                text:root.nick_name
                hint_text:"Nickname"
                hint_text_color_normal:"white"
                helper_text: "jonny"
                helper_text_mode: "persistent"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
            DefaultTextField:
                id:email
                text:root.email
                hint_text:"Email"
                hint_text_color_normal:"white"
                helper_text: "someone@something.com"
                helper_text_mode: "persistent"
                validator:"email"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5, "center_y":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
            DefaultTextField:
                id:phone
                text:root.phone
                hint_text:"Phone Number"
                hint_text_color_normal:"white"
                helper_text: "09056435678"
                helper_text_mode: "persistent"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5, "center_y":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False

            DefaultTextField:
                id:password
                hint_text:"Password"
                hint_text_color_normal:"white"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                password:True
                multiline:False

            DefaultTextField:
                id:password_conf
                hint_text:"Confirm password"
                hint_text_color_normal:"white" if password.text == self.text else "red"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                password:True
                multiline:False

            MDRectangleFlatIconButton:
                text:"UPDATE USER"
                icon:"database-plus-outline"
                size_hint_x:1
                text_color: 1 , 1 , 1 , 1
                line_color: 1 , 1 , 1 , 1
                icon_color: 1 , 1 , 1 , 1
                on_release: 
                    root.update()
        

''')


class UpdateUser(MDScreen, MDBoxLayout):
    name = "update_user"
    first_name = StringProperty()
    last_name = StringProperty()
    nick_name = StringProperty()
    from_screen = StringProperty()
    email = StringProperty()
    phone = StringProperty()
    access_token = StringProperty()
    base_url = StringProperty()
    image_base_url = StringProperty()
    user_id: int
    id = StringProperty()
    message = StringProperty()
    message_color = (1, 1, 0, .7)


    def back(self):
        self.parent.current = "account"

    
    def get_details(self):
        t = threading.Thread(target=self._get_details)
        t.start()

    def on_get_details(self, res):
        self.first_name = res['first_name']
        self.last_name = res['last_name']
        self.email = res['email']
        self.phone = res['phone']
        self.nick_name = res['nick_name']

    def _get_details(self):
        try:
            response = requests.get(
                url=f"{self.base_url}/user/{self.id}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                },
            )

            res = response.json()
            Clock.schedule_once(lambda x: self.on_get_details(res))
        except Exception as e:
            print(e)

    def on_enter(self):
        self.get_details()

    def update(self):
        t = threading.Thread(target=self._update)
        t.start()

    def on_update(self):
        self.ids.first_name.text = ""
        self.ids.last_name.text = ""
        self.ids.nick_name.text = ""
        self.ids.email.text = ""
        self.ids.phone.text = ""
        self.ids.password.text = ""
        self.parent.current = "account"

    def on_update_message(self, message, background_color):
        toast(message, duration=5, background=background_color)

    def _update(self):
        try:

            data = {
                "first_name": self.ids.first_name.text,
                "last_name": self.ids.last_name.text,
                "nick_name": self.ids.nick_name.text,
                "email": self.ids.email.text,
                "phone": self.ids.phone.text,
                "password": self.ids.password.text,
            }

            if data['email'] == "" or data['phone'] == "" or data['first_name'] == "" or data["last_name"] == "" or data["nick_name"] == "" or data['password'] == "":
                Clock.schedule_once(lambda x: self.on_update_message(
                    message="Make sure no field is empty",
                    background_color=(1, 0, 0, .7)
                ))
                return
            elif data['password'] != self.ids.password_conf.text:
                Clock.schedule_once(lambda x: self.on_register_message(
                    message="Password Mismatch",
                    background_color=(1, 0, 0, .7)
                ))
                return
            else:
                response = requests.put(
                    url=f"{self.base_url}/user/{self.id}",
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {self.access_token}'
                    },
                    json=data
                )

                if response.ok:
                    self.message = "User added successfully"
                    self.message_color = (0, 1, 0, .7)
                    Clock.schedule_once(lambda x: self.on_update())

                elif response.status_code == 409:
                    Clock.schedule_once(lambda x: self.on_update_message(
                        message="User already exist",
                        background_color=(1, 0, 0, .7)
                    ))

                elif response.status_code == 422:
                    self.message = "Make sure no field is empty"
                    self.message_color = (1, 0, 0, .7)

        except Exception as e:
            print(e)