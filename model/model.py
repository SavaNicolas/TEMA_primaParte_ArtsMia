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