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

<Listing>:

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
                
                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height:self.minimum_height
                    MDTextField:
                        id:search_text
                        text:root.search_text
                        hint_text:"Search"
                        font_size:"14sp"
                        cursor_width:"2sp"
                        multiline:False
                        pos_hint:{"center_x":.5}
                        hint_text_color_focus:"white"
                        hint_text_color_normal:"white"
                        text_color_normal:1 , 1 , 1 , 1
                        text_color_focus:1 , 1 , 1 , 1
                        line_color_normal:1 , 1 , 1 , 1
                        on_text: root.change_text()
                        
                    MDIconButton:
                        icon: "reload"
                        theme_text_color: "Custom"
                        text_color:[1,1,1,1]
                        on_release:
                            root.on_search()
                
                MDLabel:
                    id:search_label
                    color:
                    color: 1 , 1 , 1 , 1

               

                

            GridLayout:
                cols:2
                id:property_grid
                spacing: '10dp'
                size_hint_y: None
                height:self.minimum_height


    MDBoxLayout:
        id:swiper_box
        orientation: 'vertical'
        pos_hint: {'top': .89}
        md_bg_color:[1,1,1,1]
        radius:[10]
        size_hint: 1, None
        height:self.minimum_height
        padding: ('0dp', '20dp', '0dp', '20dp')
        spacing: '20dp'

        MDLabel:
            text: "Recent Listings"
            size_hint: 1, None
            height: dp(10)
            halign:"center"
            font_style:"H4"

        Carousel:
            id:swiper
            size_hint_y: None
            height: dp(250)
            # y: root.height - self.height - dp(20)
            
            
    MDRelativeLayout:
        
        MDSwitch:
            id:switch
            icon_active: "check"
            icon_inactive: "close"
            icon_active_color: "white"
            icon_inactive_color: "grey"
            thumb_color_inactive: "brown"
            pos_hint: {'center_x': .8, 'center_y': .1}
            active:True
            on_active:root.toggle_swiper()
    MDSpinner:
        active:root.spinner_state
        size_hint:None, None
        height: dp(50)
        width: dp(50)
        pos_hint:{'center_x': .5, 'center_y': .5}


    ''')


class Listing(MDScreen, MDBoxLayout):
    name = "listing"
    base_url = StringProperty()
    image_base_url = StringProperty()
    property_list = ListProperty()
    search_text = StringProperty()
    spinner_state = BooleanProperty(True)

    def to_single(self, instance):
        id = instance.id
        self.parent.get_screen("single").id = id
        self.parent.get_screen("single").from_screen = self.name

        self.parent.current = "single"

    def change_text(self):
        try:
            self.search_text = self.ids.search_text.text
            search_label = self.ids.search_label
            search_label.text = "search result for: "+self.search_text
            if self.search_text == "":
                search_label.text = ""
                self.on_leave()
                self.on_enter()

        except Exception as e:
            print(e)

    def on_search(self):
        try:
            search_label = self.ids.search_label
            search_label.text = "search result for: "+self.search_text
            if self.search_text == "":
                search_label.text = ""
            self.on_leave()
            self.on_enter()
        except Exception as e:
            print(e)

    def toggle_swiper(self):
        switch = self.ids.switch
        swiper_box = self.ids.swiper_box

        if switch.active:
            self.add_widget(swiper_box)
        else:
            self.remove_widget(swiper_box)

    def add_swiper_item(self, image, text, id):
        try:
            swiper_item = MDBoxLayout(
                padding=("20dp")
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
            swiper_item.add_widget(smart_tile)

            return swiper_item

        except Exception as e:
            print(e)

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

    def on_get_property(self):
        self.spinner_state = False
        swiper = self.ids.swiper
        property_grid = self.ids.property_grid
        for item in self.property_list[:5]:
            swiper.add_widget(self.add_swiper_item(
                image=f"{self.image_base_url}/{item['primary_image_path']}",
                text=item['title'],
                id=item['id']
            )
            )
        for item in self.property_list:
            property_grid.add_widget(self.add_property(
                image=f"{self.image_base_url}/{item['primary_image_path']}",
                text=item['title'],
                id=item['id']
            )
            )

        app = MDApp.get_running_app()
        app_bar = app.root.ids.app_bar
        app_bar.title = "Student Housing Listings"

    def get_property(self):
        t = threading.Thread(target=self._get_property)
        t.start()

    def _get_property(self):
        try:
            response = requests.get(
                url=f"{self.base_url}/property?search={self.search_text}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                }
            )

            if response.ok:
                self.spinner_state = False
                res = response.json()
                self.property_list = res
                Clock.schedule_once(lambda x: self.on_get_property())

        except Exception as e:
            print(e)

    def on_enter(self, *args):
        self.get_property()

    def on_leave(self, *args):
        self.spinner_state = True
        swiper = self.ids.swiper
        property_grid = self.ids.property_grid
        swiper.clear_widgets()
        property_grid.clear_widgets()
