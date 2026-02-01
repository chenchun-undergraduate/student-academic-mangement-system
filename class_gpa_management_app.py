from tkinter import *
from tkinter import ttk, messagebox, filedialog
# import pymysql
from datetime import datetime
# from db_connection import get_connection
from backend_code import *
import csv



# --------------- used to quick connect with datatbase ---------------------------
# def get_connection():
    
#     return pymysql.connect(
#         host='localhost',
#         user='root',
#         password='12345678',
#         database='Class_GPA_Management_SYS_db',
#         charset='utf8mb4',
#     )


# ---------------- return the unlock course row(tuple) with a list satisfy 
# ---------------- prerequisite courses GPA >= 2.4 or 'InProgress'
# ---------------- and the grades_current.grade_id = NULL means no course record before 
# def fetch_unlocked_courses():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute('''
#     SELECT
#         c.course_id,
#         c.course_code,
#         c.course_name,
#         c.credit
#     FROM
#         courses AS c
#     LEFT JOIN
#         course_prerequisites AS p
#         ON c.course_id = p.course_id
#     LEFT JOIN
#         grades_current AS g_pre
#         ON p.prereq_course_id = g_pre.course_id
#     LEFT JOIN
#         grades_current AS g_self
#         ON c.course_id = g_self.course_id
#     WHERE
#         g_self.grade_id IS NULL
#     GROUP BY
#         c.course_id
#     HAVING
#         COUNT(p.prereq_course_id) =
#         SUM(
#             CASE
#                 WHEN p.prereq_course_id IS NULL THEN 1
#                 WHEN g_pre.grade_point >= 2.4 OR g_pre.status = 'InProgress' THEN 1
#                 ELSE 0
#             END
#         )
#     ORDER BY
#         c.course_id;
#     ''')
#     rows = cur.fetchall()
#     conn.close()
#     return rows


# # --------------- back the information of prerequisite course row(tuple) when we click the course list
# # --------------- we first set prereq_course_id.course_id = course we select
# # --------------- and we then get the prereq_course_id.prereq_course_id = course.course_id
# # --------------- to get the prerequisite information in the course
# def get_prereqs_for_course(course_id):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT p.prereq_course_id, c.course_code, c.course_name
#         FROM course_prerequisites p
#         JOIN courses c ON p.prereq_course_id = c.course_id
#         WHERE p.course_id = %s
#     """, (course_id,))
#     rows = cur.fetchall()
#     conn.close()
#     return rows


# # ----------------- Delete a course row by course_id.
# def delete_course_by_id(course_id):

#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute('''DELETE FROM courses WHERE course_id = %s''', (course_id,))
#     conn.commit()
#     conn.close()

# # ---------------- use to return the course list 
# # ---------------- combine courses table with grade_current table
# def fetch_courses_with_grade():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute('''
#         SELECT c.course_id, c.course_code, c.course_name, c.credit,
#                g.grade_point, g.term, g.status
#         FROM courses c
#         LEFT JOIN grades_current g ON g.course_id = c.course_id
#         ORDER BY c.course_id
#     ''')
#     rows = cur.fetchall()
#     conn.close()
#     return rows

# # ---------------- courses that already have GPA in grades_current (grade_point not null)
# def fetch_courses_with_gpa_only():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute('''
#         SELECT c.course_code, c.course_name, c.credit,
#                g.grade_point, g.term, g.status, g.comment
#         FROM grades_current g
#         JOIN courses c ON g.course_id = c.course_id
#         WHERE g.grade_point IS NOT NULL
#         ORDER BY c.course_id
#     ''')
#     rows = cur.fetchall()
#     conn.close()
#     return rows

# # ---------------- return the grade change(normal/ retake/ correction/ inprogress)
# # ---------------- history for selected course
# def fetch_grade_history(course_id):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute('''
#         SELECT change_time, change_type,
#                old_grade_point,
#                new_grade_point,
#                comment
#         FROM grade_changes
#         WHERE course_id = %s
#         ORDER BY change_time DESC
#     ''', (course_id,))
#     rows = cur.fetchall()
#     conn.close()
#     return rows


# # ---------------- save the change(insert/update) in the current_grade table
# # ---------------- in localhost we use trigger to catch the change
# # ---------------- a new insert in grade_current -----> insert_trigger
# # ---------------- a update in grade_current ---------> update_trigger
# def update_grade_with_log(course_id, new_grade_point, term, change_type, comment):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute('''
#         SELECT grade_id, grade_point
#         FROM grades_current
#         WHERE course_id = %s
#     ''', (course_id,))
#     row = cur.fetchone()

#     now = datetime.now()

