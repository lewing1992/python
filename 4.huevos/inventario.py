from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from kivy.uix.popup import Popup

class InventarioScreen(Screen):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.cursor = db.cursor()
        self.layout = BoxLayout(orientation="vertical")

        self.info = Label(text=self.actualizar_informacion())
        self.layout.add_widget(self.info)

        # Campos para agregar nuevas cajas
        self.cajas_input = TextInput(hint_text="Añadir cajas al inventario", input_filter="int")
        actualizar_btn = Button(text="Actualizar Inventario", on_press=self.actualizar_inventario)

        # Campos para editar manualmente los huevos
        self.huevos_input = TextInput(hint_text="Editar huevos restantes manualmente", input_filter="int")
        editar_btn = Button(text="Editar Huevos Restantes", on_press=self.editar_huevos)

        volver_btn = Button(text="Volver al Menú", on_press=self.volver_al_menu)

        self.layout.add_widget(self.cajas_input)
        self.layout.add_widget(actualizar_btn)
        self.layout.add_widget(self.huevos_input)
        self.layout.add_widget(editar_btn)
        self.layout.add_widget(volver_btn)
        self.add_widget(self.layout)

    def actualizar_informacion(self):
        self.cursor.execute("SELECT cajas_totales, huevos_restantes FROM inventario")
        cajas_totales, huevos_restantes = self.cursor.fetchone()
        return f"Cajas totales: {cajas_totales}\nHuevos restantes: {huevos_restantes}"

    def actualizar_vista(self):
        """Actualiza dinámicamente la etiqueta del inventario."""
        self.info.text = self.actualizar_informacion()

    def actualizar_inventario(self, instance):
        nuevas_cajas = int(self.cajas_input.text) if self.cajas_input.text else 0
        huevos_por_caja = 30
        nuevos_huevos = nuevas_cajas * huevos_por_caja
        # Validaciones
        if not nuevos_huevos:
            self.show_popup("Epa","El campo agregar caja es obligatorio.")
            return

        nuevos_huevos = int(nuevos_huevos)
        # Validaciones

        self.cursor.execute("UPDATE inventario SET cajas_totales = cajas_totales + ?, huevos_restantes = huevos_restantes + ?",
                            (nuevas_cajas, nuevos_huevos))
        self.db.commit()

        self.actualizar_vista()
        self.cajas_input.text = ""

    def editar_huevos(self, instance):
        nuevos_huevos = int(self.huevos_input.text) if self.huevos_input.text else 0
        if not nuevos_huevos:
            self.show_popup("Epa","El campo huevos restantes es obligatorio.")
            return
        self.cursor.execute("UPDATE inventario SET huevos_restantes = ?", (nuevos_huevos,))
        self.db.commit()

        self.info.text = self.actualizar_informacion()
        self.huevos_input.text = ""

    def volver_al_menu(self, instance):
        self.manager.current = "menu"

    def show_error(self, message):
        self.show_popup("Error", message)

    def show_success(self, message):
        self.show_popup("Éxito", message)

    def show_popup(self, title, message):
        close_btn = Button(text="OK", size_hint=(1, 0.2))
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.8, 0.4),
                      auto_dismiss=True)
        popup.open()