from math import radians, cos, sin, asin, sqrt
class MinDistancia:
    def __init__(self, dict_ListaCoordenadas):
        self.Nombre = dict_ListaCoordenadas['nombre']
        self.ListaCor = dict_ListaCoordenadas['coordenadas']

    def DistanciaMin(self, Lista, Camino):
        MinDis = 100000
        IndMin = 0
        n = len(Lista)
        for i in range(1,n):
            if (MinDis > Lista[i]) and (i not in Camino):
                MinDis = Lista[i]
                IndMin = i

        return IndMin

    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6372.8
        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
        c = 2*asin(sqrt(a))
        return R * c
        
    def CaminoMinimo(self):
        n = len(self.ListaCor)
        Dis = [1000000]*n
        for i in range(n):
            Dis[i]=[1000000]*n
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                else:
                    Dis[i][j] = self.haversine(self.ListaCor[i][0], self.ListaCor[i][1], self.ListaCor[j][0], self.ListaCor[j][1])
        XD = 0
        Camino = [0]
        for i in range(n-1):
            XD = self.DistanciaMin(Dis[XD], Camino)
            Camino.append(XD)
        
        ListRuta = []
        for i in Camino:
            Lista = []
            Lista.append(self.ListaCor[i][0])
            Lista.append(self.ListaCor[i][1])
            ListRuta.append(Lista)
        
        return {'nombre': self.Nombre, 'coordenadas': ListRuta}

def test():
    d_region = {
        'nombre': "Almacen 1",
        'coordenadas':[
            [-71.887626,-13.546890],
            [-71.993247,-13.525835],
            [-71.968925,-13.517197],
            [-71.966753,-13.531635],
            [-71.939824,-13.527277],
            [-71.915907,-13.531228],
        ]
    }
    mindist = MinDistancia(d_region)
    print(mindist.CaminoMinimo())

if __name__ == "__main__":
    test()