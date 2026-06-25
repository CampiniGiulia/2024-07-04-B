from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SeLECt DISTINCT year(s.`datetime` ) as anno
                        FROM sighting s
                        order by anno """
            cursor.execute(query)

            for row in cursor:
                result.append(
                row["anno"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_states_year(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT distinct s2.*
                        FROM sighting s, state s2 
                        WHERE s.state = s2.id and YEAR(s.`datetime` ) = %s
                        order by s2.name"""
            cursor.execute(query, (year,))

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(year, stato):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.*
                        FROM sighting s, state s2 
                        wHERE s.state = s2.id and YEAR(s.`datetime` ) = %s and s.state=%s """
            cursor.execute(query, (year, stato))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(year, stato):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT distinct t1.id1 as id1, t2.id2 as id2
                        FROM (SELECT s.id as id1, s.shape as forma1
                        FROM sighting s, state s2 
                        wHERE s.state = s2.id and YEAR(s.`datetime` ) = %s and s.state=%s) t1,
                        (SELECT s.id as id2, s.shape as forma2
                        FROM sighting s, state s2 
                        wHERE s.state = s2.id and YEAR(s.`datetime` ) = %s and s.state=%s) t2
                        WHERE t1.id1 < t2.id2 and t1.forma1 = t2.forma2  """
            cursor.execute(query, (year, stato, year, stato))

            for row in cursor:
                result.append((row["id1"], row["id2"]))
            cursor.close()
            cnx.close()
        return result