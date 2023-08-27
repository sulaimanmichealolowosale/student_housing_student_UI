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
from kivymd.uix.list import OneLineListItem


Builder.load_string('''

<Category>:

    MDScrollView:
        effect_cls: "ScrollEffect"
        size_hint: 1, .9
        scroll_y:1
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
                MDList:
                    id:list

            GridLayout:
                cols:2
                id:property_grid
                spacing: '10dp'

            
    MDSpinner:
        active:root.spinner_state
        size_hint:None, None
        height: dp(50)
        width: dp(50)
        pos_hint:{'center_x': .5, 'center_y': .5}


    ''')


class Category(MDScreen, MDBoxLayout):
    name = "category"
    base_url = StringProperty()
    image_base_url = StringProperty()
    category_list = ListProperty()
    search_text = StringProperty()
    spinner_state = BooleanProperty(True)
    id = StringProperty()
    cat_id = StringProperty()
    category_title = StringProperty()


    def to_single(self, instance):
        id = instance.id
        self.parent.get_screen("by_category").cat_id = str(id)
        self.parent.get_screen("by_category").from_screen = self.name
        self.parent.get_screen("by_category").id = self.id
        self.parent.current = "by_category"

    def add_category(self, title, id):
        try:
            list_item = OneLineListItem(
                text=title,
                theme_text_color = "Custom",
                text_color = (1,1,1,1),
            )

            setattr(list_item, "id", str(id))
            list_item.bind(on_release=self.to_single)

            return list_item

        except Exception as e:
            print(e)

    def on_get_category(self):
        list = self.ids.list
        self.spinner_state = False

        for item in self.category_list:
            list.add_widget(self.add_category(
                title=item['title'],
                id=item['id']
            )
            )
        app = MDApp.get_running_app()
        app_bar = app.root.ids.app_bar
        app_bar.title = "Student Housing Categories"

    def get_category(self):
        t = threading.Thread(target=self._get_category)
        t.start()

    def _get_category(self):
        try:
            response = requests.get(
                url=f"{self.base_url}/category",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                }
            )
            if response.ok:
                self.spinner_state = False
            res = response.json()
            self.category_list = res
            Clock.schedule_once(lambda x: self.on_get_category())
            return res

        except Exception as e:
            print(e)

    def on_enter(self, *args):
        self.get_category()

    def on_leave(self, *args):
        self.spinner_state = True
        list = self.ids.list
        list.clear_widgets()
