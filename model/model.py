import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._artObjects = DAO.getAllObjects()  # lista con le fermate
        # creo grafo
        self._grafo = nx.Graph()
        # mappa di oggetti
        self.idMapObjects = {}
        for f in self._artObjects:
            self.idMapObjects[f.object_id] = f

        self._bestPath= []
        self._bestCost=0


    def getOptPath(self,source,lun):
        #inizializzo best path e best cost sia nell'init che a inizio metodo
        self._bestPath= []
        self._bestCost=0

        parziale=[source]

        for n in nx.neighbors(self._grafo,source):#tra tutti i vicini di source
            if parziale[-0].classification == n.classification and n not in parziale:
                parziale.append(n)
                #chiamo la ricorsione
                self._ricorsione(parziale,lun)
                #backtracking
                parziale.pop()

        return self._bestPath,self._bestCost

    def _ricorsione(self,parziale,lun):
        #metodo terminale: parziale è una soluzione valida
        if len(parziale) == lun: #parziale ha la lunghezza passata in input
            #verifico se è una soluzione miglione, ma in ogni caso esco
            if self.costo(parziale)< self._bestCost:
                self._bestCost= self.costo(parziale)
                self._bestPath = copy.deepcopy(parziale) #ricordalo sempre
            return #fuori dall'if perchè returno a prescindere

        else: #significa che ancora stiamo okay
            for n in nx.neighbors(self._grafo,parziale[-1]): #-1 perchè è l'ultimo
                if parziale[-0].classification== n.classification: #il testo dice che devono avere tutti la classification
                    parziale.append(n)
                    self._ricorsione(parziale,lun)
                    parziale.pop()#backtraking

    def costo(self,listaOggetti):
        "prende una lista di oggetti e mi somma i pesi"
        totCosto= 0
        for i in range(0,len(listaOggetti)-1): #se iteri sugli archi è sempre -1
            totCosto=self._grafo[listaOggetti[i]][listaOggetti[i+1]]["weight"] #i e i+1 sono due archi successivi
        return totCosto

    def buildGraphPesato(self):
        # aggiungiamo i nodi(li ho nelle fermate)
        self._grafo.add_nodes_from(self._artObjects)
        # aggiungo archi
        self.addEdgesPesati()

    def addEdgesPesati(self):
        allEdges=DAO.peso_coppie(self.idMapObjects)
        for edge in allEdges:
            self._grafo.add_edge(edge.o1, edge.o2, weight=edge.peso)


    def getNumNodi(self):
        return len(self._grafo.nodes())

    def getNumArchi(self):
        return len(self._grafo.edges())

    @property
    def objects(self):
        return self._artObjects

    def getInfoConnessa(self,idInput):
        """
        restituisce la dimensione della componente connessa(a quanti nodi è collegata: cioè a quanti nodi può arrivare(da una fermata, quante fermate della metro posso raggiungere?)
        deepfirst e breath first
        """
        source= self._idMapObjects[idInput]
        #modo 1: conto i successori
        successori= nx.dfs_successors(self._grafo, source).values() #restituisce un dizionario chiave: oggetto, valore: lista di oggetti successori
        res=[]
        for s in successori:
            res.extend(s)
        print("modo 1:", len(res)+1)

        # modo 2: conto i predecessori
        predecessori = nx.dfs_predecessors(self._grafo,source)  # restituisce un dizionario chiave: oggetto, valore: il predecessore
        print("modo 1:", len(predecessori.values())+1)

        #modo3:dfstree, e conto i nodi dell'albero di visita
        dfsTree= nx.dfs_tree(self._grafo, source).values() #e poi faccio len

        #modo 4:medodi connectivity
        conn= nx.node_connected_components(self._graph,source)

        return len(conn)

    def hasNode(self,idInput):
        """
        per vedere se c'è il nodo scritto
        """
        return idInput in self._idMapObjects

    def getObjectFromId(self,id):
        return self.idMapObjects[id]

