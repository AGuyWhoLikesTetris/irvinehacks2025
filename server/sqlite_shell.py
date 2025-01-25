# sqlite_shell.py
#
# ICS 33 Winter 2025
# Code Example
#
# This is a SQLite shell that we can run within a Python shell, which will
# allow us to type SQL statements and see their results (or any error
# messages they produce if they fail).

import sqlite3



def run():
    # We'll start by asking the user where their database is located.
    database_path = input('Database Path: ').strip()

    # If the user specifies no database path, then we'll connect to an
    # in-memory database instead.
    if len(database_path) == 0:
        database_path = ':memory:'

    connection = None

    try:
        connection = _connect(database_path)

        # Read one statement and, if it's something other than None,
        # execute it.  Continue until _read_next_statement returns None.
        while statement := _read_next_statement(connection):
            _execute_statement(connection, statement)
    except sqlite3.Error as e:
        _display_error(e)
    finally:
        # Be sure that we've closed the connection.  Note that the
        # "with" statement won't work here, since sqlite3's connections
        # are not context managers.
        if connection is not None:
            connection.close()



def _connect(database_path):
    # The "isolation_level" parameter is a way of controlling what
    # happens when more than one connection modifies the database
    # simultaneously, which is a problem we won't need to address
    # here, so our best bet is to simply turn that feature off.
    connection = sqlite3.connect(database_path, isolation_level = None)

    # Ask SQLite to enforce foreign keys, which is not the default, so
    # we have to turn this feature on each time we connect.
    _quietly_execute_statement(connection, 'PRAGMA foreign_keys = ON;')

    return connection



def _read_next_statement(connection):
    PROMPT = 'Statement:'

    statement = input(f'{PROMPT} ').strip()

    # If the user typed an empty line to begin with, we'll return
    # None, which will cause the program to end.
    if len(statement) == 0:
        return None

    # We'll ask the user to continue typing lines of text until all
    # of the lines of text they've typed make up a complete SQL
    # statement.  Fortunately, we don't have to know whether a
    # statement is complete, since sqlite3.complete_statement can
    # answer that question for us.
    while not sqlite3.complete_statement(statement):
        next_line = input(f'{"." * len(PROMPT)} ').strip()
        statement += ' ' + next_line

    return statement



def _quietly_execute_statement(connection, statement):
    cursor = None

    try:
        # Execute a statement that we expect not to return any data.
        cursor = connection.execute(statement)
    finally:
        # When we get here, cursor might be None (if executing the statement
        # failed), so we need to be careful to close the cursor only if it
        # was opened.
        if cursor is not None:
            cursor.close()



def _execute_statement(connection, statement):
    cursor = None

    try:
        # Execute the statement and, if successful, fetch and print all of
        # the rows from the resulting cursor.
        cursor = connection.execute(statement)

        while row := cursor.fetchone():
            print(row)
    except sqlite3.Error as e:
        _display_error(e)
    finally:
        # When we get here, cursor might be None (if executing the statement
        # failed), so we need to be careful to close the cursor only if it
        # was opened.
        if cursor is not None:
            cursor.close()



def _display_error(e):
    error_message = ' '.join(e.args)
    print(f'ERROR: {error_message}')



if __name__ == '__main__':
    run()
