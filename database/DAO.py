from database.DB_connect import DBConnect
from model.arco import Arco
from model.artObject import ArtObject


class DAO():
    @staticmethod
    def getAllObjects():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM objects o"
        cursor.execute(query)

        for row in cursor:
            result.append(ArtObject(**row))
            #equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def peso_coppie(idMapObjects):
        """
        Alla pressione del bottone, creare un grafo che rappresenti gli oggetti
        e la loro copresenza nelle varie mostre. In particolare,
        il grafo dovrà essere pesato, semplice e non orientato.
        I vertici rappresentano tutti gli oggetti presenti nel database (tabella objects).
        Un arco collega due oggetti se sono stati esposti contemporaneamente nella stessa exhibition
        ed il peso dell’arco rappresenta il numero di exhibition in cui tali oggetti sono stati contemporaneamente esposti.
        """
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select eo1.object_id as o1, eo2.object_id as o2, count(*) as peso
                    from exhibition_objects eo1, exhibition_objects eo2 
                    WHERE eo1.exhibition_id = eo2.exhibition_id 
                    and eo1.object_id < eo2.object_id 
                    group by eo1.object_id, eo2.object_id
                    order by peso desc"""
        cursor.execute(query)

        for row in cursor:
            result.append(Arco(idMapObjects[row["o1"]],idMapObjects[row["o2"]],row["peso"]))
            # o1 e o2 sono id e noi vogliamo l'oggetto
        cursor.close()
        conn.close()
        return result

