from bottle import get, post, run, request, response
import sqlite3
import json

conn = sqlite3.connect("movies.sqlite")

def hash(msg):
    import hashlib
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()


def format_response(d):
    return json.dumps(d, indent=4) + "\n"

@get('/ping')
def ping():
#    response.content_type = 'application/json'
    response.status = 200
    return 'pong \n'


@post('/reset')
def reset_tables():
	c = conn.cursor()
	c.executescript("""
		
		DELETE 
		FROM theatres;

		DELETE 
		FROM movies;

		DELETE 
		FROM tickets;

		DELETE 
		FROM customers;

		DELETE 
		FROM screenings;

		INSERT OR IGNORE
		INTO customers(username, full_name, c_password)
		VALUES	('alice', 'Alice', 'dobido'),
			('bob', 'Bob', 'whatsinaname');

		INSERT OR IGNORE
		INTO movies(m_title, production_year, imdb_key, running_time)
		VALUES	('The Shape of Water', 2017, 'tt5580390', 120),
			('Moonlight', 2016, 'tt4975722', 140),
			('Spotlight', 2015, 'tt1895587', 90),
			('Birdman', 2014, 'tt2562232', 107);

		INSERT OR IGNORE
		INTO theatres(th_name, capacity)
		VALUES	('Kino', 10),
			('Södran', 16),
			('Skandia', 100);
		"""
	)
	conn.commit()
	u = [{"username": username, "full name": fullname, "password": c_password}
        	for (username, fullname, password) in c]
	
	t = [{"th_name": th_name, "capacity": capacity}
        	for (th_name, capacity) in c]
	response.status = 200
	return 'OK\n'

@get('/theaters')
def get_theatres():
	c = conn.cursor()
	c.execute(
		"""
		SELECT *
		FROM theatres
		WHERE 1=1
		"""
	)
	s = [{"theater": theater, "capacity": capacity}
        	for (theater, capacity) in c]
	return json.dumps({"data": s}, indent=4)

@get('/movies')
def get_movies():
	c = conn.cursor()
	query =	"""
		SELECT *
		FROM movies
		WHERE 1=1
		"""
	params = []
	if request.query.title:
		query += "AND m_title = ? "
		params.append(request.query.title)
	if request.query.year:
		query += "AND production_year = ? "
		params.append(request.query.year)
	if request.query.imdb:
		query += "AND imdb_key = ?"
		params.append(request.query.imdb)
	c.execute(
		query,
		params
	)
	m = [{"title": title, "year": year, "imdb_key": imdb, "running_time": running_time}
        	for (title, year, imdb, running_time) in c]

	response.status = 200
	return json.dumps({'data': m}, indent=4)

@get('/movies/<imdb>')
def get_movie(imdb):
    c = conn.cursor()
    c.execute(
        """
        SELECT *
        FROM   movies
        WHERE  imdb_key = ?
        """,
        [imdb]
    )
    m = [{"title": title, "year": year, "imdb": imdb, "running_time": running_time}
        	for (title, year, key, running_time) in c]
    response.status = 200
    return json.dumps({'data': m}, indent=4)

@get('/performances')
def get_screenings():

	query = """
		SELECT sc_id, sc_date, start_time, th_name, production_year, capacity - tickets_sold, m_title
		FROM screenings
		JOIN theatres
		USING (th_name)
		JOIN movies
		USING (imdb_key)
		WHERE 1=1
		"""
	params = []
	if request.query.performance:
		query += "AND sc_id = ? "
		params.append(request.query.performance)
	if request.query.date:
		query += "AND sc_date = ? "
		params.append(request.query.date)
	if request.query.time:
		query += "AND start_time = ? "
		params.append(request.query.time)
	if request.query.imdb:
		query += "AND imdb_key = ?"
		params.append(request.query.imdb)
	if request.query.theater:
		query += "AND th_name = ?"
		params.append(request.query.theater)

	c = conn.cursor()
	c.execute(
		query,
		params
	)
	s = [{"performanceId": performance, "date": date, "startTime": time, "theater": theater, "year": year, "remainingSeats": remainingSeats, "title": title}
		for (performance, date, time, theater, year, remainingSeats, title) in c]
	response.status = 200
	return json.dumps({"data": s}, indent=4)


