# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: protos/powerschool_old.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import Dict, List

import betterproto


@dataclass
class AssignmentOld(betterproto.Message):
    category: str = betterproto.string_field(1)
    description: str = betterproto.string_field(2)
    name: str = betterproto.string_field(3)
    percent: str = betterproto.string_field(4)
    score: str = betterproto.string_field(5)
    letter_grade: str = betterproto.string_field(6)
    status: Dict[str, bool] = betterproto.map_field(
        7, betterproto.TYPE_STRING, betterproto.TYPE_BOOL
    )
    points_possible: str = betterproto.string_field(8)
    date: str = betterproto.string_field(9)
    weight: str = betterproto.string_field(10)
    include_in_final_grade: str = betterproto.string_field(11)
    terms: List[str] = betterproto.string_field(12)


@dataclass
class SectionOld(betterproto.Message):
    assignments: List["AssignmentOld"] = betterproto.message_field(1)
    expression: str = betterproto.string_field(2)
    start_date: str = betterproto.string_field(3)
    end_date: str = betterproto.string_field(4)
    final_grades: Dict[str, "SectionOldFinalGrade"] = betterproto.map_field(
        5, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    name: str = betterproto.string_field(6)
    room_name: str = betterproto.string_field(7)
    teacher: "SectionOldTeacher" = betterproto.message_field(8)


@dataclass
class SectionOldFinalGrade(betterproto.Message):
    percent: str = betterproto.string_field(1)
    letter: str = betterproto.string_field(2)
    comment: str = betterproto.string_field(3)
    eval: str = betterproto.string_field(4)
    start_date: int = betterproto.int32_field(5)
    end_date: int = betterproto.int32_field(6)


@dataclass
class SectionOldTeacher(betterproto.Message):
    first_name: str = betterproto.string_field(1)
    last_name: str = betterproto.string_field(2)
    email: str = betterproto.string_field(3)
    school_phone: str = betterproto.string_field(4)


@dataclass
class InformationOld(betterproto.Message):
    current_g_p_a: str = betterproto.string_field(1)
    current_term: str = betterproto.string_field(2)
    dob: str = betterproto.string_field(3)
    id: str = betterproto.string_field(4)
    first_name: str = betterproto.string_field(5)
    middle_name: str = betterproto.string_field(6)
    last_name: str = betterproto.string_field(7)
    gender: str = betterproto.string_field(8)
    photo_date: str = betterproto.string_field(9)


@dataclass
class AttendanceOld(betterproto.Message):
    code: str = betterproto.string_field(1)
    description: str = betterproto.string_field(2)
    date: str = betterproto.string_field(3)
    period: str = betterproto.string_field(4)
    name: str = betterproto.string_field(5)


@dataclass
class AdditionalOld(betterproto.Message):
    avatar: str = betterproto.string_field(1)


@dataclass
class StudentDataOld(betterproto.Message):
    information: "InformationOld" = betterproto.message_field(1)
    sections: List["SectionOld"] = betterproto.message_field(2)
    attendances: List["AttendanceOld"] = betterproto.message_field(3)
    additional: "AdditionalOld" = betterproto.message_field(4)
