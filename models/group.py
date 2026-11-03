from config.database import Database


def list_for_student(student_id):
    """Grupos a los que pertenece un estudiante."""
    return Database.fetch_all(
        """
        SELECT
            g.group_id,
            g.name AS group_name,
            dp.name AS degree_program,
            trim(concat(p.first_name, ' ', p.last_name)) AS professor_name
        FROM group_students gs
        JOIN groups g ON g.group_id = gs.group_id
        JOIN degree_programs dp
            ON dp.degree_program_id = g.degree_program_id
        JOIN users p ON p.user_id = g.professor_id
        WHERE gs.student_id = %s
        ORDER BY g.name
        """,
        (student_id,),
    )


def list_for_professor(professor_id):
    """Grupos que imparte un profesor, con número de alumnos."""
    return Database.fetch_all(
        """
        SELECT
            g.group_id,
            g.name AS group_name,
            g.access_code,
            dp.name AS degree_program,
            count(gs.student_id) AS student_count
        FROM groups g
        JOIN degree_programs dp
            ON dp.degree_program_id = g.degree_program_id
        LEFT JOIN group_students gs ON gs.group_id = g.group_id
        WHERE g.professor_id = %s
        GROUP BY g.group_id, g.name, g.access_code, dp.name
        ORDER BY g.name
        """,
        (professor_id,),
    )
