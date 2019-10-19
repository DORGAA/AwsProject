############### S #############

class Tableau:
  def __init__(self ,nom,id_tableau):
    self.nom = nom
    self.id_tableau=id_tableau
  def insert(self, cursor):
    cursor.execute('''INSERT INTO tableaux VALUES ( ?, ? ) ''', (self.nom ,self.id_tableau)
    )
        
        
  @classmethod
  def create_table(cls, cursor):
    cursor.execute('DROP TABLE IF EXISTS tableaux')

    cursor.execute('''
    CREATE TABLE tableaux   
    ( id NUMBER NOT NULL primary key,
    nom TEXT NOT NULL
    )''')
        
        
class TableauForDisplay:
    def __init__(self, row):
        self.nom = row["nom"]
        self.id=row["id"]
   
    
    @classmethod
    def getAll(cls, cursor):
      cursor.execute('''
          SELECT * 
          FROM tableaux
      ''')
      #print(cursor.fetchall() )
      #print("******")
      return cursor.fetchall()
        
        
        
     