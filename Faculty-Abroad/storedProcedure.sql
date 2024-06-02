CREATE DEFINER=`root`@`%` PROCEDURE `GetSubjectProportionsAtRandomUniversity`()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_universityId VARCHAR(8);
    DECLARE v_universityName VARCHAR(255);
    DECLARE v_courseId VARCHAR(16);
    DECLARE v_subject VARCHAR(255);
    DECLARE total_courses INT DEFAULT 0;
    DECLARE cur CURSOR FOR 
        SELECT e.courseId
        FROM Universities u
		RIGHT JOIN Programs p ON p.universityId = u.universityId
		JOIN Experiences e ON e.programId = p.programId
        WHERE u.universityId IS NOT NULL AND u.universityId = v_universityId;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Select a random university ID and name with universityId <= '00000999'
    SELECT u.universityId, u.uniName INTO v_universityId, v_universityName 
	FROM Universities u
	JOIN Programs p ON u.universityId = p.universityId
	JOIN Experiences e ON p.programId = e.programId
	WHERE u.universityId <= '00000999' AND e.courseId IS NOT NULL
	GROUP BY u.universityId, u.uniName
	ORDER BY RAND() LIMIT 1;

    -- Initialize temporary table to hold subject proportions
    DROP TEMPORARY TABLE IF EXISTS TempSubjectProportions;
    CREATE TEMPORARY TABLE TempSubjectProportions (
        subject VARCHAR(255),
        subject_count INT DEFAULT 0
    );

    -- Open the cursor
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO v_courseId;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Extract the subject from course_name
        SET v_subject = SUBSTRING_INDEX(v_courseId, ' ', 1);

        -- Insert or update the subject count in the temporary table
        IF (SELECT COUNT(*) FROM TempSubjectProportions WHERE subject = v_subject) > 0 THEN
            UPDATE TempSubjectProportions SET subject_count = subject_count + 1 WHERE subject = v_subject;
        ELSE
            INSERT INTO TempSubjectProportions (subject, subject_count) VALUES (v_subject, 1);
        END IF;
    END LOOP;

    -- Close the cursor
    CLOSE cur;

    -- Calculate the total number of courses
    SELECT SUM(subject_count) INTO total_courses FROM TempSubjectProportions;

    -- Select the subject proportions and university name from the temporary table
    SELECT v_universityName AS university, subject, subject_count, (subject_count / total_courses) * 100 AS subject_percentage
    FROM TempSubjectProportions;

    -- Drop the temporary table
    DROP TEMPORARY TABLE IF EXISTS TempSubjectProportions;
END