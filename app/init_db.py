from app.database import engine
from models import Base

def main():
    Base.metadata.create_all(bind=engine)
    print('create table')

if __name__ == "__main__":
    main()

