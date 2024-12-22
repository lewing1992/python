from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from datetime import datetime
from kivy.uix.popup import Popup


class ClientesScreen(Screen):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.cursor = db.cursor()
        self.layout = BoxLayout(orientation="vertical")

        # Campos para datos del cliente
        self.nombre_input = TextInput(hint_text="Nombre del cliente")
        self.cantidad_input = TextInput(hint_text="Cantidad de huevos (número entero)", input_filter="int")
        self.pago_input = TextInput(hint_text="Cantidad pagada (número)", input_filter="float")

        registrar_btn = Button(text="Registrar Compra", on_press=self.registrar_compra)
        volver_btn = Button(text="Volver al Menú", on_press=self.volver_al_menu)

        self.resultado = Label(text="")

        self.layout.add_widget(self.nombre_input)
        self.layout.add_widget(self.cantidad_input)
        self.layout.add_widget(self.pago_input)
        self.layout.add_widget(registrar_btn)
        self.layout.add_widget(volver_btn)
        self.layout.add_widget(self.resultado)

        self.add_widget(self.layout)

    def registrar_compra(self, instance):
        nombre = self.nombre_input.text
        cantidad = int(self.cantidad_input.text) if self.cantidad_input.text else 0
        pago = float(self.pago_input.text) if self.pago_input.text else 0.0
        
        # Validaciones
        if not nombre or not cantidad or not pago:
            self.show_popup("Epa","Todos los campos son obligatorios.")
            return

        cantidad = int(cantidad)
        pago = float(pago)

        # Validaciones
        self.cursor.execute("SELECT huevos_restantes FROM inventario")
        huevos_restantes = self.cursor.fetchone()[0]

        if cantidad > huevos_restantes:
            self.resultado.text = "Error: No hay suficientes huevos en inventario."
            return

        precio_por_huevo = 0.5
        total = cantidad * precio_por_huevo
        deuda = max(0, total - pago)
        fecha_actual = datetime.now().strftime("%d-%m-%Y")

        # Registrar en la base de datos
        self.cursor.execute("INSERT INTO clientes (nombre, cantidad, pago, deuda, fecha) VALUES (?, ?, ?, ?, ?)",
                       (nombre, cantidad, pago, deuda, fecha_actual))
        self.cursor.execute("UPDATE inventario SET huevos_restantes = huevos_restantes - ?", (cantidad,))
        self.db.commit()

        self.resultado.text = f"Compra registrada: {nombre}, debe: {deuda:.2f}"

        # Actualizar inventario dinámicamente
        inventario_screen = self.manager.get_screen("inventario")
        inventario_screen.actualizar_vista()

        self.nombre_input.text = ""
        self.cantidad_input.text = ""
        self.pago_input.text = ""
  

    def show_popup(self, title, message):
        close_btn = Button(text="OK", size_hint=(1, 0.2))
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.8, 0.4),
                      auto_dismiss=True)
        popup.open()

    def volver_al_menu(self, instance):
        self.manager.current = "menu"
