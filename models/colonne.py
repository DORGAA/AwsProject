############### S #############

class Colonne:
    def __init__(self ,nom,description,id_tableau):
        self.nom = nom
        self.description=description
        self.id_tableau=id_tableau
    def insert(self, cursor):
        cursor.execute('''
          INSERT INTO colonnes
          VALUES 
          ( ?, ?, ? )
        ''', (self.nom, self.description,self.id_tableau)
        )
        
        
    @classmethod
    def create_table(cls, cursor):
        cursor.execute('DROP TABLE IF EXISTS colonnes')

        cursor.execute('''
        CREATE TABLE colonnes      
        ( nom TEXT NOT NULL PRIMARY KEY
        , description TEXT NOT NULL
        , id_tableau TEXT NOT NULL
        , FOREIGN KEY (id_tableau) REFERENCES tableau(id)
        )''')
        
        
class ColonneForDisplay:
    def __init__(self, row):
        self.nom = row["nom"]
        self.description=row["description"]
        self.id_tableau=row["id_tableau"]
   
    
    @classmethod
    def getAll(cls, cursor):
      cursor.execute('''
          SELECT * 
          FROM colonnes
      ''')
      return [ cls(row) for row in cursor.fetchall() ]
    
    @classmethod
    def getAllForTab(cls, cursor,tab_id):
      cursor.execute('''
          SELECT * 
          FROM colonnes
          WHERE id_tableau= ?
      ''',(tab_id,))
      return cursor.fetchall()
        
        
        
     