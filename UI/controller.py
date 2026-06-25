import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._anno = None
        self._stato = None
        self._grafoCostrito = False


    def fillDDYears(self):
        anni = self._model.getAllYears()
        anniOPTI = list(map(lambda x: ft.dropdown.Option(data=x, text=x, on_click=self._choiceDDI), anni))
        self._view.ddyear.options = anniOPTI

    def _choiceDDI(self, e):
        self._anno = int(e.control.data)  # inizializzo nell'init  self._annoInizio = None
        print(self._anno)

    def fillStato(self, e):
        stati = self._model.getAllStates(self._anno)
        statiOPT = list(map(lambda x: ft.dropdown.Option(data=x, text=x.name, on_click=self._choiceDDanni), stati))
        self._view.ddstate.options = statiOPT
        self._view.update_page()

    def _choiceDDanni(self, e):
        self._stato= e.control.data
        print(self._stato)





    def handle_graph(self, e):
        #controlli
        self._model.buildGraph(self._anno, self._stato.id)
        self._grafoCostrito = True
        nodi, archi = self._model.getDetails()
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {nodi} "))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {archi} "))
        compCpnn, maxComp = self._model.getCompConnesse()
        self._view.txt_result1.controls.append(ft.Text(f"Il grafo ha {len(compCpnn)} componenti connesse"))
        self._view.txt_result1.controls.append(ft.Text(f"La componente connessa più grande è costituita da {len(maxComp)} nodi "))
        for n in maxComp:
            self._view.txt_result1.controls.append(ft.Text(f"d:{n.id}- {n.city} [{n.state}], {n.datetime}"))
        self._view.update_page()

    def handle_path(self, e):
        if self._grafoCostrito is False:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text(f"Costruire prima il grafo"))
            self._view.update_page()
            return
        avvistamenti, score = self._model.getAvvistamenti()
        self._view.txt_result2.controls.append(ft.Text(f"Ricorsione con score {score}"))
        for a in avvistamenti:
            self._view.txt_result2.controls.append(ft.Text(f"{a.id} -- durata: {a.duration} -- data: {a.datetime}"))
        self._view.update_page()

