"""Defines all the functions related to the database"""
from app import db
from sqlalchemy import text
from flask import current_app as app
import random

def fetch_todo() -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute(text("""SELECT e.expId,
    user.firstName,
	user.lastName,
    e.courseId,
	p.semester,
    p.year,
    u.uniName,
    e.blog_exp
    FROM Experiences as e
    LEFT JOIN Programs as p
    ON e.programId = p.programId
    LEFT JOIN Universities as u
    ON p.universityId = u.universityId
    LEFT JOIN Users as user
    ON e.userId = user.userId
    ORDER BY p.end_date DESC;""")).fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "expId": result[0],
            "first_name": result[1],
            "last_name": result[2],
            "course": result[3],
            "semester": result[4],
            "year": result[5],
            "uni": result[6],
            "blog": result[7]
        }
        todo_list.append(item)

    return todo_list


def update_exp_entry(expId: str, first_name: str, last_name: str, course: str, semester: str, year: int) -> None:

    """Updates experience description based on given `expId`

    Args:
        expId (str): unique expId
        first_name (str): First Name
        last_name (str): Last Name
        course (str): Courses
        semester (str): semester
        year (int): year of experience

    Returns:
        None
    """

    conn = db.connect()

    print(expId, first_name, last_name)
    if (first_name) or (last_name):
        query = 'Update Users set firstName = "{}", lastName = "{}" where userId IN (SELECT userId FROM Experiences WHERE expId = "{}");'.format(first_name, last_name, expId)
        conn.execute(text(query))
    if (course):
        query = 'Update Experiences Set courseId = "{}" Where expId = "{}";'.format(course, expId)
        conn.execute(text(query))
    if (semester) or (year):
        query = 'Update Programs set semester = "{}", year = {} where programId IN (SELECT programId FROM Experiences WHERE expId = "{}");'.format(semester, year, expId)
        conn.execute(text(query))
    # if (uni):
    #     update_uni_entry(expId, uni)

    conn.commit()
    conn.close()


# def update_user_entry(expId: str, first_name: str, last_name: str, conn) -> None:
#     """Updates user name based on input
#
#     Args:
#         expId (str): Targeted expId
#         first_name (str): Updated first name
#         last_name (str): Updated last name
#
#     Returns:
#         None
#     """
#     print(expId, first_name, last_name, "update_user_entry")
#
# #     conn = db.connect()
#     query = 'Update Users set firstName = "{}", lastName = "{}" where userId IN (SELECT userId FROM Experiences WHERE expId = "{}");'.format(first_name, last_name, expId)
#     conn.execute(text(query))
# #     conn.commit()
# #     conn.close()
#
#
# def update_course_entry(expId: str, course: str) -> None:
#     """Updates user name based on input
#
#     Args:
#         expId (str): Targeted expId
#         course (str): Updated course
#
#     Returns:
#         None
#     """
#
# #     conn = db.connect()
#     query = 'Update Experiences Set courseId = "{}" Where expId = "{}";'.format(course, expId)
#     conn.execute(text(query))
# #     conn.commit()
# #     conn.close()
#
#
# def update_program_entry(expId: str, semester: str, year: int) -> None:
#     """Updates user name based on input
#
#     Args:
#         expId (str): Targeted expId
#         semester (str): Updated semester
#         year (int): Updated year
#
#     Returns:
#         None
#     """
#
# #     conn = db.connect()
#     query = 'Update Programs set semester = "{}", year = {} where programId IN (SELECT programId FROM Experiences WHERE expId = "{}");'.format(semester, year, expId)
#     conn.execute(text(query))
# #     conn.commit()
# #     conn.close()


# def update_uni_entry(expId: str, uni: str) -> None:
#     """Updates user name based on input

#     Args:
#         expId (str): Targeted expId
#         first_name (str): Updated first name
#         last_name (str): Updated last name

#     Returns:
#         None
#     """

#     conn = db.connect()
#     query = 'Update Users set uniName = "{}" where programId IN (SELECT programId FROM Experiences WHERE expId = "{}");'.format(uni, expId)
#     conn.execute(text(query))
#     conn.commit()
#     conn.close()

def get_next_expId(conn):
    """
    Fetches the last experience ID from the database and calculates the next ID.
    
    Args:
        conn: The database connection object.
        
    Returns:
        The next experience ID as a string.
    """
    # Query to select the last experience ID ordered in descending order.
    last_expId_query ="""
    SELECT expId FROM Experiences
    ORDER BY CAST(SUBSTRING(expId, 2) AS UNSIGNED) DESC
    LIMIT 1;
    """
    last_expId_result = conn.execute(text(last_expId_query)).fetchone()
    
    # Start with a default ID if the table is empty.
    next_id_number = 2000
    if last_expId_result:
        last_expId = last_expId_result[0]
        if last_expId.startswith('E'):
            # Extract the numerical part of the expId and increment it.
            last_id_number = int(last_expId[1:])
            next_id_number = last_id_number + 1
    
    # Combine 'E' with the next ID number to form the new expId.
    next_expId = f"E{next_id_number}"
    return next_expId


def get_next_userID(conn):
    """
    Fetches the last user ID from the database and calculates the next ID.
    
    Args:
        conn: The database connection object.
        
    Returns:
        The next user ID as a string.
    """

    # Query to select the last user ID ordered in descending order.
    last_userId_query = """
    SELECT userId FROM Users
    ORDER BY CAST(SUBSTRING(userId, 2) AS UNSIGNED) DESC
    LIMIT 1;
    """
    last_userId_result = conn.execute(text(last_userId_query)).fetchone()
    # print("what we get", last_userId_result)
    # Start with a default ID if the table is empty.
    print(last_userId_result[0])
    next_id_number = 3000
    if last_userId_result:
        last_userId = last_userId_result[0]
        # print("last_userId", last_userId, type(last_userId))
        if last_userId.startswith('U'):
            # print("it starts with U")
            # Extract the numerical part of the expId and increment it.
            last_id_number = int(last_userId[1:])
            # print("last_id_number", last_id_number, type(last_id_number))
            next_id_number = last_id_number + 1
            # print("next_id_number", next_id_number, type(next_id_number))
    
    # Combine 'U' with the next ID number to form the new expId.
    next_userId = f"U{next_id_number}"
    return next_userId