#     if row:
#         # we have a record for this course in grade_current
#         grade_id, old_gpa = row
#         cur.execute('''
#             UPDATE grades_current
#             SET grade_point = %s,
#                 term = %s,
#                 status = %s,
#                 comment = %s,
#                 updated_at = %s
#             WHERE grade_id = %s
#         ''', (new_grade_point, term,
#               change_type, comment, now, grade_id))
#     else:
#         # we don't have record for this course in grade_current
#         cur.execute('''
#             INSERT INTO grades_current
#                 (course_id, grade_point, term, status, comment, updated_at)
#             VALUES
#                 (%s, %s, %s, %s, %s, %s)
#         ''', (course_id, new_grade_point,
#               term, change_type, comment, now))
#     conn.commit()
#     conn.close()


# # ---------------- back the sum(GPA),sum(credit) where the row of grade_current IS NOT NULL
# def calculate_cumulative_gpa():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute('''
#         SELECT
#             SUM(g.grade_point * c.credit) AS total_points,
#             SUM(c.credit) AS total_credits
#         FROM grades_current g
#         JOIN courses c ON g.course_id = c.course_id
#         WHERE g.grade_point IS NOT NULL
#     ''')
#     row = cur.fetchone()
#     conn.close()

#     if not row:
#         return 0.0

#     total_points, total_credits = row
#     if not total_credits or total_credits == 0:
#         return 0.0
#     return float(total_points) / float(total_credits)


