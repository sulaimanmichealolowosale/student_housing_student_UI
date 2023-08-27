from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, ListProperty
import requests
import threading
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.app import MDApp
from kivymd.uix.swiper import MDSwiperItem
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.label import MDLabel
from kivy.core.clipboard import Clipboard
from components.image_modal import ImageModal
import webbrowser


Builder.load_string('''

<AgentDetails>:

    orientation: 'vertical'

    MDTopAppBar:
        pos_hint: {'top':1 }
        left_action_items: [["arrow-left", lambda x: root.back()]]

    MDScrollView:
        effect_cls: "ScrollEffect"
        size_hint: 1, .9
        scroll_y:1

        MDBoxLayout:
            id:main_box
            orientation: 'vertical'
            spacing: '40dp'
            padding: ('10dp', '20dp', '10dp', '10dp')
            size_hint_y:None
            size:(root.width, root.height)
            height:self.minimum_height

            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height:self.minimum_height
                md_bg_color:[1,1,1,1]
                padding: ('10dp', '20dp', '10dp', '10dp')
                spacing: '30dp'
                radius:[10,]

                MDSmartTile:
                    source:root.agent_image_url
                    pos_hint: {'center_x': .5 }
                    size_hint:None, None
                    size: '170dp','170dp'
                    mipmap:True
                    allow_stretch: False
                    box_color:[0,0,0,0]
                    radius: [100]
                    on_release: root.open_modal(self)

                TextLabel:
                    text: "Name: "+root.agent_name
                    bold:True
                TextLabel:
                    text: "Email: "+root.agent_email
                    bold:True
                TextLabel:
                    text: "Nick Name: "+root.agent_nick_name
                    bold:True

                MDTextButton:
                    text: "Phone: "+root.agent_phone
                    size_hint_x: 1
                    on_release: root.call()
                
            MDLabel:
                text: 'Properties'
                font_style:"H4"
                halign:"center"
                color: 1 , 1 , 1 , 1

            GridLayout:
                cols:2
                id:user_grid
                spacing: '10dp'
                size_hint_y: None
                height:self.minimum_height


    MDSpinner:
        active:root.spinner_state
        size_hint:None, None
        height: dp(50)
        width: dp(50)
        pos_hint:{'center_x': .5, 'center_y': .5}


    ''')


class AgentDetails(MDScreen, MDBoxLayout):
    name = "agentdetails"
    base_url = StringProperty()
    image_base_url = StringProperty()
    property_list = ListProperty()
    search_text = StringProperty()
    spinner_state = BooleanProperty(True)
    agent_image_url = StringProperty()
    agent_name = StringProperty()
    agent_email = StringProperty()
    agent_nick_name = StringProperty()
    agent_phone = StringProperty()

    id: int

    def open_modal(self, instance):
        modal = ImageModal()
        modal.open_modal(instance=instance)

    def back(self):
        self.parent.current = "agent"

    def call(self):
        t = threading.Thread(target=self._call)
        t.start()

    def _call(self):
        Clipboard.copy(self.agent_phone)
        copied_phone = Clipboard.paste()
        webbrowser.open(url="tel:" + copied_phone)

    def to_single(self, instance):
        id = instance.id
        self.parent.get_screen("single").id = id
        self.parent.get_screen("single").from_screen = self.name

        self.parent.current = "single"

    def add_property(self, image, text, id):
        try:
            box = MDBoxLayout(
                padding=("10dp"),
                size_hint=(.5, None),
                height="150dp"
            )

            smart_tile = MDSmartTile(
                source=image,
                radius=[20,],
                box_radius=[0, 0, 20, 20]
            )
            setattr(smart_tile, "id", str(id))
            smart_tile.bind(on_release=self.to_single)

            label = MDLabel(
                text=text,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )

            smart_tile.add_widget(label)

            box.add_widget(smart_tile)
            return box

        except Exception as e:
            print(e)

    def on_get_agent(self, res):
        self.spinner_state = False
        user_grid = self.ids.user_grid
        for item in self.property_list:
            user_grid.add_widget(self.add_property(
                image=f"{self.image_base_url}/{item['primary_image_path']}",
                text=item['title'],
                id=item['id']
            )
            )
        self.agent_image_url = f"{self.image_base_url}/{res['image_url']}"
        self.agent_email = res['email']
        self.agent_phone = res['phone']
        self.agent_nick_name = res['nick_name']
        self.agent_name = res['first_name'] + res['last_name']

    def get_agent(self):
        t = threading.Thread(target=self._get_agent)
        t.start()

    def _get_agent(self):
        try:
            response = requests.get(
                url=f"{self.base_url}/user/{self.id}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                }
            )
            if response.ok:
                res = response.json()
                self.property_list = res['properties']
                self.spinner_state = False
                Clock.schedule_once(lambda x: self.on_get_agent(res))

        except Exception as e:
            print(e)

    def on_enter(self, *args):
        self.get_agent()

    def on_leave(self, *args):
        self.spinner_state = True
        user_grid = self.ids.user_grid
        user_grid.clear_widgets()
