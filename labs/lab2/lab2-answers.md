Labb 2

Q4

a) The "theatre" entity set has a unique name (for the movie theatre chain), which makes _t_name_ a natural key. There is also the composite key composed of "m_title_" and "production_year", which is a natural key (assuming you don't name a movie based completely on what movie names already are taken).

b) It is possible for the natural key "t_name" to change, since theatres can change names. After a movie is released, the name of the movie can not be changed, so hte natural key stays the same.

c) The entity set "screening" is a weak entity set.

d) Since the entity set "screening" is a weak entity set, an invented key such as "screening_id" could be used to help identify the specific screening. You could also use a foreign key, such as "imdb_key" from the movie entity set.

A "theatre_id", an invented key for the theatre entity set, would be useful in case the name of the theatre changes. If we only have the natural key "t_name" a change in the name IRL could result in changes in many places in the database.

Q6

theatres(_th_id_, _th_name_, capacity)
movies(_m_title_, _production_year_, _imdb_key_, running_time)
customers(_username_, full_name, password)
tickets(_ti_id_, /_th_id_/, /_start_time_/, /_imdb_key_/)
screenings(start_time, sc_title, /_imdb_key_/)

Q7. There are at least two ways of keeping track of the number of seats available for each performance – describe them both, with their upsides and downsides (write your answer in lab2-answers.md).

One way to keep track of the available seats is to have a mutable attribute that logs the number of available seats, such as "available-seats". A bought or refunded ticket means that the attribute itself is changed, requiring the database to be locked.

The other way is keeping track of the available by logging sold and refunded tickets. The available seats are then calculated from these two attributes. It requires extra calculation, but it does not require the database to be locked for every ticket sale or refund, which makes it a more flexible scheme. Keeping track of transactions like this is called event sourcing.
