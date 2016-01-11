import sqlite3
input=(1)
inputg=int(1)
ops='Linux'
user='henkvdven'

datab = sqlite3.connect('logDB.sqlite')
c=datab.cursor()
c.execute('''CREATE TABLE Request
       (Agent           INT    NOT NULL,
       Onderwerp          CHAR     NOT NULL,
       Opgevraagd     CHAR     NOT NULL,
       Account        CHAR);''')

print "Table created successfully";
datab.commit()


c.execute("insert into Request values(?,?,?,?)",(inputg,input,ops,user,))
datab.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
datab.close()
