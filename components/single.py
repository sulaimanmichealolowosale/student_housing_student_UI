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
from kivy.uix.image import AsyncImage
from kivymd.uix.list import ImageLeftWidget
from components.image_modal import ImageModal
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard
import webbrowser


Builder.load_string('''

<TitleLabel@MDLabel>:
    font_style:"H5"

<TextLabel@MDLabel>
    size_hint: 1, None
    height: self.texture_size[1]
    theme_text_color:"Custom"
    text_color:[.5,.5,.5,1]

<Single>:

    orientation: 'vertical'

    MDTopAppBar:
        pos_hint: {'top':1 }
        left_action_items: [["arrow-left", lambda x: root.back()]]

    MDScrollView:
        effect_cls: "ScrollEffect"
        size_hint: 1, .9
        scroll_y:1

        # pos_hint: {'top':.9 }
        
        MDBoxLayout:
            id:main_box
            orientation: 'vertical'
            spacing: '30dp'
            # padding: ('10dp', '20dp', '10dp', '10dp')
            size_hint_y:None
            size:(root.width, root.height)
            height:self.minimum_height
            padding: ('0dp', '10dp', '0dp', '150dp')
            MDLabel:
                text: root.title
                font_style:"H6"
                bold:True
                size_hint: 1, None
                height: self.texture_size[1]
                halign:"center"
                color: 1 , 1 , 1 , 1
            
            MDSmartTile:
                source:root.primary_image_path
                size_hint: 1, None
                box_color:[0,0,0,0]
                radius:[10,]
                height: dp(250)
                on_release: root.open_modal(self)

            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height:self.minimum_height
                md_bg_color:[1,1,1,1]
                padding: ('10dp', '20dp', '10dp', '10dp')
                spacing: '30dp'
                radius:[10,]
                
                TitleLabel:
                    text: "Description:"
                    
                TextLabel:
                    text: root.description   
                
                TitleLabel:
                    text: 'Address:'

                TextLabel:
                    text: root.address
                    size_hint: 1, None
                    height: self.texture_size[1]
                
                
                TitleLabel:
                    text: 'Toilet and Bathroom Description:'

                TextLabel:
                    text: root.toilet_bathroom_desc

                
                TitleLabel:
                    text: 'Kitchen Description:'

                TextLabel:
                    text: root.kitchen_desc

                
                TitleLabel:
                    text: 'Water System:'

                TextLabel:
                    text: root.water_system

                
                TitleLabel:
                    text: 'Security Type:'

                TextLabel:
                    text: root.security_type

                
                TitleLabel:
                    text: 'Listing Type:'

                TextLabel:
                    text: root.property_type

                TitleLabel:
                    text: 'Property Status:'

                MDIcon:
                    icon: "check-circle" if root.property_status == "available" else "close-circle"
                    color: [0,1,0,1] if root.property_status == "available" else [1,0,0,1]
                TitleLabel:
                    text: 'Amount:'

                TextLabel:
                    text: root.price

                TitleLabel:
                    text: 'Payment Duration:'

                TextLabel:
                    text: root.payment_duration
                
                TitleLabel:
                    text: 'Additional Fee:'

                TextLabel:
                    text: root.additional_fee

                TitleLabel:
                    text: 'Reasons for Additional Fee:'

                TextLabel:
                    text: root.reason_for_fee

            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height:self.minimum_height
                md_bg_color:[1,1,1,1]
                padding: ('10dp', '20dp', '10dp', '10dp')
                spacing: '30dp'
                radius:[10,]


                TitleLabel:
                    text: 'Agent'
                    font_style:"H4"
                    halign:"center"

                MDSmartTile:
                    source:root.agent_image_url
                    pos_hint: {'center_x': .5 }
                    size_hint:None, None
                    size: '170dp','170dp'
                    mipmap:True
                    allow_stretch: False
                    box_color:[0,0,0,0]
                    radius: [100]
                    on_release: root.to_agent_details()

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
                
                MDIconButton:
                    icon: "phone"
                    on_release: root.call()
                    theme_icon_color:"Custom"
                    icon_color:[0,1,0,1]

            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height:self.minimum_height
                md_bg_color:[1,1,1,1]
                padding: ('10dp', '20dp', '10dp', '10dp')
                radius:[10,]

                OneLineListItem:
                    text: root.category
                    on_release: root.to_property()


    Carousel:
        id:swiper
        size_hint_y: None
        height: dp(150)
        # y: root.height - self.height - dp(20)

''')


