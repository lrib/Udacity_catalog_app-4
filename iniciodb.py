from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Categoria, Item, User

engine = create_engine('sqlite:///project.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Categoria Start

categoria1 = Categoria(id=1, name="Flamengo")
session.add(categoria1)
session.commit()

categoria2 = Categoria(id=2, name="Botafogo")
session.add(categoria2)
session.commit()

categoria3 = Categoria(id=3, name="Vasco")
session.add(categoria3)
session.commit()

categoria4 = Categoria(id=4, name="Fluminense")
session.add(categoria4)
session.commit()

categoria5 = Categoria(id=5, name="Bangu")
session.add(categoria5)
session.commit()

categoria6 = Categoria(id=6, name="America")
session.add(categoria6)
session.commit()

# Categoria Stop
