SELECT 
    s.table_position AS Position,
    t.team_name AS Team
FROM standings s
JOIN teams t ON s.team_id = t.team_id
GROUP BY t.team_name, s.table_position
ORDER BY s.table_position ASC;
