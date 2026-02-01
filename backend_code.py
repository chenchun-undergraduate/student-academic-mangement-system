from db_connection import get_connection

def fetch_unlocked_courses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
    SELECT
        c.course_id,
        c.course_code,
        c.course_name,
        c.credit
    FROM
        courses AS c
    LEFT JOIN
        course_prerequisites AS p
        ON c.course_id = p.course_id
    LEFT JOIN
        grades_current AS g_pre
        ON p.prereq_course_id = g_pre.course_id
    LEFT JOIN
        grades_current AS g_self
        ON c.course_id = g_self.course_id
    WHERE
        g_self.grade_id IS NULL
    GROUP BY
        c.course_id
    HAVING
        COUNT(p.prereq_course_id) =
        SUM(
            CASE
                WHEN p.prereq_course_id IS NULL THEN 1
                WHEN g_pre.grade_point >= 2.4 OR g_pre.status = 'InProgress' THEN 1
                ELSE 0
            END
        )
    ORDER BY
        c.course_id;
    ''')
    rows = cur.fetchall()
    conn.close()
    return rows


# --------------- back the information of prerequisite course row(tuple) when we click the course list
# --------------- we first set prereq_course_id.course_id = course we select
# --------------- and we then get the prereq_course_id.prereq_course_id = course.course_id
# --------------- to get the prerequisite information in the course
def get_prereqs_for_course(course_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.prereq_course_id, c.course_code, c.course_name
        FROM course_prerequisites p
        JOIN courses c ON p.prereq_course_id = c.course_id
        WHERE p.course_id = %s
    """, (course_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


# ----------------- Delete a course row by course_id.
def delete_course_by_id(course_id):

    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''DELETE FROM courses WHERE course_id = %s''', (course_id,))
    conn.commit()
    conn.close()

# ---------------- use to return the course list 
# ---------------- combine courses table with grade_current table
def fetch_courses_with_grade():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT c.course_id, c.course_code, c.course_name, c.credit,
               g.grade_point, g.term, g.status
        FROM courses c
        LEFT JOIN grades_current g ON g.course_id = c.course_id
        ORDER BY c.course_id
    ''')
    rows = cur.fetchall()
    conn.close()
    return rows

# ---------------- courses that already have GPA in grades_current (grade_point not null)
def fetch_courses_with_gpa_only():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT c.course_code, c.course_name, c.credit,
               g.grade_point, g.term, g.status, g.comment
        FROM grades_current g
        JOIN courses c ON g.course_id = c.course_id
        WHERE g.grade_point IS NOT NULL
        ORDER BY c.course_id
    ''')
    rows = cur.fetchall()
    conn.close()
    return rows

# ---------------- return the grade change(normal/ retake/ correction/ inprogress)
# ---------------- history for selected course
def fetch_grade_history(course_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT change_time, change_type,
               old_grade_point,
               new_grade_point,
               comment
        FROM grade_changes
        WHERE course_id = %s
        ORDER BY change_time DESC
    ''', (course_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


# ---------------- save the change(insert/update) in the current_grade table
# ---------------- in localhost we use trigger to catch the change
# ---------------- a new insert in grade_current -----> insert_trigger
# ---------------- a update in grade_current ---------> update_trigger
def update_grade_with_log(course_id, new_grade_point, term, change_type, comment):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
        SELECT grade_id, grade_point
        FROM grades_current
        WHERE course_id = %s
    ''', (course_id,))
    row = cur.fetchone()

    now = datetime.now()

    if row:
        # we have a record for this course in grade_current
        grade_id, old_gpa = row
        cur.execute('''
            UPDATE grades_current
            SET grade_point = %s,
                term = %s,
                status = %s,
                comment = %s,
                updated_at = %s
            WHERE grade_id = %s
        ''', (new_grade_point, term,
              change_type, comment, now, grade_id))
    else:
        # we don't have record for this course in grade_current
        cur.execute('''
            INSERT INTO grades_current
                (course_id, grade_point, term, status, comment, updated_at)
            VALUES
                (%s, %s, %s, %s, %s, %s)
        ''', (course_id, new_grade_point,
              term, change_type, comment, now))
    conn.commit()
    conn.close()


# ---------------- back the sum(GPA),sum(credit) where the row of grade_current IS NOT NULL
def calculate_cumulative_gpa():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT
            SUM(g.grade_point * c.credit) AS total_points,
            SUM(c.credit) AS total_credits
        FROM grades_current g
        JOIN courses c ON g.course_id = c.course_id
        WHERE g.grade_point IS NOT NULL
    ''')
    row = cur.fetchone()
    conn.close()

    if not row:
        return 0.0

    total_points, total_credits = row
    if not total_credits or total_credits == 0:
        return 0.0
    return float(total_points) / float(total_credits)