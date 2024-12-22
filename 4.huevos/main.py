from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from bdd import conectar_bd
from clientes import ClientesScreen
from inventario import InventarioScreen
from historial import HistorialScreen

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button



class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")
        
        # Botones para navegar
        btn_clientes = Button(text="CLIENTES", on_press=self.ir_a_clientes)
        btn_inventario = Button(text="INVENTARIO", on_press=self.ir_a_inventario)
        btn_historial = Button(text="HISTORIAL", on_press=self.ir_a_historial)
        # btn_reniciarBdd = Button(text="ELIMINAR DATOS", on_press=self.reset_db)

        self.layout.add_widget(btn_clientes)
        self.layout.add_widget(btn_inventario)
        self.layout.add_widget(btn_historial)


        self.add_widget(self.layout)


    def ir_a_clientes(self, instance):
        self.manager.current = "clientes"

    def ir_a_inventario(self, instance):
        self.manager.current = "inventario"

    def ir_a_historial(self, instance):
        self.manager.current = "historial"

    # def reset_db(self, instance):
    #     db = reset_database()
    #     db.reset_database()
    #     print("Base de datos reiniciada con éxito.")


class HuevosApp(App):
    def build(self):
        db = conectar_bd()


        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(ClientesScreen(db, name="clientes"))
        sm.add_widget(InventarioScreen(db, name="inventario"))
        sm.add_widget(HistorialScreen(db, name="historial"))

        sm.current = "menu"

        return sm

if __name__ == "__main__":
    HuevosApp().run()
