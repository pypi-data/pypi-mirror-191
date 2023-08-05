# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: deepomatic/oef/protos/models/image/detection/ssd_anchor_generator.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='deepomatic/oef/protos/models/image/detection/ssd_anchor_generator.proto',
  package='deepomatic.oef.models.image.detection',
  syntax='proto2',
  serialized_pb=_b('\nGdeepomatic/oef/protos/models/image/detection/ssd_anchor_generator.proto\x12%deepomatic.oef.models.image.detection\"\xf2\x02\n\x12SsdAnchorGenerator\x12\x15\n\nnum_layers\x18\x01 \x01(\x05:\x01\x36\x12\x16\n\tmin_scale\x18\x02 \x01(\x02:\x03\x30.2\x12\x17\n\tmax_scale\x18\x03 \x01(\x02:\x04\x30.95\x12\x0e\n\x06scales\x18\x0c \x03(\x02\x12\x15\n\raspect_ratios\x18\x04 \x03(\x02\x12*\n\x1finterpolated_scale_aspect_ratio\x18\r \x01(\x02:\x01\x31\x12*\n\x1creduce_boxes_in_lowest_layer\x18\x05 \x01(\x08:\x04true\x12\x1d\n\x12\x62\x61se_anchor_height\x18\x06 \x01(\x02:\x01\x31\x12\x1c\n\x11\x62\x61se_anchor_width\x18\x07 \x01(\x02:\x01\x31\x12\x15\n\rheight_stride\x18\x08 \x03(\x05\x12\x14\n\x0cwidth_stride\x18\t \x03(\x05\x12\x15\n\rheight_offset\x18\n \x03(\x05\x12\x14\n\x0cwidth_offset\x18\x0b \x03(\x05')
)




_SSDANCHORGENERATOR = _descriptor.Descriptor(
  name='SsdAnchorGenerator',
  full_name='deepomatic.oef.models.image.detection.SsdAnchorGenerator',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='num_layers', full_name='deepomatic.oef.models.image.detection.SsdAnchorGenerator.num_layers', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=6,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='min_scale', full_name='deepomatic.oef.models.image.detection.SsdAnchorGenerator.min_scale', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.2),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_scale', full_name='deepomatic.oef.models.image.detection.SsdAnchorGenerator.max_scale', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.95),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='scales', full_name='deepomatic.oef.models.image.detection.SsdAnchorGenerator.scales', index=3,
      number=12, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='aspect_ratios', full_name='deepomatic.oef.models.image.detection.SsdAnchorGenerator.aspect_ratios', index=4,
      number=4, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='interpolated_scale_aspect_ratio', full_name='deepomatic.oef.models.image.detection.SsdAnchorGenerator.interpolated_scale_aspect_ratio', index=5,
      number=13, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='reduce_boxes_in_lowest_layer', full_name='deepomatic.oef.models.image.detection.SsdAnchorGenerator.reduce_boxes_in_lowest_layer', index=6,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='base_anchor_height', full_name='deepomatic.oef.models.image.detection.SsdAnchorGenerator.base_anchor_height', index=7,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='base_anchor_width', full_name='deepomatic.oef.models.image.detection.SsdAnchorGenerator.base_anchor_width', index=8,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='height_stride', full_name='deepomatic.oef.models.image.detection.SsdAnchorGenerator.height_stride', index=9,
      number=8, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='width_stride', full_name='deepomatic.oef.models.image.detection.SsdAnchorGenerator.width_stride', index=10,
      number=9, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='height_offset', full_name='deepomatic.oef.models.image.detection.SsdAnchorGenerator.height_offset', index=11,
      number=10, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='width_offset', full_name='deepomatic.oef.models.image.detection.SsdAnchorGenerator.width_offset', index=12,
      number=11, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=115,
  serialized_end=485,
)

DESCRIPTOR.message_types_by_name['SsdAnchorGenerator'] = _SSDANCHORGENERATOR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SsdAnchorGenerator = _reflection.GeneratedProtocolMessageType('SsdAnchorGenerator', (_message.Message,), dict(
  DESCRIPTOR = _SSDANCHORGENERATOR,
  __module__ = 'deepomatic.oef.protos.models.image.detection.ssd_anchor_generator_pb2'
  # @@protoc_insertion_point(class_scope:deepomatic.oef.models.image.detection.SsdAnchorGenerator)
  ))
_sym_db.RegisterMessage(SsdAnchorGenerator)


# @@protoc_insertion_point(module_scope)
