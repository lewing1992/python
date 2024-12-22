from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button

import xlsxwriter

class HistorialScreen(Screen):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.cursor = db.cursor()

        self.layout = BoxLayout(orientation="vertical")
        self.info = Label(text=self.mostrar_historial())
        self.exportar_btn = Button(text="Exportar a Excel", on_press=self.exportar_excel)
        volver_btn = Button(text="Volver al Menú", on_press=self.volver_al_menu)

        self.layout.add_widget(self.info)
        self.layout.add_widget(self.exportar_btn)
        self.layout.add_widget(volver_btn)
        self.add_widget(self.layout)

    def mostrar_historial(self):
        self.cursor.execute("SELECT nombre, cantidad, pago, deuda, fecha FROM clientes")
        registros = self.cursor.fetchall()

        if not registros:
            return "No hay registros en el historial."

        texto = "Historial de Compras:\n"
        for nombre, cantidad, pago, deuda, fecha in registros:
            estado = "Debe" if deuda > 0 else "Pagado"
            texto += f"{fecha} - {nombre}: {cantidad} huevos, {estado}, Deuda: {deuda:.2f}\n"
        return texto

    def exportar_excel(self, instance):
        workbook = xlsxwriter.Workbook("historial_compras.xlsx")
        worksheet = workbook.add_worksheet()

        self.cursor.execute("SELECT nombre, cantidad, pago, deuda, fecha FROM clientes")
        registros = self.cursor.fetchall()

        headers = ["Fecha", "Nombre", "Cantidad", "Pagado", "Deuda"]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        for row, registro in enumerate(registros, start=1):
            for col, dato in enumerate(registro):
                worksheet.write(row, col, dato)

        workbook.close()
        self.info.text += "\nHistorial exportado a historial_compras.xlsx."
    def volver_al_menu(self, instance):
        self.manager.current = "menu"
