#all the queries of .py files are saved here and then same is called in the said .py files (signin.py)
def get_user_by_username(cursor, username):
    query = """
        SELECT user_id, name, username, password
        FROM users
        WHERE username = %s
    """

    cursor.execute(query, (username,)) #execute the SELECT statement
    return cursor.fetchone() #fetch one user that is specified

#signup.py
def create_user(cursor, name, username, email, password_hash):
    query = """
        INSERT INTO users (name, username, email, password)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (name, username, email, password_hash)
    ) #execute the INSERT statement

#createproject.py
def create_project_query(
    cursor, user_id, title, description, duration, agency, budget
):
    query = """
        INSERT INTO projects
        (user_id, title, description, duration, agency, budget)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        user_id,
        title,
        description,
        duration,
        agency,
        budget
    )) #execute the INSERT statement

#fetch all projects belonging to a specific user (viewproject.py)
def get_projects_by_user(cursor, user_id):
    query = """
        SELECT project_id, title, description, duration,
               agency, budget, status, created_at
        FROM projects
        WHERE user_id = %s
        ORDER BY created_at DESC
    """

    cursor.execute(query, (user_id,)) #execute the SELECT statement
    return cursor.fetchall() #fetch all projects of the user

#fetch details of a specific project belonging to a specific user (projectdetails.py)
def get_project_by_id(cursor, project_id, user_id):
    query = """
        SELECT
            project_id,
            title,
            description,
            duration,
            agency,
            budget,
            status,
            created_at
        FROM projects
        WHERE project_id = %s
          AND user_id = %s
    """

    cursor.execute(query, (project_id, user_id)) #execute the SELECT statement
    return cursor.fetchone() #fetch the specified project

#update details of a specific project belonging to a specific user (updateproject.py)
def update_project_query(
    cursor, title, description, duration, agency, budget,
    status, project_id, user_id
):
    query = """
        UPDATE projects
        SET title = %s,
            description = %s,
            duration = %s,
            agency = %s,
            budget = %s,
            status = %s
        WHERE project_id = %s
          AND user_id = %s
    """

    cursor.execute(query, (
        title,
        description,
        duration,
        agency,
        budget,
        status,
        project_id,
        user_id
    )) #execute the UPDATE statement

#delete a specific project belonging to a specific user (deleteproject.py)
def delete_project_query(cursor, project_id, user_id):
    query = """
        DELETE FROM projects
        WHERE project_id = %s AND user_id = %s
    """

    cursor.execute(query, (project_id, user_id)) #execute the DELETE statement

#fetch details of a specific user (profile.py)
def get_user_by_id(cursor, user_id):
    query = """
        SELECT user_id, name, username, email
        FROM users
        WHERE user_id = %s
    """
    cursor.execute(query, (user_id,)) #execute the SELECT statement
    return cursor.fetchone() #fetch the specified user

# update details of a specific user (profile.py)
def update_user_query(cursor, user_id, name, email):
    query = """
        UPDATE users
        SET name = %s,
            email = %s
        WHERE user_id = %s
    """

    cursor.execute(query, (name, email, user_id)) #execute the UPDATE statement

#insert feedback submitted by a user (feedback.py)
def create_feedback(cursor, user_id, name, email, message):
    query = """
        INSERT INTO feedback
            (user_id, name, email, message)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(
        query,
        (user_id, name, email, message)
    ) #execute the INSERT statement