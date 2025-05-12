import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        #creo il grafo
        self._model.buildGraphPesato()
        self._view.txt_result.controls.append(ft.Text(f"il grafo contiene {self._model.getNumNodi()} nodi e {self._model.getNumArchi()} archi"))

       #una volta creato il grafo posso abilitare l'altro bottone
        self._view.txtIdOggetto.disabled=False
        self._view._btnCompConnessa.disabled=False

        self._view.update_page()

    def handleCompConnessa(self,e):
        txtInput= self._view.txtIdOggetto.value

        if txtInput == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("inserisci un valore"))
            self._view.update_page()
            return

        try:
            idInput = int(txtInput)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("inserisci un numero"))
            self._view.update_page()
            return

        if not self._model.hasNode(idInput):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("inserisci un id valido"))
            self._view.update_page()
            return

        sizeComponenteConnessa= self._model.getInfoConnessa(idInput)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"la componente connessa che contiene il nodo {self._model.getObjectFromId} ha dimensione pari a {sizeComponenteConnessa}"))

        self._view._ddLun.disabled = False
        self._view._btnCerca.disabled = False

        #riempo tendina!!!
        #myValues= list(range(2,sizeComponenteConnessa))
        # for i in myValues:
        #     self._view._ddLun.options.append(ft.dropdown.Option(i))
        myValues = list(range(2, sizeComponenteConnessa))
        myValuesDD= map(lambda x: ft.dropdown.Option(x),myValues)
        self._view.update_page()


    def handleCerca(self,e):
        source= self._model.getObjectFromId(int(self._view.txtIdOggetto.value))
        lun = self._view._ddLun.value
        if lun is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("inserisci un parametro lunghezza"))
            self._view.update_page()
            return
        lunInt= int(lun)
        path, peso= self._model.getOptPath(source,lunInt)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"cammino trovato. Peso: {peso}"))
        for i in path:
            self._view.txt_result.controls.append(ft.Text(i))
        self._view.update_page()






