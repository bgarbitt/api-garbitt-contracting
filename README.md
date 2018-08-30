Simple flask api connecting to MySQL database.

To run (on windows command prompt):

* Make sure you're in the api directory
* mysql -u root -p gcl < schema.sql
* enter password (should destroy current database and create a new one)
* mysql -u root -p gcl
* open Database_test_inserts.txt in some editor. Copy all. Paste into database.
* Database should be populated now.
* py app.py