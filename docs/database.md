How to proceed when creating a new table or changing tables on the file models.py:
	1. Create a issue explaining your changes;
	2. Create a branch with the name of the issue to be fixed;
	3. Ask for Andre's and Salles's blessing;
	4. Add the new field or table on docs/Database_Documentation.md following the model in the document;
	5. Send broadcast notification to all back and and front end developers so they can find what needs to be modified;
	6. Edit the file models.py
	8. Edit the forms.py to add or edit fields;
	9. Add at least 3 test data into the fixtures json document to make sure we can still loaddata into the database if it crashes.