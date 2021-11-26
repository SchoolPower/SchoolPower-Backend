#!/bin/bash
protoc -I . --python_betterproto_out=powerschool protos/powerschool.proto
protoc -I . --python_betterproto_out=powerschool protos/powerschool_old.proto