# curl -X POST http://localhost:7007/performances\?imdb=<imdb>\&theater=<theater>\&date=<date>\&time=<time>
@post('/performances')
def post_screening():
   date = request.query.date
   time = request.query.time
   theater = request.query.theater
   imdb = request.query.imdb
   if not (date and time and theater and imdb):
      return 'NOT OK'
   c = conn.cursor()
   c.execute(   
	"""
	INSERT OR IGNORE
	INTO screenings(sc_date, start_time, th_name, imdb_key)
	VALUES(?,?,?,?)
	""",
	[date, time, theater, imdb]
   )
   conn.commit()
   response.status = 200
   return 'OK'

@post('/tickets')
def post_ticket():
	user = request.query.user
	performance = request.query.performance
	pwd = request.query.pwd
	if not (user and performance and pwd):
		response.status = 400
		return 'NOT OK'
	c = conn.cursor()
	c.execute(
		"""
		SELECT c_password
		FROM customers
		WHERE username = ?		
		""", [user]
	)
#	actual_password = c.fetchone()
#	if not (actual_password == hash(pwd)):
#		return 'Wrong password'
	print(format_response(performance))
	c.execute(
		"""
		SELECT capacity - tickets_sold
		FROM screenings
		JOIN theatres
		USING (th_name)
		WHERE sc_id = ?
		""", [performance]
	)
	for row in c:
		nbrOfSeats = row[0]
	if(nbrOfSeats <= 0):
		return 'No tickets left'
	c.execute(
		"""	
		INSERT
		INTO tickets(username, sc_id)
		VALUES(?,?)
		""", [user, performance]
	)
	c.execute(
		"""
		SELECT ti_id
		FROM   tickets
		WHERE rowid = last_insert_rowid()
		"""
	)
	for row in c:
		id = row[0]
	c.execute(
		"""
		UPDATE screenings
		SET tickets_sold = tickets_sold + 1
		WHERE sc_id = ?
		""", [performance]
	)
	conn.commit()
	response.status = 200
	return format_response("/tickets/{}".format(id))

@get('/customers/:username/tickets')
def customer_tickets(username):
    c = conn.cursor()
    c.execute(
        """
        SELECT sc_date, start_time, th_name, m_title, production_year, COUNT(sc_id) AS nbrOfTickets
        FROM customers
        JOIN tickets
        USING (username)
        JOIN screenings
        USING (sc_id)
        JOIN movies
        USING (imdb_key)
        GROUP BY sc_id
        HAVING username = ?
        """, [username]
        )
    s = [{"date": p_date, "startTime": p_time, "theater": theater_name, "year": year, "title": title, "nbrOfTickets": nbrOfTickets}
          for (p_date, p_time, theater_name, title, year, nbrOfTickets) in c]
    response.status = 200
    return format_response({"data": s})

@get('/tickets')
def get_tickets():
	query = """
		SELECT ti_id, username, sc_id, th_name, sc_date, start_time, m_title, tickets_sold
		FROM tickets
		JOIN screenings
		USING (sc_id)
		JOIN movies
		USING (imdb_key)
		GROUP BY sc_id
		HAVING 1=1
		"""
	params = []

	if request.query.ti_id:
		query += "AND ti_id = ? "
		params.append(request.query.ti_id)
	if request.query.user:
		query += "AND username = ? "
		params.append(request.query.user)
	if request.query.performance:
		query += "AND sc_id = ?"
		params.append(request.query.performance)
	if request.query.theater:
		query += "AND th_name =?"
		params.append(request.query.theater)
	if request.query.date:
		query += "AND sc_date = ? "
		params.append(request.query.date)
	if request.query.time:
		query += "AND start_time = ? "
		params.append(request.query.time)
	if request.query.title:
		query += "AND m_title = ?"
		params.append(request.query.title)
	c = conn.cursor()
	c.execute(
		query,
		params
	)
	s = [{"ti_id": ti_id, "user": user, "sc_id": performance, "theater": theater, "date": date, "time": time, "title": title,"tickets_sold": tickets_sold}
		for (ti_id, user, performance, theater, date, time, title, tickets_sold) in c]
	response.status = 200
	return json.dumps({"data": s}, indent=4)

run(host='localhost', port=7007)


