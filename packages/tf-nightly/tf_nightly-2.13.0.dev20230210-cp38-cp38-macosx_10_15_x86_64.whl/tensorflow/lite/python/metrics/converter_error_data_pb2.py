# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/lite/python/metrics/converter_error_data.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n9tensorflow/lite/python/metrics/converter_error_data.proto\x12\x0etflite.metrics\"\xab\x06\n\x12\x43onverterErrorData\x12\x11\n\tcomponent\x18\x01 \x01(\t\x12\x14\n\x0csubcomponent\x18\x02 \x01(\t\x12@\n\nerror_code\x18\x03 \x01(\x0e\x32,.tflite.metrics.ConverterErrorData.ErrorCode\x12\x15\n\rerror_message\x18\x04 \x01(\t\x12=\n\x08operator\x18\x05 \x01(\x0b\x32+.tflite.metrics.ConverterErrorData.Operator\x12=\n\x08location\x18\x06 \x01(\x0b\x32+.tflite.metrics.ConverterErrorData.Location\x1a\x18\n\x08Operator\x12\x0c\n\x04name\x18\x01 \x01(\t\x1a\x39\n\x07\x46ileLoc\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04line\x18\x02 \x01(\r\x12\x0e\n\x06\x63olumn\x18\x03 \x01(\r\x1aU\n\tSourceLoc\x12\x0c\n\x04name\x18\x01 \x01(\t\x12:\n\x06source\x18\x02 \x01(\x0b\x32*.tflite.metrics.ConverterErrorData.FileLoc\x1a\x85\x01\n\x08Location\x12=\n\x04type\x18\x01 \x01(\x0e\x32/.tflite.metrics.ConverterErrorData.LocationType\x12:\n\x04\x63\x61ll\x18\x02 \x03(\x0b\x32,.tflite.metrics.ConverterErrorData.SourceLoc\"\x94\x01\n\tErrorCode\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x18\n\x14\x45RROR_NEEDS_FLEX_OPS\x10\x01\x12\x1a\n\x16\x45RROR_NEEDS_CUSTOM_OPS\x10\x02\x12%\n!ERROR_UNSUPPORTED_CONTROL_FLOW_V1\x10\x03\x12\x1d\n\x18\x45RROR_GPU_NOT_COMPATIBLE\x10\xc8\x01\"J\n\x0cLocationType\x12\x0e\n\nUNKNOWNLOC\x10\x00\x12\x0b\n\x07NAMELOC\x10\x01\x12\x0f\n\x0b\x43\x41LLSITELOC\x10\x02\x12\x0c\n\x08\x46USEDLOC\x10\x03')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tensorflow.lite.python.metrics.converter_error_data_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CONVERTERERRORDATA._serialized_start=78
  _CONVERTERERRORDATA._serialized_end=889
  _CONVERTERERRORDATA_OPERATOR._serialized_start=356
  _CONVERTERERRORDATA_OPERATOR._serialized_end=380
  _CONVERTERERRORDATA_FILELOC._serialized_start=382
  _CONVERTERERRORDATA_FILELOC._serialized_end=439
  _CONVERTERERRORDATA_SOURCELOC._serialized_start=441
  _CONVERTERERRORDATA_SOURCELOC._serialized_end=526
  _CONVERTERERRORDATA_LOCATION._serialized_start=529
  _CONVERTERERRORDATA_LOCATION._serialized_end=662
  _CONVERTERERRORDATA_ERRORCODE._serialized_start=665
  _CONVERTERERRORDATA_ERRORCODE._serialized_end=813
  _CONVERTERERRORDATA_LOCATIONTYPE._serialized_start=815
  _CONVERTERERRORDATA_LOCATIONTYPE._serialized_end=889
# @@protoc_insertion_point(module_scope)
