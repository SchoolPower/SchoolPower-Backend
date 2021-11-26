import datetime as datetime
import json
from datetime import timezone
from typing import Any

from .model_old import *


def parse_old_api(student_data: Any) -> StudentDataOld:
    assignments_categories = {cat.id: cat for cat in student_data.assignmentCategories}
    scores = {a.assignmentId: a for a in student_data.assignmentScores}
    attendance_codes = {obj.id: obj for obj in student_data.attendanceCodes}
    enrollment_id_to_section = {}
    for section in student_data.sections:
        for enrollment in section.enrollments:
            enrollment_id_to_section[enrollment.id] = section

    instructors = {obj.id: obj for obj in student_data.teachers}
    reporting_terms = {obj.id: obj for obj in student_data.reportingTerms}
    citizen_codes = {obj.id: obj for obj in student_data.citizenCodes}
    citizen_grades = {obj.reportingTermId: citizen_codes[obj.codeId] for obj in student_data.citizenGrades}

    def get_status(assignment, score):
        status = {'includeInFinalGrade': assignment.includeinfinalgrades == 1}
        if score:
            status.update({prop: score[prop]
                           for prop in ['collected', 'exempt', 'incomplete', 'late', 'missing']
                           } if assignment.id in scores else {})
        return status

    def to_date_string(date: datetime):
        if not date:
            return None
        return date.astimezone(timezone.utc).isoformat(timespec='milliseconds')[:-6] + "Z"

    return StudentDataOld(
        information=InformationOld(
            current_g_p_a=student_data.student.currentGPA,
            current_term=student_data.student.currentTerm,
            id=str(student_data.student.id),
            dob=to_date_string(student_data.student.dob),
            first_name=student_data.student.firstName,
            middle_name=student_data.student.middleName,
            last_name=student_data.student.lastName,
            gender=student_data.student.gender,
            photo_date=to_date_string(student_data.student.photoDate),
        ),
        attendances=[AttendanceOld(
            code=attendance_codes[attendance.attCodeid].attCode if attendance.attCodeid in attendance_codes else None,
            date=to_date_string(attendance.attDate),
            description=attendance_codes[
                attendance.attCodeid].description if attendance.attCodeid in attendance_codes else None,
            name=enrollment_id_to_section[
                attendance.ccid].schoolCourseTitle if attendance.ccid in enrollment_id_to_section else None,
            period=enrollment_id_to_section[
                attendance.ccid].expression if attendance.ccid in enrollment_id_to_section else None,
        ) for attendance in student_data.attendance],
        sections=sorted([SectionOld(
            name=section.schoolCourseTitle,
            teacher=SectionOldTeacher(
                first_name=instructors[section.teacherID].firstName,
                last_name=instructors[section.teacherID].lastName,
                email=instructors[section.teacherID].email,
                school_phone=instructors[section.teacherID].schoolPhone,
            ),
            expression=section.expression,
            room_name=section.roomName,
            assignments=[AssignmentOld(
                name=assignment.name,
                date=to_date_string(assignment.dueDate),
                letter_grade=scores[assignment.id].letterGrade if assignment.id in scores else None,
                percent=scores[assignment.id].percent if assignment.id in scores else None,
                score=scores[assignment.id].score if assignment.id in scores else None,
                points_possible=str(assignment.pointspossible),
                category=assignments_categories[assignment.categoryId].name,
                include_in_final_grade=str(assignment.includeinfinalgrades),
                weight=str(assignment.weight),
                terms=list(set(term.abbreviation for term in reporting_terms.values() if
                               term.startDate <= assignment.dueDate <= term.endDate)),
                status=get_status(assignment, scores.get(assignment.id)),
                description=assignment.description,
            ) for assignment in student_data.assignments if assignment.sectionid == section.id],
            final_grades={reporting_terms[grade.reportingTermId].title: SectionOldFinalGrade(
                percent=str(grade.percent),
                letter=grade.grade,
                comment=grade.commentValue.strip('\r\n ') if grade.commentValue else None,
                eval=citizen_grades[
                    grade.reportingTermId].codeName if grade.reportingTermId in citizen_grades else '--',
                start_date=int(reporting_terms[grade.reportingTermId].startDate.timestamp()),
                end_date=int(reporting_terms[grade.reportingTermId].endDate.timestamp()),
            ) for grade in student_data.finalGrades if grade.sectionid == section.id},
            start_date=to_date_string(section.enrollments[0].startDate),
            end_date=to_date_string(section.enrollments[0].endDate),
        ) for section in student_data.sections], key=lambda k: str(k.expression) + str(k.name)),
        additional=AdditionalOld(avatar=""),
    )


if __name__ == '__main__':
    import pickle

    res = parse_old_api(pickle.load(open('student_data', 'rb')).studentDataVOs[0])
    json.dump(res.to_dict(include_default_values=True), open('newapi.json', 'w'), indent=4, ensure_ascii=False)
