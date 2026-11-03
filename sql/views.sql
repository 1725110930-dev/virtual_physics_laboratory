-- Vistas para leaderboard y avance por grupo.
-- En la base actual de Supabase estas vistas NO existen todavía.
-- Ejecuta este archivo en el SQL Editor de Supabase.

CREATE OR REPLACE VIEW view_leaderboard AS
SELECT
    u.user_id AS student_id,
    CONCAT(u.first_name, ' ', u.last_name) AS student_name,
    g.name AS group_name,
    dp.name AS degree_program_name,
    MAX(la.xp_earned) AS max_xp
FROM users u
JOIN group_students gs ON u.user_id = gs.student_id
JOIN groups g ON gs.group_id = g.group_id
JOIN degree_programs dp ON g.degree_program_id = dp.degree_program_id
JOIN group_lab_assignments gla ON g.group_id = gla.group_id
JOIN lab_attempts la
    ON gla.group_lab_assignment_id = la.group_lab_assignment_id
   AND la.student_id = u.user_id
WHERE u.role = 'STUDENT' AND u.is_active = TRUE
GROUP BY u.user_id, u.first_name, u.last_name, g.name, dp.name
ORDER BY max_xp DESC;

CREATE OR REPLACE VIEW view_group_progress AS
SELECT
    g.group_id,
    g.professor_id,
    u.user_id AS student_id,
    CONCAT(u.first_name, ' ', u.last_name) AS student_name,
    COALESCE(MAX(la.xp_earned), 0) AS best_xp
FROM group_students gs
JOIN users u ON gs.student_id = u.user_id
JOIN groups g ON gs.group_id = g.group_id
LEFT JOIN group_lab_assignments gla ON g.group_id = gla.group_id
LEFT JOIN lab_attempts la
    ON gla.group_lab_assignment_id = la.group_lab_assignment_id
   AND la.student_id = u.user_id
GROUP BY g.group_id, g.professor_id, u.user_id, u.first_name, u.last_name;
