from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Building = db.Column(db.String(10), index=True, unique=False)
	Room = db.Column(db.String(10), index=True, unique=False)
	Location_x = db.Column(db.String(20), index=True, unique=False)
	Location_y = db.Column(db.String(20), index=True, unique=False)
	SSID = db.Column(db.String(20), index=True, unique=False)
	BSSID = db.Column(db.String(20), index=True, unique=False)
	Frequency = db.Column(db.String(10), index=True, unique=False)
	Level = db.Column(db.String(10), index=True, unique=False)
	Model = db.Column(db.String(10), index=True, unique=False)
	Time  = db.Column(db.String(10), index=True, unique=False)
	def __repr__(self):
		return '<User %r>' % (self.id)




'''class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
		
	nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)'''