<?php

namespace PowerAPI;

/** Raw data goes in, formatted data comes out. You can't explain that. */
class Parser
{
    /**
     * Group an assignment dump by section and merge in its category and score
     * @param array $rawAssignments assignment dump to be parsed
     * @param array $assignmentCategories array of possible assignment categories
     * @param array $assignmentScores array of assignment scores grouped by ID
     * @return array assignments grouped by section ID
    */
    static public function assignments($rawAssignments, $assignmentCategories, $assignmentScores,$reportingTerms)
    {
        $assignments = Array();

        foreach ($rawAssignments as $assignment) {
            if (!isset($assignments[$assignment->sectionid])) {
                $assignments[$assignment->sectionid] = Array();
            }
            $terms = Array();
            foreach ($reportingTerms as $term){
                $assignmentDate = strtotime($assignment->dueDate);
                if($term->startDate<$assignmentDate && $term->endDate>$assignmentDate){
                    $terms[]=$term->abbr;
                }
            }
            
            $assignments[$assignment->sectionid][] = new Data\Assignment(Array(
                'assignment' => $assignment,
                'category' => $assignmentCategories[$assignment->categoryId],
                'score' => Parser::requireDefined($assignmentScores[$assignment->id]),
                'terms' => array_values(array_unique($terms))
            ));
        }

        return $assignments;
    }

    /** Group an assignmentCategories dump by section ID
     * @param array $rawAssignmentCategories assignment categories dump to be parsed
     * @return array assignment categories grouped by category ID
     */
    static public function assignmentCategories($rawAssignmentCategories)
    {
        $assignmentCategories = Array();

        foreach ($rawAssignmentCategories as $assignmentCategory) {
            $assignmentCategories[$assignmentCategory->id] = $assignmentCategory;
        }

        return $assignmentCategories;
    }

    /** Group an assignmentScores dump by section ID
     * @param array $rawAssignmentScores assignment scores dump to be parsed
     * @return array assignment scores grouped by assignment ID
     */
    static public function assignmentScores($rawAssignmentScores)
    {
        $assignmentScores = Array();

        foreach ($rawAssignmentScores as $assignmentScore) {
            if(!isset($assignmentScore->assignmentId)) continue;
            $assignmentScores[$assignmentScore->assignmentId] = $assignmentScore;
        }

        return $assignmentScores;
    }

    /** Group a finalGrades dump by section ID
     * @param array $rawFinalGrades final grades dump to be parsed
     * @return array final grades grouped by section ID
     */
    static public function finalGrades($rawFinalGrades)
    {
        $finalGrades = Array();

        foreach ($rawFinalGrades as $finalGrade) {
            if (!isset($finalGrades[$finalGrade->sectionid])) {
                $finalGrades[$finalGrade->sectionid] = [];
            }

            $finalGrades[$finalGrade->sectionid][] = $finalGrade;
        }

        return $finalGrades;
    }

    /** Group a reportingTerms dump by term ID
     * @param array $rawReportingTerms reporting terms dump to be parsed
     * @return array reporting terms grouped by term ID
     */
    static public function reportingTerms($rawReportingTerms)
    {
        $reportingTerms = Array();

        foreach ($rawReportingTerms as $reportingTerm) {
            $reportingTerms[$reportingTerm->id] = (object)array(
                "abbr" => $reportingTerm->abbreviation,
                "startDate" => strtotime($reportingTerm->startDate),
                "endDate" => strtotime($reportingTerm->endDate)
            );
        }
        
        return $reportingTerms;
    }

    /** Check if $a should be displayed before or after $b
     * @param array $a section A
     * @param array $b section B
     * @return int -1 if $a should go first, 0 if $a = $b, 1 if $b should go first
     */
    static public function sectionsSort($a, $b)
    {
        if ($a->expression !== $b->expression) {
            return strcmp($a->expression, $b->expression);
        } else {
            return strcmp($a->name, $b->name);
        }
    }

    /** Create a Section object for each section
     * @param array $rawSections sections dump to be parsed
     * @param array $assignments array of assignments grouped by section ID
     * @param array $finalGrades array of final grades grouped by section ID
     * @param array $reportingTerms array of reporting terms grouped by term ID
     * @param array $teachers array of teachers grouped by teacher ID
     * @return array
     */
    static public function sections($rawSections, $assignments, $finalGrades, $reportingTerms, $teachers, $citizenGrades)
    {
        $sections = Array();

        foreach ($rawSections as $section) {
            $sections[] = new Data\Section(Array(
                'assignments' => Parser::requireDefined($assignments[$section->id]),
                'finalGrades' => Parser::requireDefined($finalGrades[$section->id]),
                'reportingTerms' => $reportingTerms,
                'section' => $section,
                'teacher' => $teachers[$section->teacherID],
                'citizenGrades' => $citizenGrades
            ));
        }

        usort($sections, array('PowerAPI\Parser', 'sectionsSort'));

        return $sections;
    }

    /** Group a teachers dump by teacher ID
     * @param array $rawTeachers teachers dump to be parsed
     * @return array teachers grouped by teacher ID
     */
    static public function teachers($rawTeachers)
    {
        $teachers = Array();

        foreach ($rawTeachers as $teacher) {
            $teachers[$teacher->id] = $teacher;
        }

        return $teachers;
    }

    /**
     * Return null if the passed value does not exist or the value if it does
     * @param mixed $value value to be examined and possibly returned
     * @return mixed null or the passed parameter
    */
    static public function requireDefined(&$value)
    {
        if (isset($value)) {
            return $value;
        } else {
            return null;
        }
    }
    
    static public function groupById($raw)
    {
        $items = Array();

        foreach ($raw as $item) {
            $items[$item->id] = $item;
        }
        return $items;
    }
    
    static public function citizenGrades($rawCitizenGrades, $rawCitizenCodes)
    {
        $citizenCodes = Parser::groupById($rawCitizenCodes);
        
        $citizenGrades = Array();
        foreach ($rawCitizenGrades as $citizenGrade) {
            $citizenGrades[$citizenGrade->reportingTermId] = $citizenCodes[$citizenGrade->codeId];
        }
        return $citizenGrades;
    }
    
    static public function attendances($rawAttendances, $attendanceCodes, $raw_sections)
    {
        $attendances = Array();

        $sections=Array();
        foreach ($raw_sections as $section){
            $sections[$section->enrollments->id]=$section;
        }
        if(is_array($rawAttendances)){
            foreach ($rawAttendances as $attendance) {
                $attendances[] = array(
                    "code" => $attendanceCodes[$attendance->attCodeid]->attCode,
                    "description" => $attendanceCodes[$attendance->attCodeid]->description,
                    "date" => $attendance->attDate,
                    "period" => $sections[$attendance->ccid]->expression,
                    "name" => $sections[$attendance->ccid]->schoolCourseTitle
                );
            }
        }else{
                $attendances[] = array(
                    "code" => $attendanceCodes[$rawAttendances->attCodeid]->attCode,
                    "description" => $attendanceCodes[$rawAttendances->attCodeid]->description,
                    "date" => $rawAttendances->attDate,
                    "period" => $sections[$rawAttendances->ccid]->expression,
                    "name" => $sections[$rawAttendances->ccid]->schoolCourseTitle
                );    
            }
        return $attendances;
    }
}
