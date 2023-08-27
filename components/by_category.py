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


Builder.load_string('''

<ByCategory>:

    MDTopAppBar:
        pos_hint: {'top':1 }
        left_action_items: [["arrow-left", lambda x: root.back()]]

    MDScrollView:
        effect_cls: "ScrollEffect"
        size_hint: 1, .9
        MDBoxLayout:
            id:main_box
            orientation: 'vertical'
            spacing: '20dp'
            padding: ('10dp', '20dp', '10dp', '10dp')
            size_hint_y:None
            size:(root.width, root.height)
            height:self.minimum_height

            MDBoxLayout:
                size_hint: 1, None
                height:self.minimum_height
                orientation: 'vertical'
                spacing: '10dp'

                MDLabel:
                    id:search_label
                    text:"Listing on Category: " + root.category_title 
                    color: 1 , 1 , 1 , 1

            GridLayout:
                cols:2
                id:property_grid
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


class ByCategory(MDScreen, MDBoxLayout):
    name = "by_category"
    base_url = StringProperty()
    image_base_url = StringProperty()
    property_list = ListProperty()
    search_text = StringProperty()
    spinner_state = BooleanProperty(True)
    id = StringProperty()
    cat_id = StringProperty()
    category_title = StringProperty()
    from_screen = StringProperty()

    def back(self):
        self.parent.current = self.from_screen

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

    def on_get_property(self, res):
        property_grid = self.ids.property_grid
        self.spinner_state = False
        self.category_title = res['title']

        for item in self.property_list:
            property_grid.add_widget(self.add_property(
                image=f"{self.image_base_url}/{item['primary_image_path']}",
                text=item['title'],
                id=item['id']
            )
            )

    def get_property(self):
        t = threading.Thread(target=self._get_property)
        t.start()

    def _get_property(self):
        try:
            response = requests.get(
                url=f"{self.base_url}/category/{self.cat_id}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                }
            )
            if response.ok:
                self.spinner_state = False
            res = response.json()
            self.property_list = res['properties']
            Clock.schedule_once(lambda x: self.on_get_property(res))
            return res

        except Exception as e:
            print(e)

    def on_enter(self, *args):
        self.get_property()

    def on_leave(self, *args):
        self.spinner_state = True
        property_grid = self.ids.property_grid
        property_grid.clear_widgets()