def get_next_programID(conn):
    """
    Fetches the last program ID from the database and calculates the next ID.
    
    Args:
        conn: The database connection object.
        
    Returns:
        The next program ID as a string.
    """

    # Query to select the last program ID ordered in descending order.
    last_programId_query = """
    SELECT programId FROM Programs
    ORDER BY CAST(SUBSTRING(programId, 2) AS UNSIGNED) DESC
    LIMIT 1;
    """
    last_programId_result = conn.execute(text(last_programId_query)).fetchone()
    next_id_number = 2000
    if last_programId_result:
        last_programId = last_programId_result[0]
        # print("last_userId", last_userId, type(last_userId))
        if last_programId.startswith('P'):
            last_id_number = int(last_programId[1:])
            next_id_number = last_id_number + 1
            # print("next_id_number", next_id_number, type(next_id_number))
    
    # Combine 'P' with the next ID number to form the new expId.
    next_programId = f"P{next_id_number}"
    return next_programId


# Example functions from the TODO APP
def insert_new_task(first_name: str, last_name: str, course: str, semester: str, year: int, uni='UIUC') -> str:
    """Insert new experience into the database.
    Args:
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        course (str): Course ID.
        semester (str): Semester.
        year (int): Year.
        uni (str): University name, default is 'UIUC'.
    Returns:
        The experience ID for the inserted entry.
    """
    conn = db.connect()

    # Generate the next experience ID.
    

    # User schema parameters
    userId = get_next_userID(conn)
    print(userId)
    # homeUni = "00001000"
    rando = random.randint(1, 999)
    homeUni = "00000" + str(rando)
    homeDept = "CS"
    researchInterest = "DP"

    # Insert into Users table.
    # Note: Adjust the following line to match your actual Users table schema.
    conn.execute(text("""
    INSERT INTO Users (userId, firstName, lastName, homeUni, homeDept, researchInterest)
    VALUES (:userId, :first_name, :last_name, :homeUni, :homeDept, :researchInterest);
    """), {
        'userId': userId,
        'first_name': first_name, 
        'last_name': last_name,
        'homeUni': homeUni,
        'homeDept': homeDept,
        'researchInterest': researchInterest
    })
    # conn.commit()
    
    # Get the user ID of the newly inserted user.
    # user_id = conn.execute("SELECT LAST_INSERT_ID();").fetchone()[0]
    # print("just added user_id", user_id)

    
    # Program schema parameters
    programId = get_next_programID(conn)
    if semester == 'Fall':
        start_date = f'{year}-09-01'
        end_date = f'{year}-12-01'
    elif semester == 'Summer':
        start_date = f'{year}-06-01'
        end_date = f'{year}-09-01'
    elif semester == 'Spring':
        start_date = f'{year}-01-01'
        end_date = f'{year}-05-01'
    else :
        start_date = f'{year}-01-01'
        end_date = f'{year}-05-01'

    # Insert into Programs table.
    # Note: Adjust the following line to match your actual Programs table schema.
    conn.execute(text("""
    INSERT INTO Programs (programId, universityId, start_date, end_date, semester, year)
    VALUES (:programId, :universityId, :start_date, :end_date, :semester, :year);
    """), {
        'programId': programId,
        'universityId': homeUni, 
        'start_date': start_date,
        'end_date': end_date,
        'semester': semester,
        'year': year
    })
    # conn.commit()
    print("program id is", programId)
    

    # Get the program ID of the newly inserted program.
    # program_id = conn.execute("SELECT LAST_INSERT_ID();").fetchone()[0]

    # Experience schema parameters
    blog = None
    housingIdQuery = """
    SELECT housingId FROM Housing 
    ORDER BY housingId DESC 
    LIMIT 1;
    """
    housingId = conn.execute(text(housingIdQuery)).fetchone()[0]
    # conn.commit()

    
    expId = get_next_expId(conn)
    print("expId is", expId)
    # input("here")

    # Insert into Experiences table.
    conn.execute(text("""
    INSERT INTO Experiences (expId, programId, userId, courseId, housingId, blog_exp)
    VALUES (:expId, :programId, :userId, :courseId, :housingId, :blog);
    """), {
        'expId': expId,
        'programId': programId, 
        'userId': userId,
        'courseId': course,
        'housingId': housingId,
        'blog': blog
    })
    print("program id is", programId)

    # input("press enter to continue!!!")

    # conn.commit()
    conn.close()

    return expId



def remove_task_by_id(task_id: str) -> None:
    
    # app.logger.info("remove_task_by_id has been called!!!")
    print("remove_task_by_id has been called")

    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From Experiences where expId="{}";'.format(task_id)
    conn.execute(text(query))
    conn.commit()
    conn.close()


def stored_procedure() -> None:
    """ run stored procedure which returns a random uni, subject, and subject percentage"""
    conn = db.connect()
    query = 'CALL GetSubjectProportionsAtRandomUniversity();'
    query_results = conn.execute(text(query)).fetchall()
    conn.close()
    rand_uni = []
    print(query_results)
    for result in query_results:
        item = {
            "university": result[0],
            "subject": result[1],
            "subject_percentage": result[3]
        }
        rand_uni.append(item)

    return rand_uni