class Single(MDScreen, MDBoxLayout):
    name = "single"
    title = StringProperty()
    primary_image_path = StringProperty()
    images = ListProperty()
    base_url = StringProperty()
    image_base_url = StringProperty()
    id = StringProperty()
    description = StringProperty()
    address = StringProperty()
    security_type = StringProperty()
    water_system = StringProperty()
    toilet_bathroom_desc = StringProperty()
    kitchen_desc = StringProperty()
    property_status = StringProperty()
    property_type = StringProperty()
    price = StringProperty()
    payment_duration = StringProperty()
    additional_fee = StringProperty()
    reason_for_fee = StringProperty()
    agent_name = StringProperty()
    agent_email = StringProperty()
    agent_nick_name = StringProperty()
    agent_phone = StringProperty()
    agent_rating = StringProperty()
    agent_image_url = StringProperty()
    category = StringProperty()
    category_id = StringProperty()
    from_screen = StringProperty()
    agent_id: int

    def open_modal(self, instance):
        modal = ImageModal()
        modal.open_modal(instance=instance)

    def to_agent_details(self):
        self.parent.get_screen("agentdetails").id = self.agent_id
        self.parent.get_screen("agentdetails").from_screen = self.name

        self.parent.current = "agentdetails"

    def back(self):
        self.parent.current = "listing"

    def to_property(self):
        category = self.category
        self.parent.get_screen("by_category").cat_id = str(self.category_id)
        self.parent.get_screen("by_category").from_screen = self.name
        self.parent.get_screen("by_category").id = self.id
        self.parent.current = "by_category"

    def call(self):
        t = threading.Thread(target=self._call)
        t.start()

    def _call(self):
        Clipboard.copy(self.agent_phone)
        copied_phone = Clipboard.paste()
        webbrowser.open(url="tel:" + copied_phone)

    def get_property(self):
        t = threading.Thread(target=self._get_property)
        t.start()

    def add_swiper_item(self, image):
        try:
            swiper_item = MDBoxLayout(
                padding=dp(10),
                # size_hint=(None, None),
                # size=(dp(150), dp(150))
            )
            smart_tile = MDSmartTile(
                source=image,
                box_color=[0, 0, 0, 0],
                radius=[10,]
                # size_hint=(None, None),
                # size=(dp(150), dp(150))
            )
            smart_tile.bind(on_release=self.open_modal)
            swiper_item.add_widget(smart_tile)

            return swiper_item

        except Exception as e:
            print(e)

    def on_get_property(self, res):
        self.title = res['title']
        self.primary_image_path = f"{self.image_base_url}/{res['primary_image_path']}"
        self.description = res['description']
        self.address = res['address']
        self.toilet_bathroom_desc = res['toilet_bathroom_desc']
        self.kitchen_desc = res['kitchen_desc']
        self.security_type = res['security_type']
        self.price = f"\u20a6{res['price']}"
        self.additional_fee = f"\u20a6{res['additional_fee']}"
        self.property_status = res['property_status']
        self.property_type = res['property_type']
        self.reason_for_fee = res['reason_for_fee']
        self.payment_duration = res['payment_duration']
        self.reason_for_fee = res['reason_for_fee']
        self.water_system = res['water_system']
        self.agent_name = f"{res['agent']['first_name']} {res['agent']['last_name']}"
        self.agent_email = f"{res['agent']['email']}"
        self.agent_id = f"{res['agent']['id']}"
        self.agent_rating = f"{res['agent']['rating']}"
        self.agent_phone = f"{res['agent']['phone']}"
        self.agent_nick_name = f"{res['agent']['nick_name']}"
        self.agent_image_url = f"{self.image_base_url}/{res['agent']['image_url']}"
        self.category_id = f"{res['category_id']}"
        self.category = f"{res['category']['title']}"
        swiper = self.ids.swiper

        for item in self.images:
            swiper.add_widget(
                self.add_swiper_item(
                    image=f"{self.image_base_url}/{item['file_path']}")
            )

    def _get_property(self):
        try:

            response = requests.get(
                url=f"{self.base_url}/property/{self.id}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                }
            )

            res = response.json()
            self.images = res['images']

            Clock.schedule_once(lambda x: self.on_get_property(res))

        except Exception as e:
            print(e)

    def on_enter(self, *args):
        self.get_property()

    def on_leave(self, *args):
        swiper = self.ids.swiper
        swiper.clear_widgets()
