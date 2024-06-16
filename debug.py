from database.tables import User, session

if __name__ == '__main__':

    a = User.query.filter(User.email == "hope04302@gmail.com")
    print(a)