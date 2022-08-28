from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name


class AlgorithmResults(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key = True)
    number_of_elements = db.Column(db.Integer)
    sorting_algorithm = db.Column(db.String(255))
    time_of_execution = db.Column(db.Float)


    def __init__(self, number_of_elements, sorting_algorithm, time_of_execution):
        self.number_of_elements = number_of_elements
        self.sorting_algorithm = sorting_algorithm
        self.time_of_execution = time_of_execution

    # def __repr__(self):
    #     return '<User %r>' % self.name




