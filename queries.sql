-- 0. Query to get Standings for the season
SELECT 
    s.table_position AS Position,
    t.team_name AS Team,
    s.points AS Points
FROM standings s
JOIN teams t ON s.team_id = t.team_id
GROUP BY t.team_name, s.table_position, s.points
ORDER BY s.table_position ASC;

-- 1. Query to find Top-Scoring Stadiums
SELECT 
    m.stadium,
    t.team_name AS home_team,
    t.city,
    SUM(m.home_score + m.away_score) AS total_goals
FROM Matches m
JOIN Teams t ON m.stadium = t.stadium
GROUP BY m.stadium, t.team_name, t.city
ORDER BY total_goals DESC;

-- 2. Home Standings Query
SELECT 
    t.team_name AS team,
    COUNT(*) AS home_matches_played,
    SUM(CASE WHEN m.result = 'home' THEN 1 ELSE 0 END) AS home_wins,
    SUM(CASE WHEN m.result = 'draw' THEN 1 ELSE 0 END) AS home_draws,
    SUM(CASE WHEN m.result = 'away' THEN 1 ELSE 0 END) AS home_losses,
    SUM(m.home_score) AS goals_scored_at_home,
    SUM(m.away_score) AS goals_conceded_at_home,
    SUM(
        CASE 
            WHEN m.result = 'home' THEN 3
            WHEN m.result = 'draw' THEN 1
            ELSE 0
        END
    ) AS home_points
FROM Matches m
JOIN Teams t ON m.home_team_id = t.team_id
GROUP BY t.team_name
ORDER BY home_points DESC, goals_scored_at_home DESC;

-- 3. Away Standings Query
SELECT 
    t.team_name AS team,
    COUNT(*) AS away_matches_played,
    SUM(CASE WHEN m.result = 'away' THEN 1 ELSE 0 END) AS away_wins,
    SUM(CASE WHEN m.result = 'draw' THEN 1 ELSE 0 END) AS away_draws,
    SUM(CASE WHEN m.result = 'home' THEN 1 ELSE 0 END) AS away_losses,
    SUM(m.away_score) AS goals_scored_away,
    SUM(m.home_score) AS goals_conceded_away,
    SUM(
        CASE 
            WHEN m.result = 'away' THEN 3
            WHEN m.result = 'draw' THEN 1
            ELSE 0
        END
    ) AS away_points
FROM Matches m
JOIN Teams t ON m.away_team_id = t.team_id
GROUP BY t.team_name
ORDER BY away_points DESC, goals_scored_away DESC;

-- 4. Query to List the Longest Winning Streak for Each Team
WITH TeamResults AS (
    SELECT 
        team_id,
        match_date,
        result,
        ROW_NUMBER() OVER (PARTITION BY team_id ORDER BY match_date) -
        ROW_NUMBER() OVER (PARTITION BY team_id, result = 'win' ORDER BY match_date) AS win_streak_group
    FROM (
        SELECT 
            match_date,
            home_team_id AS team_id,
            CASE WHEN result = 'home' THEN 'win' ELSE 'not_win' END AS result
        FROM Matches
        UNION ALL
        SELECT 
            match_date,
            away_team_id AS team_id,
            CASE WHEN result = 'away' THEN 'win' ELSE 'not_win' END AS result
        FROM Matches
    ) subquery
),
Streaks AS (
    SELECT 
        team_id,
        win_streak_group,
        COUNT(*) AS streak_length
    FROM TeamResults
    WHERE result = 'win'
    GROUP BY team_id, win_streak_group
)
SELECT 
    t.team_name,
    MAX(s.streak_length) AS longest_streak
FROM Streaks s
JOIN Teams t ON s.team_id = t.team_id
GROUP BY t.team_name
ORDER BY longest_streak DESC;
