import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self.stateMap = {}
        self._bestSoluzione = []
        self._bestScore = 0

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllStates(self, year):
        stati = DAO.get_all_states_year(year)
        for node in stati:
            n = node.id.lower()
            self._idMap[n] = node
        return stati

    def buildGraph(self, year, stato):
        self._graph.clear()
        self._nodi = DAO.getAllNodes(year, stato)
        self._graph.add_nodes_from(self._nodi)
        for node in self._nodi:
            self._idMap[node.id] = node
        archi = DAO.getAllEdges(year, stato)
        for edge in archi:
            u = self._idMap[edge[0]]
            v = self._idMap[edge[1]]
            if u.distance_HV(v) < 100:
                self._graph.add_edge(u, v)

    def getDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getCompConnesse(self):
        compConn = list(nx.connected_components(self._graph))
        maxComp = max(compConn, key=len)
        return compConn, maxComp

    def getAvvistamenti(self):
        self._bestSoluzione = []
        self._bestScore = 0
        parziale = []
        for n in self._graph.nodes:
            parziale.append(n)
            self._ricorsione(parziale, n.duration)
            parziale.pop()
        return self._bestSoluzione, self._bestScore

    def _ricorsione(self, parziale, durataPrec):
        #cond ottimale
        if self.score(parziale) > self._bestScore:
            print("ottimo")
            self._bestSoluzione = copy.deepcopy(parziale)
            self._bestScore = self.score(parziale)

        for n in self._graph.neighbors(parziale[-1]):
            print("continua")
            if n not in parziale and self.amm(n, parziale) and n.duration > durataPrec:
                print("aggiunge")
                parziale.append(n)
                self._ricorsione(parziale, n.duration)
                parziale.pop()

    def amm(self, n, parziale):
        mese = n.datetime.month
        tot = 0
        for m in parziale:
            if m.datetime.month == mese:
                tot += 1
        if tot <= 2:
            return True
        return False

    def score(self, parziale):
        tot = 0
        for n in range(0, len(parziale)-1):
            if parziale[n].datetime.month == parziale[n+1].datetime.month:
                tot+=200
        tot += 100 * len(parziale)
        return tot
