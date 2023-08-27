from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.utils import platform

from components.auth import Auth
from components.register import Register
# from components.dashboard import DashboardView


# ################## CATEGORY IMPORTS#########################


# ################## PROPERTY IMPORTS#########################

from components.property import Listing
from components.single import Single
from components.by_category import ByCategory
from components.category import Category
from components.agent import Agent
from components.agent_details import AgentDetails
from components.account import Account
from components.update_account import UpdateUser


# from components.account import Account

from kivy.clock import Clock

from kivy.core.window import Window

Window.size = (400, 650)

BASE_URL = "http://192.168.0.100:8000/"
IMAGE_BASE_URL = "http://192.168.0.100:8000/"


KV = '''

<DrawerClickableItem@MDNavigationDrawerItem>
    focus_color: "#e7e4c0"
    text_color: "#4a4939"
    icon_color: "#4a4939"
    ripple_color: "#c5bdd2"
    selected_color: "#0c6c4d"

<Main>

    MDNavigationDrawerMenu:
        effect_cls: "ScrollEffect"

        DrawerClickableItem:
            icon: "home-city"
            text: "Listings"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "listing"

        DrawerClickableItem:
            icon: "account-multiple"
            text: "Agents"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "agent"
                
        DrawerClickableItem:
            icon: "playlist-check"
            text: "Categories"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "category"
        
        MDNavigationDrawerDivider:

        DrawerClickableItem:
            icon: "account"
            text: "Account"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "account"

        DrawerClickableItem:
            icon: "logout"
            text: "Logout"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "auth"

MDScreen:

    FitImage:
        id:profile_picture
        height: root.height
        allow_stretch:False  

        canvas.after:
            Color:
                rgba: 0, 0, 0, .5  
            Rectangle:
                pos: self.pos
                size: self.size

    MDTopAppBar:
        id:app_bar
        pos_hint: {"top": 1}
        elevation: 4
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
       

    MDNavigationLayout:

        MDScreenManager:
            id: screen_manager

            Auth:
                on_enter:nav_drawer.disabled = True
                on_pre_leave:nav_drawer.disabled = False
                
            Register:
                on_enter:nav_drawer.disabled = True
                on_pre_leave:nav_drawer.disabled = False

            Listing:

            Single:

            ByCategory:

            Category:

            Agent:

            AgentDetails:

            Account:

            UpdateUser:


        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
            enable_swiping:True

            Main:
                id:main
                screen_manager: screen_manager
                nav_drawer: nav_drawer
               
'''


class Main(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    nav_image = StringProperty("kivy.png")


class StudentHousing(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.material_style = "M3"
        # self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def on_start(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions(
                [
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE,
                    Permission.CALL_PHONE
                ]

            )


if __name__ == "__main__":
    try:
        StudentHousing().run()
    except Exception as e:
        print(e)
