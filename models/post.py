import datetime

class Post:
    def __init__(self, content, author_id,colonne_id):
        self.content = content
        self.author_id = author_id
        self.timestamp = datetime.datetime.now().timestamp()
        self.colonne_id = colonne_id

    def insert(self, cursor):
        cursor.execute('''
          INSERT INTO posts 
          VALUES 
          ( ?, ?, ?,? )
        ''', (self.content, self.author_id, self.timestamp,self.colonne_id)
        )
        
    def __repr__(self):
        return "[Post by %s at %s: %s]"%(
            self.author_id, 
            str(datetime.datetime.fromtimestamp(self.timestamp)),
            self.content[:50]
        )

    @classmethod
    def create_table(cls, cursor):
        cursor.execute('DROP TABLE IF EXISTS posts')

        cursor.execute('''
        CREATE TABLE posts
        ( author_id TEXT NOT NULL
        , content TEXT
        , colonne_id TEXT
        , timestamp DOUBLE
        , FOREIGN KEY (author_id) REFERENCES users(email)
        , FOREIGN KEY (colonne_id) REFERENCES colonnes(nom)
        )''')

class PostForDisplay:
    def __init__(self, row):
        self.author_name = row['author_name']
        self.date = datetime.datetime.fromtimestamp(row['timestamp'])
        self.content = row['content']
        self.colonne_id = row['colonne_id']
   
    
    @classmethod
    def getAll(cls, cursor):
      cursor.execute('''
          SELECT *
          FROM posts
      ''')
      return [ cls(row) for row in cursor.fetchall() ]