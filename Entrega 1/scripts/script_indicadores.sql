-- Creditos por estudiante en semestre
SELECT us_fname, us_lname, us_doc, us_doc_type, dt_year, dt_semester, SUM(sb_credits) as total_credits FROM `Enrolled_in_fact` join `User_dimension` on (en_us_id = us_id) join `Subject_dimension` on (en_sb_id = sb_id) join `Date_dimension` on (en_dt_id = dt_id) WHERE us_role = 'estudiante' GROUP BY us_id, dt_year, dt_semester;
-- Creditos por estudiante completo
SELECT us_fname, us_lname, us_doc, us_doc_type, AVG(sb_credits) as total_credits FROM `Enrolled_in_fact` join `User_dimension` on (en_us_id = us_id) join `Subject_dimension` on (en_sb_id = sb_id) WHERE us_role = 'estudiante' GROUP BY us_id;
-- Creditos por estudiante en programa
SELECT us_program_name, dt_year, dt_semester, AVG(sb_credits) as avg_credits_per_program FROM `Enrolled_in_fact` join `User_dimension` on (en_us_id = us_id) join `Subject_dimension` on (en_sb_id = sb_id) join `Date_dimension` on (en_dt_id = dt_id) WHERE us_role = 'estudiante' GROUP BY us_program_name, dt_year, dt_semester;
-- Cursos que dicta un profesor en semestre
SELECT us_fname, us_lname, us_doc, us_doc_type, dt_year, dt_semester, count(sb_id) as total_subjects from Enrolled_in_fact join User_dimension on (us_id = en_us_id) join Subject_dimension on (en_sb_id=sb_id) join Date_dimension on (en_dt_id = dt_id) where us_role = 'profesor' GROUP by us_id, dt_year, dt_semester;
-- Cursos que dicta un profesor en completo
SELECT us_fname, us_lname, us_doc, us_doc_type, AVG(sb_credits) as avg_subjects_per_teacher FROM `Enrolled_in_fact` join `User_dimension` on (en_us_id = us_id) join `Subject_dimension` on (en_sb_id = sb_id) WHERE us_role = 'profesor' GROUP BY us_id;
-- Promedio nota estudiantes en semestre
SELECT us_fname, us_lname, us_doc, us_doc_type, dt_year, dt_semester, AVG(gr_score) as total_score FROM `Grades_fact` join `User_dimension` on (gr_us_id = us_id) join `Date_dimension` on (gr_dt_id = dt_id) WHERE us_role = 'estudiante' GROUP BY us_id, dt_year, dt_semester;
-- Promedio nota estudiantes en completo
SELECT us_fname, us_lname, us_doc, us_doc_type, AVG(gr_score) as total_score FROM `Grades_fact` join `User_dimension` on (gr_us_id = us_id) WHERE us_role = 'estudiante' GROUP BY us_id;
-- Promedio nota estudiantes en el semestre por programa
SELECT us_program_name, dt_year, dt_semester, AVG(gr_score) as avg_score_per_program FROM `Grades_fact` join `User_dimension` on (gr_us_id = us_id) join `Date_dimension` on (gr_dt_id = dt_id) WHERE us_role = 'estudiante' GROUP BY us_program_name, dt_year, dt_semester;
-- Promedio nota estudiantes en el semestre por facultad
SELECT us_faculty_name, dt_year, dt_semester, AVG(gr_score) as avg_score_per_faculty FROM `Grades_fact` join `User_dimension` on (gr_us_id = us_id) join `Date_dimension` on (gr_dt_id = dt_id) WHERE us_role = 'estudiante' GROUP BY us_faculty_name, dt_year, dt_semester;

-- Horas de uso de espacios en semestre
SELECT cr_number, cr_name, cr_building_number, cr_building_name, SUM(TIMEDIFF(en_fhour, en_shour)) AS total_hours FROM `Enrolled_in_fact` join `Classroom_dimension` on (en_cr_id = cr_id) GROUP BY cr_id;

-- Cantidad de estudiantes en semestre
SELECT dt_year, dt_semester, COUNT(us_id) as total_students FROM `Enrolled_in_fact` join `Date_dimension` on (en_dt_id = dt_id) join `User_dimension` on (en_us_id = us_id) WHERE us_role = 'estudiante' GROUP BY dt_year, dt_semester ORDER BY dt_year;
-- Cantidad de estudiantes en programa
SELECT us_program_name, dt_year, dt_semester, COUNT(us_id) as total_students FROM `Enrolled_in_fact` join `Date_dimension` on (en_dt_id = dt_id) join `User_dimension` on (en_us_id = us_id) WHERE us_role = 'estudiante' GROUP BY us_program_name, dt_year, dt_semester ORDER BY dt_year, us_program_name;
-- Cantidad de estudiantes en facultad
SELECT us_faculty_name, dt_year, dt_semester, COUNT(us_id) as total_students FROM `Enrolled_in_fact` join `Date_dimension` on (en_dt_id = dt_id) join `User_dimension` on (en_us_id = us_id) WHERE us_role = 'estudiante' GROUP BY us_faculty_name, dt_year, dt_semester ORDER BY dt_year;
-- Cantidad de estudiantes en materia
SELECT sb_name, dt_year, dt_semester, COUNT(us_id) as total_students FROM `Enrolled_in_fact` join `Date_dimension` on (en_dt_id = dt_id) join `User_dimension` on (en_us_id = us_id) join `Subject_dimension` on (en_sb_id = sb_id) WHERE us_role = 'estudiante' GROUP BY sb_name, dt_year, dt_semester ORDER BY dt_year;

-- cantidad de materias por semestre
SELECT dt_year, dt_semester, COUNT(sb_id) as total_subjects FROM `Enrolled_in_fact` join `Date_dimension` on (en_dt_id = dt_id) join `Subject_dimension` on (en_sb_id = sb_id) GROUP BY dt_year, dt_semester ORDER BY dt_year;

-- Horas de dedicacion por profesor por semestre
SELECT us_fname, us_lname, dt_year, dt_semester, FLOOR(SUM(TIME_TO_SEC(TIMEDIFF(en_fhour, en_shour))/3600)) AS total_hours FROM `Enrolled_in_fact` join `User_dimension` on (en_us_id = us_id) join `Date_dimension` on (en_dt_id = dt_id) WHERE us_role = 'profesor' GROUP BY us_id, dt_year, dt_semester ORDER BY dt_year;
-- Horas de dedicacion profesores por programa
SELECT us_program_name, dt_year, dt_semester, FLOOR(SUM(TIME_TO_SEC(TIMEDIFF(en_fhour, en_shour))/3600)) AS total_hours FROM `Enrolled_in_fact` join `User_dimension` on (en_us_id = us_id) join `Date_dimension` on (en_dt_id = dt_id) WHERE us_role = 'profesor' GROUP BY us_program_name, dt_year, dt_semester ORDER BY dt_year;
-- Horas de dedicacion profesores por facultad
SELECT us_faculty_name, dt_year, dt_semester, FLOOR(SUM(TIME_TO_SEC(TIMEDIFF(en_fhour, en_shour))/3600)) AS total_hours FROM `Enrolled_in_fact` join `User_dimension` on (en_us_id = us_id) join `Date_dimension` on (en_dt_id = dt_id) WHERE us_role = 'profesor' GROUP BY us_faculty_name, dt_year, dt_semester ORDER BY dt_year;