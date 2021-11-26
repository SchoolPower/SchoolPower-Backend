# SchoolPower Backend Service

The backend of SchoolPower used by our Android, iOS, and Web apps.

SchoolPower is a modern, user-oriented third-party alternative to the official PowerSchool app with user-experience and
efficiency in mind. We made this when we were students, so we prioritize features that are actually useful. It is also
fully open-source so you can make modifications to fit your need if you want to.

It fetches your data through the SOAP API used for its mobile apps and parse it into easy-to-use JSON for our native
Android, iOS and Web apps. We do not retain your grade information.

Contact us if you are interested in using SchoolPower for your institution, or if you're interested in joining the
development.

## FaaS v3

This is the third iteration of the backend API, written in Python 3 + Sanic, and intended to be deplyed as a FaaS
service (e.g. Aliyun, AWS Lambda). The v2 version written in PHP
is [acrhived here](https://github.com/SchoolPower/Schoolpower-Backend/tree/v2).

It provides a set of backward-compatible API interface for v1 apps and another set of better ones for our v2 apps that
are under development. Interfaces are defined
with [protobufs](https://github.com/SchoolPower/schoolpower-backend/tree/main/protos).

License
-------

    Copyright 2021 SchoolPower Studio

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