# --------------- GUI ---------------------
class GPAApp:
    # -------------- Tkinter-based frontend that orchestrates course display, grade entry, and GPA insights
    def __init__(self, root):
        self.root = root
        self.root.title("Class GPA Management System with Retake & Prerequisites")
        self.root.geometry("1100x650")

        self.selected_course_id = None
        self.selected_course_text = "(None)"

        self.build_widgets()
        self.refresh_all()

    # --------------- UI construction ---------------

    def build_widgets(self):
        title = Label(self.root, text="Class GPA Management System", font=("Arial", 18))
        title.pack(pady=10)

        main_frame = Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Left: course list with current grade
        left_frame = Frame(main_frame)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True)

        lbl_selected = Label(left_frame, text="Selected course: ")
        lbl_selected.pack(anchor=W)
        self.lbl_selected = lbl_selected

        columns = ("code", "name", "credit", "gpa", "term", "status")
        self.tree_courses = ttk.Treeview(
            left_frame, columns=columns, show="headings", height=15
        )
        self.tree_courses.heading("code", text="Code")
        self.tree_courses.heading("name", text="Course Name")
        self.tree_courses.heading("credit", text="Credit")
        self.tree_courses.heading("gpa", text="GPA")
        self.tree_courses.heading("term", text="Term")
        self.tree_courses.heading("status", text="Status")

        self.tree_courses.column("code", width=80)
        self.tree_courses.column("name", width=200)
        self.tree_courses.column("credit", width=60)
        self.tree_courses.column("gpa", width=70)
        self.tree_courses.column("term", width=80)
        self.tree_courses.column("status", width=90)

        self.tree_courses.pack(fill=BOTH, expand=True)
        self.tree_courses.bind("<<TreeviewSelect>>", self.on_course_select)

        btn_refresh = Button(left_frame, text="Refresh", command=self.refresh_all)
        btn_refresh.pack(pady=5)

        # Right side (top): add course
        right_frame = Frame(main_frame)
        right_frame.pack(side=LEFT, fill=Y, padx=10)

        frame_add = LabelFrame(right_frame, text="Delete Course")
        frame_add.pack(fill=X, pady=5)

        Label(frame_add, text="please select course in the list").grid(row=0, column=0, columnspan=2, padx=2, pady=4)

        Button(frame_add, text="Delete Selected Course", command=self.on_delete_course).grid(
            row=1, column=0, columnspan=2, pady=5
        )

        # Right side (middle): grade / retake
        frame_grade = LabelFrame(right_frame, text="Record / Update Grade (including Retake / InProgress)")
        frame_grade.pack(fill=X, pady=5)

        Label(frame_grade, text="GPA:").grid(row=0, column=0, sticky=E, padx=2, pady=2)
        Label(frame_grade, text="Term:").grid(row=1, column=0, sticky=E, padx=2, pady=2)
        Label(frame_grade, text="Type:").grid(row=2, column=0, sticky=E, padx=2, pady=2)
        Label(frame_grade, text="Comment:").grid(row=3, column=0, sticky=NE, padx=2, pady=2)

        self.var_gp = StringVar()
        self.var_term = StringVar()
        self.var_type = StringVar(value="Normal")

        Entry(frame_grade, textvariable=self.var_gp, width=10).grid(row=0, column=1, pady=2)
        Entry(frame_grade, textvariable=self.var_term, width=10).grid(row=1, column=1, pady=2)

        self.combo_type = ttk.Combobox(
            frame_grade,
            textvariable=self.var_type,
            values=["Normal", "Retake", "Correction", "InProgress"],
            state="readonly",
            width=12
        )
        self.combo_type.grid(row=2, column=1, pady=2)

        self.txt_comment = Text(frame_grade, width=25, height=4)
        self.txt_comment.grid(row=3, column=1, pady=2)

        Button(frame_grade, text="Save Grade", command=self.on_save_grade).grid(
            row=4, column=0, columnspan=2, pady=5
        )

        # Right side (bottom top): GPA summary
        frame_gpa = LabelFrame(right_frame, text="Cumulative GPA")
        frame_gpa.pack(fill=X, pady=5)

        self.lbl_gpa = Label(frame_gpa, text="Current GPA: 0.00")
        self.lbl_gpa.pack(side=LEFT, padx=5, pady=5)

        Button(frame_gpa, text="Calculate GPA", command=self.on_calc_gpa).pack(
            side=RIGHT, padx=5, pady=5
        )
        Button(frame_gpa, text="Export GPA CSV", command=self.on_export_csv).pack(
            side=RIGHT, padx=5, pady=5
        )

        # Right side (bottom): unlocked courses
        frame_unlock = LabelFrame(right_frame, text="Unlocked Courses (Prerequisites Satisfied)")
        frame_unlock.pack(fill=X, pady=5)

        self.tree_unlock = ttk.Treeview(
            frame_unlock,
            columns=("code", "name", "credit"),
            show="headings", height=5
        )
        self.tree_unlock.heading("code", text="Code")
        self.tree_unlock.heading("name", text="Course Name")
        self.tree_unlock.heading("credit", text="Credit")
        self.tree_unlock.column("code", width=80)
        self.tree_unlock.column("name", width=150)
        self.tree_unlock.column("credit", width=60)
        self.tree_unlock.pack(fill=X, expand=False)
        # Bottom: prerequisites of selected course
        prereq_frame = LabelFrame(self.root, text="Prerequisites for Selected Course")
        prereq_frame.pack(fill=X, padx=10, pady=5)

        self.tree_prereq = ttk.Treeview(
            prereq_frame,
            columns=("code", "name"),
            show="headings",
            height=4
        )
        self.tree_prereq.heading("code", text="Prereq Code")
        self.tree_prereq.heading("name", text="Prereq Name")
        self.tree_prereq.column("code", width=100)
        self.tree_prereq.column("name", width=250)
        self.tree_prereq.pack(fill=X, expand=False)

        # Bottom: grade history
        history_frame = LabelFrame(self.root, text="Grade Change History for Selected Course")
        history_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        cols_hist = ("time", "type", "old_gpa", "new_gpa", "comment")
        self.tree_history = ttk.Treeview(
            history_frame, columns=cols_hist, show="headings", height=6
        )
        self.tree_history.heading("time", text="Time")
        self.tree_history.heading("type", text="Type")
        self.tree_history.heading("old_gpa", text="Old GPA")
        self.tree_history.heading("new_gpa", text="New GPA")
        self.tree_history.heading("comment", text="Comment")

        self.tree_history.column("time", width=130)
        self.tree_history.column("type", width=80)
        self.tree_history.column("old_gpa", width=70)
        self.tree_history.column("new_gpa", width=70)
        self.tree_history.column("comment", width=200)

        self.tree_history.pack(fill=BOTH, expand=True)

    # --------------- Refresh functions ---------------

    def refresh_all(self):
        self.refresh_course_table()
        self.refresh_unlocked_courses()
        self.refresh_grade_history()
        self.refresh_prereq_table()

    def refresh_course_table(self):
        for item in self.tree_courses.get_children():
            self.tree_courses.delete(item)
        rows = fetch_courses_with_grade()
        for (cid, code, name, credit, gpa, term, status) in rows:
            self.tree_courses.insert(
                "", END, iid=str(cid),
                values=(
                    code or "",
                    name,
                    float(credit) if credit is not None else "",
                    gpa if gpa is not None else "",
                    term or "",
                    status or ""
                )
            )

    def refresh_unlocked_courses(self):
        for item in self.tree_unlock.get_children():
            self.tree_unlock.delete(item)
        rows = fetch_unlocked_courses()
        for (cid, code, name, credit) in rows:
            self.tree_unlock.insert(
                "", END, iid=str(cid),
                values=(code or "", name, float(credit) if credit is not None else "")
            )

    def refresh_prereq_table(self):
        # clear table 
        for item in self.tree_prereq.get_children():
            self.tree_prereq.delete(item)

        if not self.selected_course_id:
            return

        rows = get_prereqs_for_course(self.selected_course_id)
        for pid, code, name in rows:
            self.tree_prereq.insert(
                "", END,
                values=(code or "", name or "")
            )


    def refresh_grade_history(self):
        # Clear history table
        for item in self.tree_history.get_children():
            self.tree_history.delete(item)
        if not self.selected_course_id:
            return
        rows = fetch_grade_history(self.selected_course_id)
        for (t, typ, old_gpa, new_gpa, cmt) in rows:
            self.tree_history.insert(
                "", END,
                values=(
                    t or "",
                    typ or "",
                    old_gpa if old_gpa is not None else "",
                    new_gpa if new_gpa is not None else "",
                    cmt or ""
                )
            )

    # --------------- Event handlers ---------------

    def on_course_select(self, event):
        """
        Update selection state when the user chooses a course in the table,
        then refresh prerequisite and history sections tied to that course.
        """
        selected = self.tree_courses.selection()
        if not selected:
            self.selected_course_id = None
            self.selected_course_text = "(None)"
            self.lbl_selected.config(text=self.selected_course_text)
            self.refresh_grade_history()
            self.refresh_prereq_table()
            return

        cid = int(selected[0])
        self.selected_course_id = cid

        values = self.tree_courses.item(selected[0], "values")
        code, name = values[0], values[1]
        self.selected_course_text = f"[{cid}] {code} - {name}"
        self.lbl_selected.config(text=self.selected_course_text)

        self.refresh_grade_history()
        self.refresh_prereq_table()

    # ---------------- response to the delete course button ------------------------------------
    def on_delete_course(self):
        if not self.selected_course_id:
            messagebox.showwarning("Warning", "Please select the course you want to delete on the left.")
            return

        if not messagebox.askyesno("Confirm", "Confirm deletion of selected courses? This operation is irreversible."):
            return

        try:
            delete_course_by_id(self.selected_course_id)
            messagebox.showinfo("Success", "The course has been deleted.")
            self.selected_course_id = None
            self.selected_course_text = "(None)"
            self.lbl_selected.config(text=self.selected_course_text)
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", f"Deletion failed:\n{e}")

    # ---------------------------------- Response to the save grade buttton ---------------------------
    def on_save_grade(self):
        """
        Validate GPA form input, convert number, and persist via
        update_grade_with_log. Provides user feedback and resets the form
        on success.
        """
        if not self.selected_course_id:
            messagebox.showwarning("Warning", "Please select a course on the left.")
            return

        gp_str = self.var_gp.get().strip()
        term = self.var_term.get().strip()
        change_type = self.var_type.get()
        comment = self.txt_comment.get("1.0", END).strip() or None

        if change_type != "InProgress":
            if not gp_str:
                messagebox.showwarning("Warning", "GPA is required (unless InProgress).")
                return

        new_grade_point = None

        if gp_str:
            try:
                new_grade_point = float(gp_str)
            except ValueError:
                messagebox.showwarning("Warning", "GPA must be a number.")
                return

        if not term:
            term = None

        try:
            update_grade_with_log(
                self.selected_course_id,
                new_grade_point,
                term,
                change_type,
                comment
            )
            messagebox.showinfo("Success", "Grade saved.")
            self.var_gp.set("")
            self.var_term.set("")
            self.var_type.set("Normal")
            self.txt_comment.delete("1.0", END)
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save grade:\n{e}")

    # --------------- Response to the Gaculate GPA button -----------------------
    def on_calc_gpa(self):
        try:
            gpa = calculate_cumulative_gpa()
            self.lbl_gpa.config(text=f"Current GPA: {gpa:.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate GPA:\n{e}")

    # --------------- Export GPA CSV -----------------------
    def on_export_csv(self):
        try:
            rows = fetch_courses_with_gpa_only()
        except Exception as e:
            messagebox.showerror("Error", f"Data retrieval failed：\n{e}")
            return

        if not rows:
            messagebox.showinfo("Info", "No GPA records are available for export.")
            return

        path = filedialog.asksaveasfilename(
            title="Export GPA CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="courses_with_gpa.csv"
        )
        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Course Code", "Course Name", "Credit", "GPA", "Term", "Status", "Comment"])
                for code, name, credit, gpa, term, status, comment in rows:
                    writer.writerow([
                        code or "",
                        name or "",
                        float(credit) if credit is not None else "",
                        gpa if gpa is not None else "",
                        term or "",
                        status or "",
                        comment or ""
                    ])
            messagebox.showinfo("Success", f"Export successful")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: \n{e}")


if __name__ == "__main__":
    root = Tk()
    app = GPAApp(root)
    root.mainloop()
