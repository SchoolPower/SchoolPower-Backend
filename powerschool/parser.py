import json
from typing import Any

from .model import *


def parse(student_data: Any) -> StudentData:
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

    def get_assignment_grade(id):
        if id not in scores:
            return Grade()
        score = scores[id]
        return Grade(
            percentage=float(score.percent) if id in scores and score.percent else None,
            letter=score.letterGrade if id in scores else None
        )

    def get_mark_for_display(assignment):
        mark = "{:.1f}".format(float(scores[assignment.id].score)) if assignment.id in scores and scores[
            assignment.id].score else '--'
        full_mark = "{:.1f}".format(assignment.pointspossible)
        return f"{mark}/{full_mark}"

    return StudentData(
        profile=Profile(
            gpa=float(student_data.student.currentGPA) if student_data.student.currentGPA else None,
            id=student_data.student.id,
            gender=ProfileGender.MALE if student_data.student.gender == 'M' else ProfileGender.FEMALE,
            dob=int(student_data.student.dob.timestamp() * 1000),
            first_name=student_data.student.firstName,
            middle_name=student_data.student.middleName,
            last_name=student_data.student.lastName,
        ),
        attendances=[Attendance(
            code=attendance_codes[attendance.attCodeid].attCode if attendance.attCodeid in attendance_codes else None,
            date=int(attendance.attDate.timestamp() * 1000),
            description=attendance_codes[
                attendance.attCodeid].description if attendance.attCodeid in attendance_codes else None,
            comment=attendance.attComment,
            course_name=enrollment_id_to_section[
                attendance.ccid].schoolCourseTitle if attendance.ccid in enrollment_id_to_section else None,
            course_block=enrollment_id_to_section[
                attendance.ccid].expression if attendance.ccid in enrollment_id_to_section else None,
        ) for attendance in student_data.attendance],
        disabled_info=DisabledInfo(
            title=student_data.schools[0].schoolDisabledTitle if student_data.schools[0].schoolDisabled else None,
            message=student_data.schools[0].schoolDisabledMessage if student_data.schools[
                0].schoolDisabled else None,
        ),
        courses=sorted([Course(
            name=section.schoolCourseTitle,
            instructor=f"{instructors[section.teacherID].firstName} {instructors[section.teacherID].lastName}",
            instructor_email=instructors[section.teacherID].email,
            block=section.expression,
            room=section.roomName,
            assignments=[Assignment(
                title=assignment.name,
                date=int(assignment.dueDate.timestamp() * 1000),
                grade=get_assignment_grade(assignment.id),
                mark_for_display=get_mark_for_display(assignment),
                category=assignments_categories[assignment.categoryId].name,
                include_in_final_grade=assignment.includeinfinalgrades == 1,
                weight=assignment.weight,
                terms=list(set(term.abbreviation for term in reporting_terms.values() if
                               term.startDate <= assignment.dueDate <= term.endDate)),
                flags={
                    prop: scores[assignment.id][prop]
                    for prop in ['collected', 'exempt', 'incomplete', 'late', 'missing']
                } if assignment.id in scores else {},
                description=assignment.description,
                comment=scores[assignment.id].comment if assignment.id in scores else None,
            ) for assignment in student_data.assignments if assignment.sectionid == section.id],
            grades=[TermGrade(
                term=reporting_terms[grade.reportingTermId].title,
                grade=Grade(percentage=grade.percent, letter=grade.grade),
                comment=grade.commentValue.strip('\r\n ') if grade.commentValue else None,
                evaluation=citizen_grades[
                    grade.reportingTermId].description if grade.reportingTermId in citizen_grades else None,
                evaluation_code=citizen_grades[
                    grade.reportingTermId].codeName if grade.reportingTermId in citizen_grades else None,
            ) for grade in student_data.finalGrades if grade.sectionid == section.id],
            start_date=int(section.enrollments[0].startDate.timestamp() * 1000),
            end_date=int(section.enrollments[0].endDate.timestamp() * 1000),
            schedule=[CourseSchedule(
                start_time=int(schedule.start.timestamp() * 1000),
                end_time=int(schedule.stop.timestamp() * 1000)
            ) for schedule in section.startStopDates]
        ) for section in student_data.sections],
            key=lambda k: str(k.block) + str(k.name)
        ),
        extra_info=ExtraInfo(),
    )


if __name__ == '__main__':
    import pickle

    res = parse(pickle.load(open('student_data', 'rb')).studentDataVOs[0])
    json.dump(res.to_dict(), open('newapi_new.json', 'w'), indent=4, ensure_ascii=False)
