protoc object_detection/protos/*.proto --python_out=.
python object_detection/builders/model_builder_test.py
pause