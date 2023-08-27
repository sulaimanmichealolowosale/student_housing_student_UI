from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
import requests
import threading
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.app import MDApp
from kivymd.toast import toast


Builder.load_string('''

<Register>:
    orientation: "vertical"
    md_bg_color:1,1,1,1
    MDScrollView:
        id:scroll
        effect_cls: "ScrollEffect"
        MDBoxLayout:
            id:main_box
            orientation: 'vertical'
            pos_hint:{"center_y":.5}
            spacing: '20dp'
            padding: ('10dp', '20dp', '10dp', '10dp')
            size_hint_y:None
            height:self.minimum_height

            MDTextField:
                id:first_name
                text:"Sulaiman"
                hint_text:"Firstname"
                hint_text_color_normal:"red"
                helper_text: "John"
                helper_text_mode: "persistent"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
            MDTextField:
                id:last_name
                text:"Micheal"
                hint_text:"Firstname"
                hint_text_color_normal:"red"
                helper_text: "Doe"
                helper_text_mode: "persistent"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
            MDTextField:
                id:nick_name
                text:"mickey"
                hint_text:"Nickname"
                hint_text_color_normal:"red"
                helper_text: "jonny"
                helper_text_mode: "persistent"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
            MDTextField:
                id:email
                text:"admin@admin.com"
                hint_text:"Email"
                hint_text_color_normal:"red"
                helper_text: "someone@something.com"
                helper_text_mode: "persistent"
                validator:"email"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5, "center_y":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
            MDTextField:
                id:phone
                text:"09056435678"
                hint_text:"Phone Number"
                hint_text_color_normal:"red"
                helper_text: "09056435678"
                helper_text_mode: "persistent"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5, "center_y":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
                on_text: root.on_phone()
        
            MDTextField:
                id:password
                text:"sulaiman"
                hint_text:"Password"
                hint_text_color_normal:"green" if self.text == password_conf.text else "red"
                hint_text:"Password"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                password:True
                multiline:False
            MDTextField:
                id:password_conf
                hint_text:"Confirm password"
                hint_text_color_normal:"green" if password.text == self.text else "red"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                password:True
                multiline:False
            MDRectangleFlatIconButton:
                text:"ADD NEW USER"
                icon:"database-plus-outline"
                size_hint_x:1
                on_release: 
                    root.register()

            MDBoxLayout:
                size_hint: 1, None
                height:self.minimum_height
                orientation: 'horizontal'
                pos_hint: {'center_x': .5, 'y':.3 }
                MDLabel:
                    text: "Aready registered?"
                    size_hint:.5, None
                    height: dp(10)
                    halign:"right"
                    pos_hint: {'center_y':.5 }
                    # color:
                MDTextButton:
                    text: ' login here'
                    size_hint:.5, None
                    pos_hint: {'center_y':.5 }
                    theme_text_color:"Custom"
                    text_color:rgba(0, 128, 128, 255)
                    on_release: root.parent.current="auth"

        
''')

BASE_URL = "http://192.168.0.101:8000"
IMAGE_BASE_URL = "http://192.168.0.101:8000"


class Register(MDScreen, MDBoxLayout):
    spinner_state = BooleanProperty(False)
    error_text = StringProperty()
    name = "register"
    profile_image = StringProperty()

    def on_leave(self, *args):
        phone = self.ids.phone
        phone.disabled = False


    def on_phone(self):
        phone = self.ids.phone

        if len(phone.text) == 1:
            self.on_register_message(
                message="Phone number field will be disabled once it gets to the maximum. Plesae verify",
                background_color=(1, 0, 0, .7)
            )
        elif len(phone.text) > 10:
            phone.disabled = True

    def register(self):
        t = threading.Thread(target=self._register)
        t.start()

    def on_register(self):
        self.ids.first_name.text = ""
        self.ids.last_name.text = ""
        self.ids.nick_name.text = ""
        self.ids.email.text = ""
        self.ids.phone.text = ""
        self.ids.password.text = ""
        self.ids.password_conf.text = ""
        self.parent.current = "auth"

    def on_register_message(self, message, background_color):
        toast(message, duration=5, background=background_color)

    def _register(self):
        try:

            data = {
                "first_name": self.ids.first_name.text,
                "last_name": self.ids.last_name.text,
                "nick_name": self.ids.nick_name.text,
                "email": self.ids.email.text,
                "phone": self.ids.phone.text,
                "password": self.ids.password.text,
            }

            if data['email'] == "" or data['first_name'] == "" or data["last_name"] == "" or data["nick_name"] == "" or data['password'] == "" or data['phone'] == "":
                Clock.schedule_once(lambda x: self.on_register_message(
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
                response = requests.post(
                    url=f"{self.base_url}/user",
                    headers={
                        'Content-Type': 'application/json',
                    },
                    json=data
                )

                if response.ok:
                    Clock.schedule_once(lambda x: self.on_register())

                elif response.status_code == 409:
                    Clock.schedule_once(lambda x: self.on_register_message(
                        message="Email already exist",
                        background_color=(1, 0, 0, .7)
                    ))

                elif response.status_code == 422:
                    Clock.schedule_once(lambda x: self.on_register_message(
                        message="Make sure no field is empty",
                        background_color=(1, 0, 0, .7)
                    ))

        except Exception as e:
            print(e)
