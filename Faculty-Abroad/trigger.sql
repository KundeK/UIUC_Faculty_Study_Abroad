CREATE TRIGGER AfterExperienceDelete
AFTER DELETE ON Experiences
FOR EACH ROW
BEGIN
    -- Check if the course has more than 0 associated experiences
    IF (OLD.courseId IS NOT NULL AND (SELECT num_students FROM Courses WHERE courseId = OLD.courseId) > 0) THEN
        -- Decrement the num_students counter for the course associated with the experience
        UPDATE Courses
        SET num_students = num_students - 1
        WHERE courseId = OLD.courseId;
    END IF;
END
