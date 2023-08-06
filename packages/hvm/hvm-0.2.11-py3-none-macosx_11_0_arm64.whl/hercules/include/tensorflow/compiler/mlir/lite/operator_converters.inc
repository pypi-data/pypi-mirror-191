/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* MLIR TFLite FlatBuffer Builders                                            *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

flatbuffers::Offset<tflite::AddOptions> CreateAddOptions(mlir::TFL::AddOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  tflite::AddOptionsBuilder b(*fbb);
  b.add_fused_activation_function(std::move(fused_activation_function));
  return b.Finish();
}
flatbuffers::Offset<tflite::ArgMaxOptions> CreateArgMaxOptions(mlir::TFL::ArgMaxOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto output_type = ConvertDerivedTFLiteTypeAttrForOptionWriter(op.output_type(), fbb);
  tflite::ArgMaxOptionsBuilder b(*fbb);
  b.add_output_type(std::move(output_type));
  return b.Finish();
}
flatbuffers::Offset<tflite::ArgMinOptions> CreateArgMinOptions(mlir::TFL::ArgMinOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto output_type = ConvertDerivedTFLiteTypeAttrForOptionWriter(op.output_type(), fbb);
  tflite::ArgMinOptionsBuilder b(*fbb);
  b.add_output_type(std::move(output_type));
  return b.Finish();
}
flatbuffers::Offset<tflite::Pool2DOptions> CreatePool2DOptions(mlir::TFL::AveragePool2DOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto filter_height = ConvertI32AttrForOptionWriter(op.filter_height(), fbb);
  auto filter_width = ConvertI32AttrForOptionWriter(op.filter_width(), fbb);
  auto padding = ConvertTFL_PaddingAttrForOptionWriter(op.padding(), fbb);
  auto stride_h = ConvertI32AttrForOptionWriter(op.stride_h(), fbb);
  auto stride_w = ConvertI32AttrForOptionWriter(op.stride_w(), fbb);
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  tflite::Pool2DOptionsBuilder b(*fbb);
  b.add_filter_height(std::move(filter_height));
  b.add_filter_width(std::move(filter_width));
  b.add_padding(std::move(padding));
  b.add_stride_h(std::move(stride_h));
  b.add_stride_w(std::move(stride_w));
  b.add_fused_activation_function(std::move(fused_activation_function));
  return b.Finish();
}
flatbuffers::Offset<tflite::LSTMOptions> CreateBasicLSTMOptions(mlir::TFL::BasicLSTMOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  auto cell_clip = ConvertF32AttrForOptionWriter(op.cell_clip(), fbb);
  auto proj_clip = ConvertF32AttrForOptionWriter(op.proj_clip(), fbb);
  auto kernel_type = ConvertTFL_LSTMKernelTypeAttrForOptionWriter(op.kernel_type(), fbb);
  tflite::LSTMOptionsBuilder b(*fbb);
  b.add_fused_activation_function(std::move(fused_activation_function));
  b.add_cell_clip(std::move(cell_clip));
  b.add_proj_clip(std::move(proj_clip));
  b.add_kernel_type(std::move(kernel_type));
  return b.Finish();
}
flatbuffers::Offset<tflite::BatchMatMulOptions> CreateBatchMatMulOptions(mlir::TFL::BatchMatMulOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto adj_x = ConvertBoolAttrForOptionWriter(op.adj_x(), fbb);
  auto adj_y = ConvertBoolAttrForOptionWriter(op.adj_y(), fbb);
  auto asymmetric_quantize_inputs = ConvertBoolAttrForOptionWriter(op.asymmetric_quantize_inputs(), fbb);
  tflite::BatchMatMulOptionsBuilder b(*fbb);
  b.add_adj_x(std::move(adj_x));
  b.add_adj_y(std::move(adj_y));
  b.add_asymmetric_quantize_inputs(std::move(asymmetric_quantize_inputs));
  return b.Finish();
}
flatbuffers::Offset<tflite::BidirectionalSequenceLSTMOptions> CreateBidirectionalSequenceLSTMOptions(mlir::TFL::BidirectionalSequenceLSTMOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  auto cell_clip = ConvertF32AttrForOptionWriter(op.cell_clip(), fbb);
  auto proj_clip = ConvertF32AttrForOptionWriter(op.proj_clip(), fbb);
  auto merge_outputs = ConvertBoolAttrForOptionWriter(op.merge_outputs(), fbb);
  auto time_major = ConvertBoolAttrForOptionWriter(op.time_major(), fbb);
  auto asymmetric_quantize_inputs = ConvertBoolAttrForOptionWriter(op.asymmetric_quantize_inputs(), fbb);
  tflite::BidirectionalSequenceLSTMOptionsBuilder b(*fbb);
  b.add_fused_activation_function(std::move(fused_activation_function));
  b.add_cell_clip(std::move(cell_clip));
  b.add_proj_clip(std::move(proj_clip));
  b.add_merge_outputs(std::move(merge_outputs));
  b.add_time_major(std::move(time_major));
  b.add_asymmetric_quantize_inputs(std::move(asymmetric_quantize_inputs));
  return b.Finish();
}
flatbuffers::Offset<tflite::BucketizeOptions> CreateBucketizeOptions(mlir::TFL::BucketizeOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto boundaries = ConvertF32ArrayAttrForOptionWriter(op.boundaries(), fbb);
  tflite::BucketizeOptionsBuilder b(*fbb);
  b.add_boundaries(std::move(boundaries));
  return b.Finish();
}
flatbuffers::Offset<tflite::ConcatenationOptions> CreateConcatenationOptions(mlir::TFL::ConcatenationOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto axis = ConvertI32AttrForOptionWriter(op.axis(), fbb);
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  tflite::ConcatenationOptionsBuilder b(*fbb);
  b.add_axis(std::move(axis));
  b.add_fused_activation_function(std::move(fused_activation_function));
  return b.Finish();
}
flatbuffers::Offset<tflite::Conv2DOptions> CreateConv2DOptions(mlir::TFL::Conv2DOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto dilation_h_factor = ConvertI32AttrForOptionWriter(op.dilation_h_factor(), fbb);
  auto dilation_w_factor = ConvertI32AttrForOptionWriter(op.dilation_w_factor(), fbb);
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  auto padding = ConvertTFL_PaddingAttrForOptionWriter(op.padding(), fbb);
  auto stride_h = ConvertI32AttrForOptionWriter(op.stride_h(), fbb);
  auto stride_w = ConvertI32AttrForOptionWriter(op.stride_w(), fbb);
  tflite::Conv2DOptionsBuilder b(*fbb);
  b.add_dilation_h_factor(std::move(dilation_h_factor));
  b.add_dilation_w_factor(std::move(dilation_w_factor));
  b.add_fused_activation_function(std::move(fused_activation_function));
  b.add_padding(std::move(padding));
  b.add_stride_h(std::move(stride_h));
  b.add_stride_w(std::move(stride_w));
  return b.Finish();
}
flatbuffers::Offset<tflite::Conv3DOptions> CreateConv3DOptions(mlir::TFL::Conv3DOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto dilation_d_factor = ConvertI32AttrForOptionWriter(op.dilation_d_factor(), fbb);
  auto dilation_h_factor = ConvertI32AttrForOptionWriter(op.dilation_h_factor(), fbb);
  auto dilation_w_factor = ConvertI32AttrForOptionWriter(op.dilation_w_factor(), fbb);
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  auto padding = ConvertTFL_PaddingAttrForOptionWriter(op.padding(), fbb);
  auto stride_d = ConvertI32AttrForOptionWriter(op.stride_d(), fbb);
  auto stride_h = ConvertI32AttrForOptionWriter(op.stride_h(), fbb);
  auto stride_w = ConvertI32AttrForOptionWriter(op.stride_w(), fbb);
  tflite::Conv3DOptionsBuilder b(*fbb);
  b.add_dilation_d_factor(std::move(dilation_d_factor));
  b.add_dilation_h_factor(std::move(dilation_h_factor));
  b.add_dilation_w_factor(std::move(dilation_w_factor));
  b.add_fused_activation_function(std::move(fused_activation_function));
  b.add_padding(std::move(padding));
  b.add_stride_d(std::move(stride_d));
  b.add_stride_h(std::move(stride_h));
  b.add_stride_w(std::move(stride_w));
  return b.Finish();
}
flatbuffers::Offset<tflite::Conv3DOptions> CreateConv3DOptions(mlir::TFL::Conv3DTransposeOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto dilation_d_factor = ConvertI32AttrForOptionWriter(op.dilation_d_factor(), fbb);
  auto dilation_h_factor = ConvertI32AttrForOptionWriter(op.dilation_h_factor(), fbb);
  auto dilation_w_factor = ConvertI32AttrForOptionWriter(op.dilation_w_factor(), fbb);
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  auto padding = ConvertTFL_PaddingAttrForOptionWriter(op.padding(), fbb);
  auto stride_d = ConvertI32AttrForOptionWriter(op.stride_d(), fbb);
  auto stride_h = ConvertI32AttrForOptionWriter(op.stride_h(), fbb);
  auto stride_w = ConvertI32AttrForOptionWriter(op.stride_w(), fbb);
  tflite::Conv3DOptionsBuilder b(*fbb);
  b.add_dilation_d_factor(std::move(dilation_d_factor));
  b.add_dilation_h_factor(std::move(dilation_h_factor));
  b.add_dilation_w_factor(std::move(dilation_w_factor));
  b.add_fused_activation_function(std::move(fused_activation_function));
  b.add_padding(std::move(padding));
  b.add_stride_d(std::move(stride_d));
  b.add_stride_h(std::move(stride_h));
  b.add_stride_w(std::move(stride_w));
  return b.Finish();
}
flatbuffers::Offset<tflite::CumsumOptions> CreateCumsumOptions(mlir::TFL::CumsumOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto exclusive = ConvertBoolAttrForOptionWriter(op.exclusive(), fbb);
  auto reverse = ConvertBoolAttrForOptionWriter(op.reverse(), fbb);
  tflite::CumsumOptionsBuilder b(*fbb);
  b.add_exclusive(std::move(exclusive));
  b.add_reverse(std::move(reverse));
  return b.Finish();
}
flatbuffers::Offset<tflite::DepthToSpaceOptions> CreateDepthToSpaceOptions(mlir::TFL::DepthToSpaceOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto block_size = ConvertI32AttrForOptionWriter(op.block_size(), fbb);
  tflite::DepthToSpaceOptionsBuilder b(*fbb);
  b.add_block_size(std::move(block_size));
  return b.Finish();
}
flatbuffers::Offset<tflite::DepthwiseConv2DOptions> CreateDepthwiseConv2DOptions(mlir::TFL::DepthwiseConv2DOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto dilation_h_factor = ConvertI32AttrForOptionWriter(op.dilation_h_factor(), fbb);
  auto dilation_w_factor = ConvertI32AttrForOptionWriter(op.dilation_w_factor(), fbb);
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  auto padding = ConvertTFL_PaddingAttrForOptionWriter(op.padding(), fbb);
  auto stride_h = ConvertI32AttrForOptionWriter(op.stride_h(), fbb);
  auto stride_w = ConvertI32AttrForOptionWriter(op.stride_w(), fbb);
  auto depth_multiplier = ConvertI32AttrForOptionWriter(op.depth_multiplier(), fbb);
  tflite::DepthwiseConv2DOptionsBuilder b(*fbb);
  b.add_dilation_h_factor(std::move(dilation_h_factor));
  b.add_dilation_w_factor(std::move(dilation_w_factor));
  b.add_fused_activation_function(std::move(fused_activation_function));
  b.add_padding(std::move(padding));
  b.add_stride_h(std::move(stride_h));
  b.add_stride_w(std::move(stride_w));
  b.add_depth_multiplier(std::move(depth_multiplier));
  return b.Finish();
}
flatbuffers::Offset<tflite::DivOptions> CreateDivOptions(mlir::TFL::DivOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  tflite::DivOptionsBuilder b(*fbb);
  b.add_fused_activation_function(std::move(fused_activation_function));
  return b.Finish();
}
flatbuffers::Offset<tflite::ExpOptions> CreateExpOptions(mlir::TFL::ExpOp op, flatbuffers::FlatBufferBuilder *fbb) {
  tflite::ExpOptionsBuilder b(*fbb);
  return b.Finish();
}
flatbuffers::Offset<tflite::ExpandDimsOptions> CreateExpandDimsOptions(mlir::TFL::ExpandDimsOp op, flatbuffers::FlatBufferBuilder *fbb) {
  tflite::ExpandDimsOptionsBuilder b(*fbb);
  return b.Finish();
}
flatbuffers::Offset<tflite::FakeQuantOptions> CreateFakeQuantOptions(mlir::TFL::FakeQuantOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto min = ConvertF32AttrForOptionWriter(op.min(), fbb);
  auto max = ConvertF32AttrForOptionWriter(op.max(), fbb);
  auto num_bits = ConvertI32AttrForOptionWriter(op.num_bits(), fbb);
  auto narrow_range = ConvertBoolAttrForOptionWriter(op.narrow_range(), fbb);
  tflite::FakeQuantOptionsBuilder b(*fbb);
  b.add_min(std::move(min));
  b.add_max(std::move(max));
  b.add_num_bits(std::move(num_bits));
  b.add_narrow_range(std::move(narrow_range));
  return b.Finish();
}
flatbuffers::Offset<tflite::FullyConnectedOptions> CreateFullyConnectedOptions(mlir::TFL::FullyConnectedOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  auto weights_format = ConvertTFL_FullyConnectedOptionsWeightFormatAttrForOptionWriter(op.weights_format(), fbb);
  auto keep_num_dims = ConvertBoolAttrForOptionWriter(op.keep_num_dims(), fbb);
  auto asymmetric_quantize_inputs = ConvertBoolAttrForOptionWriter(op.asymmetric_quantize_inputs(), fbb);
  tflite::FullyConnectedOptionsBuilder b(*fbb);
  b.add_fused_activation_function(std::move(fused_activation_function));
  b.add_weights_format(std::move(weights_format));
  b.add_keep_num_dims(std::move(keep_num_dims));
  b.add_asymmetric_quantize_inputs(std::move(asymmetric_quantize_inputs));
  return b.Finish();
}
flatbuffers::Offset<tflite::GatherOptions> CreateGatherOptions(mlir::TFL::GatherOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto axis = ConvertI32AttrForOptionWriter(op.axis(), fbb);
  auto batch_dims = ConvertI32AttrForOptionWriter(op.batch_dims(), fbb);
  tflite::GatherOptionsBuilder b(*fbb);
  b.add_axis(std::move(axis));
  b.add_batch_dims(std::move(batch_dims));
  return b.Finish();
}
flatbuffers::Offset<tflite::HashtableOptions> CreateHashtableOptions(mlir::TFL::HashtableOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto table_id = ConvertI32AttrForOptionWriter(op.table_id(), fbb);
  auto key_dtype = ConvertTypeAttrForOptionWriter(op.key_dtype(), fbb);
  auto value_dtype = ConvertTypeAttrForOptionWriter(op.value_dtype(), fbb);
  tflite::HashtableOptionsBuilder b(*fbb);
  b.add_table_id(std::move(table_id));
  b.add_key_dtype(std::move(key_dtype));
  b.add_value_dtype(std::move(value_dtype));
  return b.Finish();
}
flatbuffers::Offset<tflite::L2NormOptions> CreateL2NormOptions(mlir::TFL::L2NormalizationOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  tflite::L2NormOptionsBuilder b(*fbb);
  b.add_fused_activation_function(std::move(fused_activation_function));
  return b.Finish();
}
flatbuffers::Offset<tflite::LSTMOptions> CreateLSTMOptions(mlir::TFL::LSTMOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  auto cell_clip = ConvertF32AttrForOptionWriter(op.cell_clip(), fbb);
  auto proj_clip = ConvertF32AttrForOptionWriter(op.proj_clip(), fbb);
  auto kernel_type = ConvertTFL_LSTMKernelTypeAttrForOptionWriter(op.kernel_type(), fbb);
  auto asymmetric_quantize_inputs = ConvertBoolAttrForOptionWriter(op.asymmetric_quantize_inputs(), fbb);
  tflite::LSTMOptionsBuilder b(*fbb);
  b.add_fused_activation_function(std::move(fused_activation_function));
  b.add_cell_clip(std::move(cell_clip));
  b.add_proj_clip(std::move(proj_clip));
  b.add_kernel_type(std::move(kernel_type));
  b.add_asymmetric_quantize_inputs(std::move(asymmetric_quantize_inputs));
  return b.Finish();
}
flatbuffers::Offset<tflite::LeakyReluOptions> CreateLeakyReluOptions(mlir::TFL::LeakyReluOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto alpha = ConvertF32AttrForOptionWriter(op.alpha(), fbb);
  tflite::LeakyReluOptionsBuilder b(*fbb);
  b.add_alpha(std::move(alpha));
  return b.Finish();
}
flatbuffers::Offset<tflite::LocalResponseNormalizationOptions> CreateLocalResponseNormalizationOptions(mlir::TFL::LocalResponseNormalizationOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto radius = ConvertI32AttrForOptionWriter(op.radius(), fbb);
  auto bias = ConvertF32AttrForOptionWriter(op.bias(), fbb);
  auto alpha = ConvertF32AttrForOptionWriter(op.alpha(), fbb);
  auto beta = ConvertF32AttrForOptionWriter(op.beta(), fbb);
  tflite::LocalResponseNormalizationOptionsBuilder b(*fbb);
  b.add_radius(std::move(radius));
  b.add_bias(std::move(bias));
  b.add_alpha(std::move(alpha));
  b.add_beta(std::move(beta));
  return b.Finish();
}
flatbuffers::Offset<tflite::LogSoftmaxOptions> CreateLogSoftmaxOptions(mlir::TFL::LogSoftmaxOp op, flatbuffers::FlatBufferBuilder *fbb) {
  tflite::LogSoftmaxOptionsBuilder b(*fbb);
  return b.Finish();
}
flatbuffers::Offset<tflite::Pool2DOptions> CreatePool2DOptions(mlir::TFL::MaxPool2DOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto padding = ConvertTFL_PaddingAttrForOptionWriter(op.padding(), fbb);
  auto stride_w = ConvertI32AttrForOptionWriter(op.stride_w(), fbb);
  auto stride_h = ConvertI32AttrForOptionWriter(op.stride_h(), fbb);
  auto filter_width = ConvertI32AttrForOptionWriter(op.filter_width(), fbb);
  auto filter_height = ConvertI32AttrForOptionWriter(op.filter_height(), fbb);
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  tflite::Pool2DOptionsBuilder b(*fbb);
  b.add_padding(std::move(padding));
  b.add_stride_w(std::move(stride_w));
  b.add_stride_h(std::move(stride_h));
  b.add_filter_width(std::move(filter_width));
  b.add_filter_height(std::move(filter_height));
  b.add_fused_activation_function(std::move(fused_activation_function));
  return b.Finish();
}
flatbuffers::Offset<tflite::ReducerOptions> CreateReducerOptions(mlir::TFL::MeanOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto keep_dims = ConvertBoolAttrForOptionWriter(op.keep_dims(), fbb);
  tflite::ReducerOptionsBuilder b(*fbb);
  b.add_keep_dims(std::move(keep_dims));
  return b.Finish();
}
flatbuffers::Offset<tflite::MirrorPadOptions> CreateMirrorPadOptions(mlir::TFL::MirrorPadOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto mode = ConvertTFL_MirrorPaddingAttrForOptionWriter(op.mode(), fbb);
  tflite::MirrorPadOptionsBuilder b(*fbb);
  b.add_mode(std::move(mode));
  return b.Finish();
}
flatbuffers::Offset<tflite::MulOptions> CreateMulOptions(mlir::TFL::MulOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  tflite::MulOptionsBuilder b(*fbb);
  b.add_fused_activation_function(std::move(fused_activation_function));
  return b.Finish();
}
flatbuffers::Offset<tflite::RandomOptions> CreateRandomOptions(mlir::TFL::MultinomialOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto seed = ConvertI64AttrForOptionWriter(op.seed(), fbb);
  auto seed2 = ConvertI64AttrForOptionWriter(op.seed2(), fbb);
  tflite::RandomOptionsBuilder b(*fbb);
  b.add_seed(std::move(seed));
  b.add_seed2(std::move(seed2));
  return b.Finish();
}
flatbuffers::Offset<tflite::NegOptions> CreateNegOptions(mlir::TFL::NegOp op, flatbuffers::FlatBufferBuilder *fbb) {
  tflite::NegOptionsBuilder b(*fbb);
  return b.Finish();
}
flatbuffers::Offset<tflite::OneHotOptions> CreateOneHotOptions(mlir::TFL::OneHotOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto axis = ConvertI32AttrForOptionWriter(op.axis(), fbb);
  tflite::OneHotOptionsBuilder b(*fbb);
  b.add_axis(std::move(axis));
  return b.Finish();
}
flatbuffers::Offset<tflite::PackOptions> CreatePackOptions(mlir::TFL::PackOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto values_count = ConvertI32AttrForOptionWriter(op.values_count(), fbb);
  auto axis = ConvertI32AttrForOptionWriter(op.axis(), fbb);
  tflite::PackOptionsBuilder b(*fbb);
  b.add_values_count(std::move(values_count));
  b.add_axis(std::move(axis));
  return b.Finish();
}
flatbuffers::Offset<tflite::PadOptions> CreatePadOptions(mlir::TFL::PadOp op, flatbuffers::FlatBufferBuilder *fbb) {
  tflite::PadOptionsBuilder b(*fbb);
  return b.Finish();
}
flatbuffers::Offset<tflite::PadV2Options> CreatePadV2Options(mlir::TFL::PadV2Op op, flatbuffers::FlatBufferBuilder *fbb) {
  tflite::PadV2OptionsBuilder b(*fbb);
  return b.Finish();
}
flatbuffers::Offset<tflite::RandomOptions> CreateRandomOptions(mlir::TFL::RandomStandardNormalOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto seed = ConvertI64AttrForOptionWriter(op.seed(), fbb);
  auto seed2 = ConvertI64AttrForOptionWriter(op.seed2(), fbb);
  tflite::RandomOptionsBuilder b(*fbb);
  b.add_seed(std::move(seed));
  b.add_seed2(std::move(seed2));
  return b.Finish();
}
flatbuffers::Offset<tflite::RandomOptions> CreateRandomOptions(mlir::TFL::RandomUniformOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto seed = ConvertI64AttrForOptionWriter(op.seed(), fbb);
  auto seed2 = ConvertI64AttrForOptionWriter(op.seed2(), fbb);
  tflite::RandomOptionsBuilder b(*fbb);
  b.add_seed(std::move(seed));
  b.add_seed2(std::move(seed2));
  return b.Finish();
}
flatbuffers::Offset<tflite::ReducerOptions> CreateReducerOptions(mlir::TFL::ReduceAllOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto keep_dims = ConvertBoolAttrForOptionWriter(op.keep_dims(), fbb);
  tflite::ReducerOptionsBuilder b(*fbb);
  b.add_keep_dims(std::move(keep_dims));
  return b.Finish();
}
flatbuffers::Offset<tflite::ReducerOptions> CreateReducerOptions(mlir::TFL::ReduceAnyOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto keep_dims = ConvertBoolAttrForOptionWriter(op.keep_dims(), fbb);
  tflite::ReducerOptionsBuilder b(*fbb);
  b.add_keep_dims(std::move(keep_dims));
  return b.Finish();
}
flatbuffers::Offset<tflite::ReducerOptions> CreateReducerOptions(mlir::TFL::ReduceMaxOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto keep_dims = ConvertBoolAttrForOptionWriter(op.keep_dims(), fbb);
  tflite::ReducerOptionsBuilder b(*fbb);
  b.add_keep_dims(std::move(keep_dims));
  return b.Finish();
}
flatbuffers::Offset<tflite::ReducerOptions> CreateReducerOptions(mlir::TFL::ReduceMinOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto keep_dims = ConvertBoolAttrForOptionWriter(op.keep_dims(), fbb);
  tflite::ReducerOptionsBuilder b(*fbb);
  b.add_keep_dims(std::move(keep_dims));
  return b.Finish();
}
flatbuffers::Offset<tflite::ReducerOptions> CreateReducerOptions(mlir::TFL::ReduceProdOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto keep_dims = ConvertBoolAttrForOptionWriter(op.keep_dims(), fbb);
  tflite::ReducerOptionsBuilder b(*fbb);
  b.add_keep_dims(std::move(keep_dims));
  return b.Finish();
}
flatbuffers::Offset<tflite::ResizeBilinearOptions> CreateResizeBilinearOptions(mlir::TFL::ResizeBilinearOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto align_corners = ConvertBoolAttrForOptionWriter(op.align_corners(), fbb);
  auto half_pixel_centers = ConvertBoolAttrForOptionWriter(op.half_pixel_centers(), fbb);
  tflite::ResizeBilinearOptionsBuilder b(*fbb);
  b.add_align_corners(std::move(align_corners));
  b.add_half_pixel_centers(std::move(half_pixel_centers));
  return b.Finish();
}
flatbuffers::Offset<tflite::ResizeNearestNeighborOptions> CreateResizeNearestNeighborOptions(mlir::TFL::ResizeNearestNeighborOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto align_corners = ConvertBoolAttrForOptionWriter(op.align_corners(), fbb);
  auto half_pixel_centers = ConvertBoolAttrForOptionWriter(op.half_pixel_centers(), fbb);
  tflite::ResizeNearestNeighborOptionsBuilder b(*fbb);
  b.add_align_corners(std::move(align_corners));
  b.add_half_pixel_centers(std::move(half_pixel_centers));
  return b.Finish();
}
flatbuffers::Offset<tflite::ReverseSequenceOptions> CreateReverseSequenceOptions(mlir::TFL::ReverseSequenceOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto seq_dim = ConvertI32AttrForOptionWriter(op.seq_dim(), fbb);
  auto batch_dim = ConvertI32AttrForOptionWriter(op.batch_dim(), fbb);
  tflite::ReverseSequenceOptionsBuilder b(*fbb);
  b.add_seq_dim(std::move(seq_dim));
  b.add_batch_dim(std::move(batch_dim));
  return b.Finish();
}
flatbuffers::Offset<tflite::SVDFOptions> CreateSVDFOptions(mlir::TFL::SVDFOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto rank = ConvertI32AttrForOptionWriter(op.rank(), fbb);
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  auto asymmetric_quantize_inputs = ConvertBoolAttrForOptionWriter(op.asymmetric_quantize_inputs(), fbb);
  tflite::SVDFOptionsBuilder b(*fbb);
  b.add_rank(std::move(rank));
  b.add_fused_activation_function(std::move(fused_activation_function));
  b.add_asymmetric_quantize_inputs(std::move(asymmetric_quantize_inputs));
  return b.Finish();
}
flatbuffers::Offset<tflite::ScatterNdOptions> CreateScatterNdOptions(mlir::TFL::ScatterNdOp op, flatbuffers::FlatBufferBuilder *fbb) {
  tflite::ScatterNdOptionsBuilder b(*fbb);
  return b.Finish();
}
flatbuffers::Offset<tflite::SelectOptions> CreateSelectOptions(mlir::TFL::SelectOp op, flatbuffers::FlatBufferBuilder *fbb) {
  tflite::SelectOptionsBuilder b(*fbb);
  return b.Finish();
}
flatbuffers::Offset<tflite::SelectV2Options> CreateSelectV2Options(mlir::TFL::SelectV2Op op, flatbuffers::FlatBufferBuilder *fbb) {
  tflite::SelectV2OptionsBuilder b(*fbb);
  return b.Finish();
}
flatbuffers::Offset<tflite::ShapeOptions> CreateShapeOptions(mlir::TFL::ShapeOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto out_type = ConvertDerivedTypeAttrForOptionWriter(op.out_type(), fbb);
  tflite::ShapeOptionsBuilder b(*fbb);
  b.add_out_type(std::move(out_type));
  return b.Finish();
}
flatbuffers::Offset<tflite::SoftmaxOptions> CreateSoftmaxOptions(mlir::TFL::SoftmaxOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto beta = ConvertF32AttrForOptionWriter(op.beta(), fbb);
  tflite::SoftmaxOptionsBuilder b(*fbb);
  b.add_beta(std::move(beta));
  return b.Finish();
}
flatbuffers::Offset<tflite::SpaceToDepthOptions> CreateSpaceToDepthOptions(mlir::TFL::SpaceToDepthOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto block_size = ConvertI32AttrForOptionWriter(op.block_size(), fbb);
  tflite::SpaceToDepthOptionsBuilder b(*fbb);
  b.add_block_size(std::move(block_size));
  return b.Finish();
}
flatbuffers::Offset<tflite::SplitOptions> CreateSplitOptions(mlir::TFL::SplitOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto num_splits = ConvertI32AttrForOptionWriter(op.num_splits(), fbb);
  tflite::SplitOptionsBuilder b(*fbb);
  b.add_num_splits(std::move(num_splits));
  return b.Finish();
}
flatbuffers::Offset<tflite::SplitVOptions> CreateSplitVOptions(mlir::TFL::SplitVOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto num_splits = ConvertI32AttrForOptionWriter(op.num_splits(), fbb);
  tflite::SplitVOptionsBuilder b(*fbb);
  b.add_num_splits(std::move(num_splits));
  return b.Finish();
}
flatbuffers::Offset<tflite::SquareOptions> CreateSquareOptions(mlir::TFL::SquareOp op, flatbuffers::FlatBufferBuilder *fbb) {
  tflite::SquareOptionsBuilder b(*fbb);
  return b.Finish();
}
flatbuffers::Offset<tflite::SqueezeOptions> CreateSqueezeOptions(mlir::TFL::SqueezeOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto squeeze_dims = ConvertI64ArrayAttrForOptionWriter(op.squeeze_dims(), fbb);
  tflite::SqueezeOptionsBuilder b(*fbb);
  b.add_squeeze_dims(std::move(squeeze_dims));
  return b.Finish();
}
flatbuffers::Offset<tflite::StridedSliceOptions> CreateStridedSliceOptions(mlir::TFL::StridedSliceOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto begin_mask = ConvertI32AttrForOptionWriter(op.begin_mask(), fbb);
  auto end_mask = ConvertI32AttrForOptionWriter(op.end_mask(), fbb);
  auto ellipsis_mask = ConvertI32AttrForOptionWriter(op.ellipsis_mask(), fbb);
  auto new_axis_mask = ConvertI32AttrForOptionWriter(op.new_axis_mask(), fbb);
  auto shrink_axis_mask = ConvertI32AttrForOptionWriter(op.shrink_axis_mask(), fbb);
  tflite::StridedSliceOptionsBuilder b(*fbb);
  b.add_begin_mask(std::move(begin_mask));
  b.add_end_mask(std::move(end_mask));
  b.add_ellipsis_mask(std::move(ellipsis_mask));
  b.add_new_axis_mask(std::move(new_axis_mask));
  b.add_shrink_axis_mask(std::move(shrink_axis_mask));
  return b.Finish();
}
flatbuffers::Offset<tflite::SubOptions> CreateSubOptions(mlir::TFL::SubOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  tflite::SubOptionsBuilder b(*fbb);
  b.add_fused_activation_function(std::move(fused_activation_function));
  return b.Finish();
}
flatbuffers::Offset<tflite::ReducerOptions> CreateReducerOptions(mlir::TFL::SumOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto keep_dims = ConvertBoolAttrForOptionWriter(op.keep_dims(), fbb);
  tflite::ReducerOptionsBuilder b(*fbb);
  b.add_keep_dims(std::move(keep_dims));
  return b.Finish();
}
flatbuffers::Offset<tflite::TopKV2Options> CreateTopKV2Options(mlir::TFL::TopKV2Op op, flatbuffers::FlatBufferBuilder *fbb) {
  tflite::TopKV2OptionsBuilder b(*fbb);
  return b.Finish();
}
flatbuffers::Offset<tflite::TransposeConvOptions> CreateTransposeConvOptions(mlir::TFL::TransposeConvOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto padding = ConvertTFL_PaddingAttrForOptionWriter(op.padding(), fbb);
  auto stride_h = ConvertI32AttrForOptionWriter(op.stride_h(), fbb);
  auto stride_w = ConvertI32AttrForOptionWriter(op.stride_w(), fbb);
  tflite::TransposeConvOptionsBuilder b(*fbb);
  b.add_padding(std::move(padding));
  b.add_stride_h(std::move(stride_h));
  b.add_stride_w(std::move(stride_w));
  return b.Finish();
}
flatbuffers::Offset<tflite::UnidirectionalSequenceLSTMOptions> CreateUnidirectionalSequenceLSTMOptions(mlir::TFL::UnidirectionalSequenceLSTMOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  auto cell_clip = ConvertF32AttrForOptionWriter(op.cell_clip(), fbb);
  auto proj_clip = ConvertF32AttrForOptionWriter(op.proj_clip(), fbb);
  auto time_major = ConvertBoolAttrForOptionWriter(op.time_major(), fbb);
  auto asymmetric_quantize_inputs = ConvertBoolAttrForOptionWriter(op.asymmetric_quantize_inputs(), fbb);
  tflite::UnidirectionalSequenceLSTMOptionsBuilder b(*fbb);
  b.add_fused_activation_function(std::move(fused_activation_function));
  b.add_cell_clip(std::move(cell_clip));
  b.add_proj_clip(std::move(proj_clip));
  b.add_time_major(std::move(time_major));
  b.add_asymmetric_quantize_inputs(std::move(asymmetric_quantize_inputs));
  return b.Finish();
}
flatbuffers::Offset<tflite::SequenceRNNOptions> CreateSequenceRNNOptions(mlir::TFL::UnidirectionalSequenceRNNOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto time_major = ConvertBoolAttrForOptionWriter(op.time_major(), fbb);
  auto fused_activation_function = ConvertTFL_AFAttrForOptionWriter(op.fused_activation_function(), fbb);
  auto asymmetric_quantize_inputs = ConvertBoolAttrForOptionWriter(op.asymmetric_quantize_inputs(), fbb);
  tflite::SequenceRNNOptionsBuilder b(*fbb);
  b.add_time_major(std::move(time_major));
  b.add_fused_activation_function(std::move(fused_activation_function));
  b.add_asymmetric_quantize_inputs(std::move(asymmetric_quantize_inputs));
  return b.Finish();
}
flatbuffers::Offset<tflite::UniqueOptions> CreateUniqueOptions(mlir::TFL::UniqueOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto idx_out_type = ConvertDerivedTFLiteTypeAttrForOptionWriter(op.idx_out_type(), fbb);
  tflite::UniqueOptionsBuilder b(*fbb);
  b.add_idx_out_type(std::move(idx_out_type));
  return b.Finish();
}
flatbuffers::Offset<tflite::UnpackOptions> CreateUnpackOptions(mlir::TFL::UnpackOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto num = ConvertI32AttrForOptionWriter(op.num(), fbb);
  auto axis = ConvertI32AttrForOptionWriter(op.axis(), fbb);
  tflite::UnpackOptionsBuilder b(*fbb);
  b.add_num(std::move(num));
  b.add_axis(std::move(axis));
  return b.Finish();
}
flatbuffers::Offset<tflite::VarHandleOptions> CreateVarHandleOptions(mlir::TFL::VarHandleOp op, flatbuffers::FlatBufferBuilder *fbb) {
  auto container = ConvertStrAttrForOptionWriter(op.container(), fbb);
  auto shared_name = ConvertStrAttrForOptionWriter(op.shared_name(), fbb);
  tflite::VarHandleOptionsBuilder b(*fbb);
  b.add_container(std::move(container));
  b.add_shared_name(std::move(shared_name));
  return b.Finish();
}
flatbuffers::Offset<tflite::ZerosLikeOptions> CreateZerosLikeOptions(mlir::TFL::ZerosLikeOp op, flatbuffers::FlatBufferBuilder *fbb) {
  tflite::ZerosLikeOptionsBuilder b(*fbb);
  return b.Finish();
}


static flatbuffers::Offset<tflite::Operator> CreateAbsOperator(mlir::TFL::AbsOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateAddNOperator(mlir::TFL::AddNOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateAddOperator(mlir::TFL::AddOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_AddOptions, CreateAddOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateArgMaxOperator(mlir::TFL::ArgMaxOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ArgMaxOptions, CreateArgMaxOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateArgMinOperator(mlir::TFL::ArgMinOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ArgMinOptions, CreateArgMinOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateAssignVariableOperator(mlir::TFL::AssignVariableOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateAveragePool2DOperator(mlir::TFL::AveragePool2DOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_Pool2DOptions, CreatePool2DOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateBasicLSTMOperator(mlir::TFL::BasicLSTMOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,const std::vector<int32_t>& intermediate_index,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  auto intermediates = fbb->CreateVector(intermediate_index);
  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_LSTMOptions, CreateBasicLSTMOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0, intermediates);
}

static flatbuffers::Offset<tflite::Operator> CreateBatchMatMulOperator(mlir::TFL::BatchMatMulOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_BatchMatMulOptions, CreateBatchMatMulOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateBatchToSpaceNdOperator(mlir::TFL::BatchToSpaceNdOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateBidirectionalSequenceLSTMOperator(mlir::TFL::BidirectionalSequenceLSTMOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,const std::vector<int32_t>& intermediate_index,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  auto intermediates = fbb->CreateVector(intermediate_index);
  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_BidirectionalSequenceLSTMOptions, CreateBidirectionalSequenceLSTMOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0, intermediates);
}

static flatbuffers::Offset<tflite::Operator> CreateBroadcastArgsOperator(mlir::TFL::BroadcastArgsOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateBroadcastToOperator(mlir::TFL::BroadcastToOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateBucketizeOperator(mlir::TFL::BucketizeOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_BucketizeOptions, CreateBucketizeOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateCallOnceOperator(mlir::TFL::CallOnceOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateCastOperator(mlir::TFL::CastOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateCeilOperator(mlir::TFL::CeilOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateComplexAbsOperator(mlir::TFL::ComplexAbsOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateConcatenationOperator(mlir::TFL::ConcatenationOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ConcatenationOptions, CreateConcatenationOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateConv2DOperator(mlir::TFL::Conv2DOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_Conv2DOptions, CreateConv2DOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateConv3DOperator(mlir::TFL::Conv3DOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_Conv3DOptions, CreateConv3DOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateConv3DTransposeOperator(mlir::TFL::Conv3DTransposeOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_Conv3DOptions, CreateConv3DOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateCosOperator(mlir::TFL::CosOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateCumsumOperator(mlir::TFL::CumsumOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_CumsumOptions, CreateCumsumOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateDensifyOperator(mlir::TFL::DensifyOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateDepthToSpaceOperator(mlir::TFL::DepthToSpaceOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_DepthToSpaceOptions, CreateDepthToSpaceOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateDepthwiseConv2DOperator(mlir::TFL::DepthwiseConv2DOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_DepthwiseConv2DOptions, CreateDepthwiseConv2DOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateDequantizeOperator(mlir::TFL::DequantizeOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateDivOperator(mlir::TFL::DivOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_DivOptions, CreateDivOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateEluOperator(mlir::TFL::EluOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateEmbeddingLookupOperator(mlir::TFL::EmbeddingLookupOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateEqualOperator(mlir::TFL::EqualOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateExpOperator(mlir::TFL::ExpOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ExpOptions, CreateExpOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateExpandDimsOperator(mlir::TFL::ExpandDimsOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ExpandDimsOptions, CreateExpandDimsOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateFakeQuantOperator(mlir::TFL::FakeQuantOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_FakeQuantOptions, CreateFakeQuantOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateFillOperator(mlir::TFL::FillOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateFloorDivOperator(mlir::TFL::FloorDivOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateFloorModOperator(mlir::TFL::FloorModOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateFloorOperator(mlir::TFL::FloorOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateFullyConnectedOperator(mlir::TFL::FullyConnectedOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_FullyConnectedOptions, CreateFullyConnectedOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateGatherNdOperator(mlir::TFL::GatherNdOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateGatherOperator(mlir::TFL::GatherOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_GatherOptions, CreateGatherOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateGreaterEqualOperator(mlir::TFL::GreaterEqualOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateGreaterOperator(mlir::TFL::GreaterOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateHardSwishOperator(mlir::TFL::HardSwishOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateHashtableFindOperator(mlir::TFL::HashtableFindOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateHashtableImportOperator(mlir::TFL::HashtableImportOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateHashtableOperator(mlir::TFL::HashtableOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_HashtableOptions, CreateHashtableOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateHashtableSizeOperator(mlir::TFL::HashtableSizeOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateImagOperator(mlir::TFL::ImagOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateL2NormalizationOperator(mlir::TFL::L2NormalizationOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_L2NormOptions, CreateL2NormOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateLSTMOperator(mlir::TFL::LSTMOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,const std::vector<int32_t>& intermediate_index,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  auto intermediates = fbb->CreateVector(intermediate_index);
  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_LSTMOptions, CreateLSTMOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0, intermediates);
}

static flatbuffers::Offset<tflite::Operator> CreateLeakyReluOperator(mlir::TFL::LeakyReluOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_LeakyReluOptions, CreateLeakyReluOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateLessEqualOperator(mlir::TFL::LessEqualOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateLessOperator(mlir::TFL::LessOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateLocalResponseNormalizationOperator(mlir::TFL::LocalResponseNormalizationOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_LocalResponseNormalizationOptions, CreateLocalResponseNormalizationOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateLogOperator(mlir::TFL::LogOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateLogSoftmaxOperator(mlir::TFL::LogSoftmaxOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_LogSoftmaxOptions, CreateLogSoftmaxOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateLogicalAndOperator(mlir::TFL::LogicalAndOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateLogicalNotOperator(mlir::TFL::LogicalNotOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateLogicalOrOperator(mlir::TFL::LogicalOrOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateLogisticOperator(mlir::TFL::LogisticOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateMatrixDiagOperator(mlir::TFL::MatrixDiagOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateMatrixSetDiagOperator(mlir::TFL::MatrixSetDiagOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateMaxPool2DOperator(mlir::TFL::MaxPool2DOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_Pool2DOptions, CreatePool2DOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateMaximumOperator(mlir::TFL::MaximumOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateMeanOperator(mlir::TFL::MeanOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ReducerOptions, CreateReducerOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateMinimumOperator(mlir::TFL::MinimumOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateMirrorPadOperator(mlir::TFL::MirrorPadOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_MirrorPadOptions, CreateMirrorPadOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateMulOperator(mlir::TFL::MulOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_MulOptions, CreateMulOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateMultinomialOperator(mlir::TFL::MultinomialOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_RandomOptions, CreateRandomOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateNegOperator(mlir::TFL::NegOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NegOptions, CreateNegOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateNonMaxSuppressionV4Operator(mlir::TFL::NonMaxSuppressionV4Op tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateNonMaxSuppressionV5Operator(mlir::TFL::NonMaxSuppressionV5Op tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateNotEqualOperator(mlir::TFL::NotEqualOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateOneHotOperator(mlir::TFL::OneHotOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_OneHotOptions, CreateOneHotOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreatePReluOperator(mlir::TFL::PReluOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreatePackOperator(mlir::TFL::PackOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_PackOptions, CreatePackOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreatePadOperator(mlir::TFL::PadOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_PadOptions, CreatePadOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreatePadV2Operator(mlir::TFL::PadV2Op tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_PadV2Options, CreatePadV2Options(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreatePowOperator(mlir::TFL::PowOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateQuantizeOperator(mlir::TFL::QuantizeOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateRFFT2dOperator(mlir::TFL::RFFT2dOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateRandomStandardNormalOperator(mlir::TFL::RandomStandardNormalOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_RandomOptions, CreateRandomOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateRandomUniformOperator(mlir::TFL::RandomUniformOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_RandomOptions, CreateRandomOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateRangeOperator(mlir::TFL::RangeOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateRankOperator(mlir::TFL::RankOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateReadVariableOperator(mlir::TFL::ReadVariableOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateRealOperator(mlir::TFL::RealOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateReduceAllOperator(mlir::TFL::ReduceAllOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ReducerOptions, CreateReducerOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateReduceAnyOperator(mlir::TFL::ReduceAnyOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ReducerOptions, CreateReducerOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateReduceMaxOperator(mlir::TFL::ReduceMaxOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ReducerOptions, CreateReducerOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateReduceMinOperator(mlir::TFL::ReduceMinOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ReducerOptions, CreateReducerOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateReduceProdOperator(mlir::TFL::ReduceProdOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ReducerOptions, CreateReducerOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateRelu1Operator(mlir::TFL::Relu1Op tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateRelu6Operator(mlir::TFL::Relu6Op tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateReluOperator(mlir::TFL::ReluOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateReshapeOperator(mlir::TFL::ReshapeOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateResizeBilinearOperator(mlir::TFL::ResizeBilinearOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ResizeBilinearOptions, CreateResizeBilinearOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateResizeNearestNeighborOperator(mlir::TFL::ResizeNearestNeighborOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ResizeNearestNeighborOptions, CreateResizeNearestNeighborOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateReverseSequenceOperator(mlir::TFL::ReverseSequenceOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ReverseSequenceOptions, CreateReverseSequenceOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateReverseV2Operator(mlir::TFL::ReverseV2Op tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateRoundOperator(mlir::TFL::RoundOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateRsqrtOperator(mlir::TFL::RsqrtOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSVDFOperator(mlir::TFL::SVDFOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_SVDFOptions, CreateSVDFOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateScatterNdOperator(mlir::TFL::ScatterNdOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ScatterNdOptions, CreateScatterNdOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSegmentSumOperator(mlir::TFL::SegmentSumOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSelectOperator(mlir::TFL::SelectOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_SelectOptions, CreateSelectOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSelectV2Operator(mlir::TFL::SelectV2Op tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_SelectV2Options, CreateSelectV2Options(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateShapeOperator(mlir::TFL::ShapeOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ShapeOptions, CreateShapeOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSinOperator(mlir::TFL::SinOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSliceOperator(mlir::TFL::SliceOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSoftmaxOperator(mlir::TFL::SoftmaxOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_SoftmaxOptions, CreateSoftmaxOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSpaceToBatchNdOperator(mlir::TFL::SpaceToBatchNdOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSpaceToDepthOperator(mlir::TFL::SpaceToDepthOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_SpaceToDepthOptions, CreateSpaceToDepthOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSparseToDenseOperator(mlir::TFL::SparseToDenseOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSplitOperator(mlir::TFL::SplitOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_SplitOptions, CreateSplitOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSplitVOperator(mlir::TFL::SplitVOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_SplitVOptions, CreateSplitVOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSqrtOperator(mlir::TFL::SqrtOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSquareOperator(mlir::TFL::SquareOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_SquareOptions, CreateSquareOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSquaredDifferenceOperator(mlir::TFL::SquaredDifferenceOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSqueezeOperator(mlir::TFL::SqueezeOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_SqueezeOptions, CreateSqueezeOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateStridedSliceOperator(mlir::TFL::StridedSliceOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_StridedSliceOptions, CreateStridedSliceOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSubOperator(mlir::TFL::SubOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_SubOptions, CreateSubOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateSumOperator(mlir::TFL::SumOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ReducerOptions, CreateReducerOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateTanhOperator(mlir::TFL::TanhOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateTileOperator(mlir::TFL::TileOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateTopKV2Operator(mlir::TFL::TopKV2Op tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_TopKV2Options, CreateTopKV2Options(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateTransposeConvOperator(mlir::TFL::TransposeConvOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_TransposeConvOptions, CreateTransposeConvOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateTransposeOperator(mlir::TFL::TransposeOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateUnidirectionalSequenceLSTMOperator(mlir::TFL::UnidirectionalSequenceLSTMOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,const std::vector<int32_t>& intermediate_index,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  auto intermediates = fbb->CreateVector(intermediate_index);
  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_UnidirectionalSequenceLSTMOptions, CreateUnidirectionalSequenceLSTMOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0, intermediates);
}

static flatbuffers::Offset<tflite::Operator> CreateUnidirectionalSequenceRNNOperator(mlir::TFL::UnidirectionalSequenceRNNOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_SequenceRNNOptions, CreateSequenceRNNOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateUniqueOperator(mlir::TFL::UniqueOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_UniqueOptions, CreateUniqueOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateUnpackOperator(mlir::TFL::UnpackOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_UnpackOptions, CreateUnpackOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateVarHandleOperator(mlir::TFL::VarHandleOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_VarHandleOptions, CreateVarHandleOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateWhereOperator(mlir::TFL::WhereOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_NONE, /*builtin_options=*/0,
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}

static flatbuffers::Offset<tflite::Operator> CreateZerosLikeOperator(mlir::TFL::ZerosLikeOp tflOp, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,flatbuffers::FlatBufferBuilder *fbb) {
  auto inputs = fbb->CreateVector(operands);
  auto outputs = fbb->CreateVector(results);

  return tflite::CreateOperator(
      *fbb, opcode_index, inputs, outputs,
      tflite::BuiltinOptions_ZerosLikeOptions, CreateZerosLikeOptions(tflOp, fbb).Union(),
      /*custom_options=*/0, tflite::CustomOptionsFormat_FLEXBUFFERS,
      /*mutating_variable_inputs=*/0);
}



llvm::Optional<tflite::BuiltinOperator> mlir::GetBuiltinOpCode(mlir::Operation* op) {
  if (isa<mlir::TFL::AbsOp>(op))
    return tflite::BuiltinOperator_ABS;
  if (isa<mlir::TFL::AddNOp>(op))
    return tflite::BuiltinOperator_ADD_N;
  if (isa<mlir::TFL::AddOp>(op))
    return tflite::BuiltinOperator_ADD;
  if (isa<mlir::TFL::ArgMaxOp>(op))
    return tflite::BuiltinOperator_ARG_MAX;
  if (isa<mlir::TFL::ArgMinOp>(op))
    return tflite::BuiltinOperator_ARG_MIN;
  if (isa<mlir::TFL::AssignVariableOp>(op))
    return tflite::BuiltinOperator_ASSIGN_VARIABLE;
  if (isa<mlir::TFL::AveragePool2DOp>(op))
    return tflite::BuiltinOperator_AVERAGE_POOL_2D;
  if (isa<mlir::TFL::BasicLSTMOp>(op))
    return tflite::BuiltinOperator_LSTM;
  if (isa<mlir::TFL::BatchMatMulOp>(op))
    return tflite::BuiltinOperator_BATCH_MATMUL;
  if (isa<mlir::TFL::BatchToSpaceNdOp>(op))
    return tflite::BuiltinOperator_BATCH_TO_SPACE_ND;
  if (isa<mlir::TFL::BidirectionalSequenceLSTMOp>(op))
    return tflite::BuiltinOperator_BIDIRECTIONAL_SEQUENCE_LSTM;
  if (isa<mlir::TFL::BroadcastArgsOp>(op))
    return tflite::BuiltinOperator_BROADCAST_ARGS;
  if (isa<mlir::TFL::BroadcastToOp>(op))
    return tflite::BuiltinOperator_BROADCAST_TO;
  if (isa<mlir::TFL::BucketizeOp>(op))
    return tflite::BuiltinOperator_BUCKETIZE;
  if (isa<mlir::TFL::CallOnceOp>(op))
    return tflite::BuiltinOperator_CALL_ONCE;
  if (isa<mlir::TFL::CastOp>(op))
    return tflite::BuiltinOperator_CAST;
  if (isa<mlir::TFL::CeilOp>(op))
    return tflite::BuiltinOperator_CEIL;
  if (isa<mlir::TFL::ComplexAbsOp>(op))
    return tflite::BuiltinOperator_COMPLEX_ABS;
  if (isa<mlir::TFL::ConcatenationOp>(op))
    return tflite::BuiltinOperator_CONCATENATION;
  if (isa<mlir::TFL::Conv2DOp>(op))
    return tflite::BuiltinOperator_CONV_2D;
  if (isa<mlir::TFL::Conv3DOp>(op))
    return tflite::BuiltinOperator_CONV_3D;
  if (isa<mlir::TFL::Conv3DTransposeOp>(op))
    return tflite::BuiltinOperator_CONV_3D_TRANSPOSE;
  if (isa<mlir::TFL::CosOp>(op))
    return tflite::BuiltinOperator_COS;
  if (isa<mlir::TFL::CumsumOp>(op))
    return tflite::BuiltinOperator_CUMSUM;
  if (isa<mlir::TFL::DensifyOp>(op))
    return tflite::BuiltinOperator_DENSIFY;
  if (isa<mlir::TFL::DepthToSpaceOp>(op))
    return tflite::BuiltinOperator_DEPTH_TO_SPACE;
  if (isa<mlir::TFL::DepthwiseConv2DOp>(op))
    return tflite::BuiltinOperator_DEPTHWISE_CONV_2D;
  if (isa<mlir::TFL::DequantizeOp>(op))
    return tflite::BuiltinOperator_DEQUANTIZE;
  if (isa<mlir::TFL::DivOp>(op))
    return tflite::BuiltinOperator_DIV;
  if (isa<mlir::TFL::EluOp>(op))
    return tflite::BuiltinOperator_ELU;
  if (isa<mlir::TFL::EmbeddingLookupOp>(op))
    return tflite::BuiltinOperator_EMBEDDING_LOOKUP;
  if (isa<mlir::TFL::EqualOp>(op))
    return tflite::BuiltinOperator_EQUAL;
  if (isa<mlir::TFL::ExpOp>(op))
    return tflite::BuiltinOperator_EXP;
  if (isa<mlir::TFL::ExpandDimsOp>(op))
    return tflite::BuiltinOperator_EXPAND_DIMS;
  if (isa<mlir::TFL::FakeQuantOp>(op))
    return tflite::BuiltinOperator_FAKE_QUANT;
  if (isa<mlir::TFL::FillOp>(op))
    return tflite::BuiltinOperator_FILL;
  if (isa<mlir::TFL::FloorDivOp>(op))
    return tflite::BuiltinOperator_FLOOR_DIV;
  if (isa<mlir::TFL::FloorModOp>(op))
    return tflite::BuiltinOperator_FLOOR_MOD;
  if (isa<mlir::TFL::FloorOp>(op))
    return tflite::BuiltinOperator_FLOOR;
  if (isa<mlir::TFL::FullyConnectedOp>(op))
    return tflite::BuiltinOperator_FULLY_CONNECTED;
  if (isa<mlir::TFL::GatherNdOp>(op))
    return tflite::BuiltinOperator_GATHER_ND;
  if (isa<mlir::TFL::GatherOp>(op))
    return tflite::BuiltinOperator_GATHER;
  if (isa<mlir::TFL::GreaterEqualOp>(op))
    return tflite::BuiltinOperator_GREATER_EQUAL;
  if (isa<mlir::TFL::GreaterOp>(op))
    return tflite::BuiltinOperator_GREATER;
  if (isa<mlir::TFL::HardSwishOp>(op))
    return tflite::BuiltinOperator_HARD_SWISH;
  if (isa<mlir::TFL::HashtableFindOp>(op))
    return tflite::BuiltinOperator_HASHTABLE_FIND;
  if (isa<mlir::TFL::HashtableImportOp>(op))
    return tflite::BuiltinOperator_HASHTABLE_IMPORT;
  if (isa<mlir::TFL::HashtableOp>(op))
    return tflite::BuiltinOperator_HASHTABLE;
  if (isa<mlir::TFL::HashtableSizeOp>(op))
    return tflite::BuiltinOperator_HASHTABLE_SIZE;
  if (isa<mlir::TFL::ImagOp>(op))
    return tflite::BuiltinOperator_IMAG;
  if (isa<mlir::TFL::L2NormalizationOp>(op))
    return tflite::BuiltinOperator_L2_NORMALIZATION;
  if (isa<mlir::TFL::LSTMOp>(op))
    return tflite::BuiltinOperator_LSTM;
  if (isa<mlir::TFL::LeakyReluOp>(op))
    return tflite::BuiltinOperator_LEAKY_RELU;
  if (isa<mlir::TFL::LessEqualOp>(op))
    return tflite::BuiltinOperator_LESS_EQUAL;
  if (isa<mlir::TFL::LessOp>(op))
    return tflite::BuiltinOperator_LESS;
  if (isa<mlir::TFL::LocalResponseNormalizationOp>(op))
    return tflite::BuiltinOperator_LOCAL_RESPONSE_NORMALIZATION;
  if (isa<mlir::TFL::LogOp>(op))
    return tflite::BuiltinOperator_LOG;
  if (isa<mlir::TFL::LogSoftmaxOp>(op))
    return tflite::BuiltinOperator_LOG_SOFTMAX;
  if (isa<mlir::TFL::LogicalAndOp>(op))
    return tflite::BuiltinOperator_LOGICAL_AND;
  if (isa<mlir::TFL::LogicalNotOp>(op))
    return tflite::BuiltinOperator_LOGICAL_NOT;
  if (isa<mlir::TFL::LogicalOrOp>(op))
    return tflite::BuiltinOperator_LOGICAL_OR;
  if (isa<mlir::TFL::LogisticOp>(op))
    return tflite::BuiltinOperator_LOGISTIC;
  if (isa<mlir::TFL::MatrixDiagOp>(op))
    return tflite::BuiltinOperator_MATRIX_DIAG;
  if (isa<mlir::TFL::MatrixSetDiagOp>(op))
    return tflite::BuiltinOperator_MATRIX_SET_DIAG;
  if (isa<mlir::TFL::MaxPool2DOp>(op))
    return tflite::BuiltinOperator_MAX_POOL_2D;
  if (isa<mlir::TFL::MaximumOp>(op))
    return tflite::BuiltinOperator_MAXIMUM;
  if (isa<mlir::TFL::MeanOp>(op))
    return tflite::BuiltinOperator_MEAN;
  if (isa<mlir::TFL::MinimumOp>(op))
    return tflite::BuiltinOperator_MINIMUM;
  if (isa<mlir::TFL::MirrorPadOp>(op))
    return tflite::BuiltinOperator_MIRROR_PAD;
  if (isa<mlir::TFL::MulOp>(op))
    return tflite::BuiltinOperator_MUL;
  if (isa<mlir::TFL::MultinomialOp>(op))
    return tflite::BuiltinOperator_MULTINOMIAL;
  if (isa<mlir::TFL::NegOp>(op))
    return tflite::BuiltinOperator_NEG;
  if (isa<mlir::TFL::NonMaxSuppressionV4Op>(op))
    return tflite::BuiltinOperator_NON_MAX_SUPPRESSION_V4;
  if (isa<mlir::TFL::NonMaxSuppressionV5Op>(op))
    return tflite::BuiltinOperator_NON_MAX_SUPPRESSION_V5;
  if (isa<mlir::TFL::NotEqualOp>(op))
    return tflite::BuiltinOperator_NOT_EQUAL;
  if (isa<mlir::TFL::OneHotOp>(op))
    return tflite::BuiltinOperator_ONE_HOT;
  if (isa<mlir::TFL::PReluOp>(op))
    return tflite::BuiltinOperator_PRELU;
  if (isa<mlir::TFL::PackOp>(op))
    return tflite::BuiltinOperator_PACK;
  if (isa<mlir::TFL::PadOp>(op))
    return tflite::BuiltinOperator_PAD;
  if (isa<mlir::TFL::PadV2Op>(op))
    return tflite::BuiltinOperator_PADV2;
  if (isa<mlir::TFL::PowOp>(op))
    return tflite::BuiltinOperator_POW;
  if (isa<mlir::TFL::QuantizeOp>(op))
    return tflite::BuiltinOperator_QUANTIZE;
  if (isa<mlir::TFL::RFFT2dOp>(op))
    return tflite::BuiltinOperator_RFFT2D;
  if (isa<mlir::TFL::RandomStandardNormalOp>(op))
    return tflite::BuiltinOperator_RANDOM_STANDARD_NORMAL;
  if (isa<mlir::TFL::RandomUniformOp>(op))
    return tflite::BuiltinOperator_RANDOM_UNIFORM;
  if (isa<mlir::TFL::RangeOp>(op))
    return tflite::BuiltinOperator_RANGE;
  if (isa<mlir::TFL::RankOp>(op))
    return tflite::BuiltinOperator_RANK;
  if (isa<mlir::TFL::ReadVariableOp>(op))
    return tflite::BuiltinOperator_READ_VARIABLE;
  if (isa<mlir::TFL::RealOp>(op))
    return tflite::BuiltinOperator_REAL;
  if (isa<mlir::TFL::ReduceAllOp>(op))
    return tflite::BuiltinOperator_REDUCE_ALL;
  if (isa<mlir::TFL::ReduceAnyOp>(op))
    return tflite::BuiltinOperator_REDUCE_ANY;
  if (isa<mlir::TFL::ReduceMaxOp>(op))
    return tflite::BuiltinOperator_REDUCE_MAX;
  if (isa<mlir::TFL::ReduceMinOp>(op))
    return tflite::BuiltinOperator_REDUCE_MIN;
  if (isa<mlir::TFL::ReduceProdOp>(op))
    return tflite::BuiltinOperator_REDUCE_PROD;
  if (isa<mlir::TFL::Relu1Op>(op))
    return tflite::BuiltinOperator_RELU_N1_TO_1;
  if (isa<mlir::TFL::Relu6Op>(op))
    return tflite::BuiltinOperator_RELU6;
  if (isa<mlir::TFL::ReluOp>(op))
    return tflite::BuiltinOperator_RELU;
  if (isa<mlir::TFL::ReshapeOp>(op))
    return tflite::BuiltinOperator_RESHAPE;
  if (isa<mlir::TFL::ResizeBilinearOp>(op))
    return tflite::BuiltinOperator_RESIZE_BILINEAR;
  if (isa<mlir::TFL::ResizeNearestNeighborOp>(op))
    return tflite::BuiltinOperator_RESIZE_NEAREST_NEIGHBOR;
  if (isa<mlir::TFL::ReverseSequenceOp>(op))
    return tflite::BuiltinOperator_REVERSE_SEQUENCE;
  if (isa<mlir::TFL::ReverseV2Op>(op))
    return tflite::BuiltinOperator_REVERSE_V2;
  if (isa<mlir::TFL::RoundOp>(op))
    return tflite::BuiltinOperator_ROUND;
  if (isa<mlir::TFL::RsqrtOp>(op))
    return tflite::BuiltinOperator_RSQRT;
  if (isa<mlir::TFL::SVDFOp>(op))
    return tflite::BuiltinOperator_SVDF;
  if (isa<mlir::TFL::ScatterNdOp>(op))
    return tflite::BuiltinOperator_SCATTER_ND;
  if (isa<mlir::TFL::SegmentSumOp>(op))
    return tflite::BuiltinOperator_SEGMENT_SUM;
  if (isa<mlir::TFL::SelectOp>(op))
    return tflite::BuiltinOperator_SELECT;
  if (isa<mlir::TFL::SelectV2Op>(op))
    return tflite::BuiltinOperator_SELECT_V2;
  if (isa<mlir::TFL::ShapeOp>(op))
    return tflite::BuiltinOperator_SHAPE;
  if (isa<mlir::TFL::SinOp>(op))
    return tflite::BuiltinOperator_SIN;
  if (isa<mlir::TFL::SliceOp>(op))
    return tflite::BuiltinOperator_SLICE;
  if (isa<mlir::TFL::SoftmaxOp>(op))
    return tflite::BuiltinOperator_SOFTMAX;
  if (isa<mlir::TFL::SpaceToBatchNdOp>(op))
    return tflite::BuiltinOperator_SPACE_TO_BATCH_ND;
  if (isa<mlir::TFL::SpaceToDepthOp>(op))
    return tflite::BuiltinOperator_SPACE_TO_DEPTH;
  if (isa<mlir::TFL::SparseToDenseOp>(op))
    return tflite::BuiltinOperator_SPARSE_TO_DENSE;
  if (isa<mlir::TFL::SplitOp>(op))
    return tflite::BuiltinOperator_SPLIT;
  if (isa<mlir::TFL::SplitVOp>(op))
    return tflite::BuiltinOperator_SPLIT_V;
  if (isa<mlir::TFL::SqrtOp>(op))
    return tflite::BuiltinOperator_SQRT;
  if (isa<mlir::TFL::SquareOp>(op))
    return tflite::BuiltinOperator_SQUARE;
  if (isa<mlir::TFL::SquaredDifferenceOp>(op))
    return tflite::BuiltinOperator_SQUARED_DIFFERENCE;
  if (isa<mlir::TFL::SqueezeOp>(op))
    return tflite::BuiltinOperator_SQUEEZE;
  if (isa<mlir::TFL::StridedSliceOp>(op))
    return tflite::BuiltinOperator_STRIDED_SLICE;
  if (isa<mlir::TFL::SubOp>(op))
    return tflite::BuiltinOperator_SUB;
  if (isa<mlir::TFL::SumOp>(op))
    return tflite::BuiltinOperator_SUM;
  if (isa<mlir::TFL::TanhOp>(op))
    return tflite::BuiltinOperator_TANH;
  if (isa<mlir::TFL::TileOp>(op))
    return tflite::BuiltinOperator_TILE;
  if (isa<mlir::TFL::TopKV2Op>(op))
    return tflite::BuiltinOperator_TOPK_V2;
  if (isa<mlir::TFL::TransposeConvOp>(op))
    return tflite::BuiltinOperator_TRANSPOSE_CONV;
  if (isa<mlir::TFL::TransposeOp>(op))
    return tflite::BuiltinOperator_TRANSPOSE;
  if (isa<mlir::TFL::UnidirectionalSequenceLSTMOp>(op))
    return tflite::BuiltinOperator_UNIDIRECTIONAL_SEQUENCE_LSTM;
  if (isa<mlir::TFL::UnidirectionalSequenceRNNOp>(op))
    return tflite::BuiltinOperator_UNIDIRECTIONAL_SEQUENCE_RNN;
  if (isa<mlir::TFL::UniqueOp>(op))
    return tflite::BuiltinOperator_UNIQUE;
  if (isa<mlir::TFL::UnpackOp>(op))
    return tflite::BuiltinOperator_UNPACK;
  if (isa<mlir::TFL::VarHandleOp>(op))
    return tflite::BuiltinOperator_VAR_HANDLE;
  if (isa<mlir::TFL::WhereOp>(op))
    return tflite::BuiltinOperator_WHERE;
  if (isa<mlir::TFL::ZerosLikeOp>(op))
    return tflite::BuiltinOperator_ZEROS_LIKE;
  return llvm::None;
}


llvm::Optional<flatbuffers::Offset<tflite::Operator>>
mlir::CreateFlatBufferOperator(mlir::Operation* op, uint32_t opcode_index, const std::vector<int32_t>& operands,const std::vector<int32_t>& results,const std::vector<int32_t>& intermediates,flatbuffers::FlatBufferBuilder *fbb) {
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::AbsOp>(op))
    return CreateAbsOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::AddNOp>(op))
    return CreateAddNOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::AddOp>(op))
    return CreateAddOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ArgMaxOp>(op))
    return CreateArgMaxOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ArgMinOp>(op))
    return CreateArgMinOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::AssignVariableOp>(op))
    return CreateAssignVariableOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::AveragePool2DOp>(op))
    return CreateAveragePool2DOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::BasicLSTMOp>(op))
    return CreateBasicLSTMOperator(tflOp, opcode_index, operands, results, intermediates, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::BatchMatMulOp>(op))
    return CreateBatchMatMulOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::BatchToSpaceNdOp>(op))
    return CreateBatchToSpaceNdOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::BidirectionalSequenceLSTMOp>(op))
    return CreateBidirectionalSequenceLSTMOperator(tflOp, opcode_index, operands, results, intermediates, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::BroadcastArgsOp>(op))
    return CreateBroadcastArgsOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::BroadcastToOp>(op))
    return CreateBroadcastToOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::BucketizeOp>(op))
    return CreateBucketizeOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::CallOnceOp>(op))
    return CreateCallOnceOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::CastOp>(op))
    return CreateCastOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::CeilOp>(op))
    return CreateCeilOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ComplexAbsOp>(op))
    return CreateComplexAbsOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ConcatenationOp>(op))
    return CreateConcatenationOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::Conv2DOp>(op))
    return CreateConv2DOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::Conv3DOp>(op))
    return CreateConv3DOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::Conv3DTransposeOp>(op))
    return CreateConv3DTransposeOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::CosOp>(op))
    return CreateCosOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::CumsumOp>(op))
    return CreateCumsumOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::DensifyOp>(op))
    return CreateDensifyOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::DepthToSpaceOp>(op))
    return CreateDepthToSpaceOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::DepthwiseConv2DOp>(op))
    return CreateDepthwiseConv2DOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::DequantizeOp>(op))
    return CreateDequantizeOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::DivOp>(op))
    return CreateDivOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::EluOp>(op))
    return CreateEluOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::EmbeddingLookupOp>(op))
    return CreateEmbeddingLookupOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::EqualOp>(op))
    return CreateEqualOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ExpOp>(op))
    return CreateExpOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ExpandDimsOp>(op))
    return CreateExpandDimsOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::FakeQuantOp>(op))
    return CreateFakeQuantOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::FillOp>(op))
    return CreateFillOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::FloorDivOp>(op))
    return CreateFloorDivOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::FloorModOp>(op))
    return CreateFloorModOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::FloorOp>(op))
    return CreateFloorOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::FullyConnectedOp>(op))
    return CreateFullyConnectedOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::GatherNdOp>(op))
    return CreateGatherNdOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::GatherOp>(op))
    return CreateGatherOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::GreaterEqualOp>(op))
    return CreateGreaterEqualOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::GreaterOp>(op))
    return CreateGreaterOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::HardSwishOp>(op))
    return CreateHardSwishOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::HashtableFindOp>(op))
    return CreateHashtableFindOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::HashtableImportOp>(op))
    return CreateHashtableImportOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::HashtableOp>(op))
    return CreateHashtableOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::HashtableSizeOp>(op))
    return CreateHashtableSizeOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ImagOp>(op))
    return CreateImagOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::L2NormalizationOp>(op))
    return CreateL2NormalizationOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::LSTMOp>(op))
    return CreateLSTMOperator(tflOp, opcode_index, operands, results, intermediates, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::LeakyReluOp>(op))
    return CreateLeakyReluOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::LessEqualOp>(op))
    return CreateLessEqualOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::LessOp>(op))
    return CreateLessOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::LocalResponseNormalizationOp>(op))
    return CreateLocalResponseNormalizationOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::LogOp>(op))
    return CreateLogOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::LogSoftmaxOp>(op))
    return CreateLogSoftmaxOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::LogicalAndOp>(op))
    return CreateLogicalAndOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::LogicalNotOp>(op))
    return CreateLogicalNotOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::LogicalOrOp>(op))
    return CreateLogicalOrOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::LogisticOp>(op))
    return CreateLogisticOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::MatrixDiagOp>(op))
    return CreateMatrixDiagOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::MatrixSetDiagOp>(op))
    return CreateMatrixSetDiagOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::MaxPool2DOp>(op))
    return CreateMaxPool2DOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::MaximumOp>(op))
    return CreateMaximumOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::MeanOp>(op))
    return CreateMeanOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::MinimumOp>(op))
    return CreateMinimumOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::MirrorPadOp>(op))
    return CreateMirrorPadOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::MulOp>(op))
    return CreateMulOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::MultinomialOp>(op))
    return CreateMultinomialOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::NegOp>(op))
    return CreateNegOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::NonMaxSuppressionV4Op>(op))
    return CreateNonMaxSuppressionV4Operator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::NonMaxSuppressionV5Op>(op))
    return CreateNonMaxSuppressionV5Operator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::NotEqualOp>(op))
    return CreateNotEqualOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::OneHotOp>(op))
    return CreateOneHotOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::PReluOp>(op))
    return CreatePReluOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::PackOp>(op))
    return CreatePackOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::PadOp>(op))
    return CreatePadOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::PadV2Op>(op))
    return CreatePadV2Operator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::PowOp>(op))
    return CreatePowOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::QuantizeOp>(op))
    return CreateQuantizeOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::RFFT2dOp>(op))
    return CreateRFFT2dOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::RandomStandardNormalOp>(op))
    return CreateRandomStandardNormalOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::RandomUniformOp>(op))
    return CreateRandomUniformOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::RangeOp>(op))
    return CreateRangeOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::RankOp>(op))
    return CreateRankOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ReadVariableOp>(op))
    return CreateReadVariableOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::RealOp>(op))
    return CreateRealOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ReduceAllOp>(op))
    return CreateReduceAllOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ReduceAnyOp>(op))
    return CreateReduceAnyOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ReduceMaxOp>(op))
    return CreateReduceMaxOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ReduceMinOp>(op))
    return CreateReduceMinOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ReduceProdOp>(op))
    return CreateReduceProdOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::Relu1Op>(op))
    return CreateRelu1Operator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::Relu6Op>(op))
    return CreateRelu6Operator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ReluOp>(op))
    return CreateReluOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ReshapeOp>(op))
    return CreateReshapeOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ResizeBilinearOp>(op))
    return CreateResizeBilinearOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ResizeNearestNeighborOp>(op))
    return CreateResizeNearestNeighborOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ReverseSequenceOp>(op))
    return CreateReverseSequenceOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ReverseV2Op>(op))
    return CreateReverseV2Operator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::RoundOp>(op))
    return CreateRoundOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::RsqrtOp>(op))
    return CreateRsqrtOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SVDFOp>(op))
    return CreateSVDFOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ScatterNdOp>(op))
    return CreateScatterNdOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SegmentSumOp>(op))
    return CreateSegmentSumOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SelectOp>(op))
    return CreateSelectOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SelectV2Op>(op))
    return CreateSelectV2Operator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ShapeOp>(op))
    return CreateShapeOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SinOp>(op))
    return CreateSinOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SliceOp>(op))
    return CreateSliceOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SoftmaxOp>(op))
    return CreateSoftmaxOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SpaceToBatchNdOp>(op))
    return CreateSpaceToBatchNdOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SpaceToDepthOp>(op))
    return CreateSpaceToDepthOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SparseToDenseOp>(op))
    return CreateSparseToDenseOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SplitOp>(op))
    return CreateSplitOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SplitVOp>(op))
    return CreateSplitVOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SqrtOp>(op))
    return CreateSqrtOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SquareOp>(op))
    return CreateSquareOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SquaredDifferenceOp>(op))
    return CreateSquaredDifferenceOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SqueezeOp>(op))
    return CreateSqueezeOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::StridedSliceOp>(op))
    return CreateStridedSliceOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SubOp>(op))
    return CreateSubOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::SumOp>(op))
    return CreateSumOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::TanhOp>(op))
    return CreateTanhOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::TileOp>(op))
    return CreateTileOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::TopKV2Op>(op))
    return CreateTopKV2Operator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::TransposeConvOp>(op))
    return CreateTransposeConvOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::TransposeOp>(op))
    return CreateTransposeOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::UnidirectionalSequenceLSTMOp>(op))
    return CreateUnidirectionalSequenceLSTMOperator(tflOp, opcode_index, operands, results, intermediates, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::UnidirectionalSequenceRNNOp>(op))
    return CreateUnidirectionalSequenceRNNOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::UniqueOp>(op))
    return CreateUniqueOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::UnpackOp>(op))
    return CreateUnpackOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::VarHandleOp>(op))
    return CreateVarHandleOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::WhereOp>(op))
    return CreateWhereOperator(tflOp, opcode_index, operands, results, fbb);
  if (auto tflOp = llvm::dyn_cast<mlir::TFL::ZerosLikeOp>(op))
    return CreateZerosLikeOperator(tflOp, opcode_index, operands, results, fbb);
  return llvm::None;
}


void mlir::BuiltinOptionsToAttributes(tflite::BuiltinOptionsUnion op_union, mlir::Builder builder, llvm::SmallVectorImpl<mlir::NamedAttribute> &attributes) {
  if(const auto *op = op_union.AsAddOptions()) {
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    return;
  }
  if(const auto *op = op_union.AsArgMaxOptions()) {
    return;
  }
  if(const auto *op = op_union.AsArgMinOptions()) {
    return;
  }
  if(const auto *op = op_union.AsPool2DOptions()) {
    attributes.emplace_back(builder.getNamedAttr("filter_height", BuildI32Attr(op->filter_height, builder)));
    attributes.emplace_back(builder.getNamedAttr("filter_width", BuildI32Attr(op->filter_width, builder)));
    attributes.emplace_back(builder.getNamedAttr("padding", BuildTFL_PaddingAttr(op->padding, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_h", BuildI32Attr(op->stride_h, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_w", BuildI32Attr(op->stride_w, builder)));
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    return;
  }
  if(const auto *op = op_union.AsBatchMatMulOptions()) {
    attributes.emplace_back(builder.getNamedAttr("adj_x", BuildBoolAttr(op->adj_x, builder)));
    attributes.emplace_back(builder.getNamedAttr("adj_y", BuildBoolAttr(op->adj_y, builder)));
    attributes.emplace_back(builder.getNamedAttr("asymmetric_quantize_inputs", BuildBoolAttr(op->asymmetric_quantize_inputs, builder)));
    return;
  }
  if(const auto *op = op_union.AsBidirectionalSequenceLSTMOptions()) {
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    attributes.emplace_back(builder.getNamedAttr("cell_clip", BuildF32Attr(op->cell_clip, builder)));
    attributes.emplace_back(builder.getNamedAttr("proj_clip", BuildF32Attr(op->proj_clip, builder)));
    attributes.emplace_back(builder.getNamedAttr("merge_outputs", BuildBoolAttr(op->merge_outputs, builder)));
    attributes.emplace_back(builder.getNamedAttr("time_major", BuildBoolAttr(op->time_major, builder)));
    attributes.emplace_back(builder.getNamedAttr("asymmetric_quantize_inputs", BuildBoolAttr(op->asymmetric_quantize_inputs, builder)));
    return;
  }
  if(const auto *op = op_union.AsBucketizeOptions()) {
    attributes.emplace_back(builder.getNamedAttr("boundaries", BuildF32ArrayAttr(op->boundaries, builder)));
    return;
  }
  if(const auto *op = op_union.AsConcatenationOptions()) {
    attributes.emplace_back(builder.getNamedAttr("axis", BuildI32Attr(op->axis, builder)));
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    return;
  }
  if(const auto *op = op_union.AsConv2DOptions()) {
    attributes.emplace_back(builder.getNamedAttr("dilation_h_factor", BuildI32Attr(op->dilation_h_factor, builder)));
    attributes.emplace_back(builder.getNamedAttr("dilation_w_factor", BuildI32Attr(op->dilation_w_factor, builder)));
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    attributes.emplace_back(builder.getNamedAttr("padding", BuildTFL_PaddingAttr(op->padding, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_h", BuildI32Attr(op->stride_h, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_w", BuildI32Attr(op->stride_w, builder)));
    return;
  }
  if(const auto *op = op_union.AsConv3DOptions()) {
    attributes.emplace_back(builder.getNamedAttr("dilation_d_factor", BuildI32Attr(op->dilation_d_factor, builder)));
    attributes.emplace_back(builder.getNamedAttr("dilation_h_factor", BuildI32Attr(op->dilation_h_factor, builder)));
    attributes.emplace_back(builder.getNamedAttr("dilation_w_factor", BuildI32Attr(op->dilation_w_factor, builder)));
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    attributes.emplace_back(builder.getNamedAttr("padding", BuildTFL_PaddingAttr(op->padding, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_d", BuildI32Attr(op->stride_d, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_h", BuildI32Attr(op->stride_h, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_w", BuildI32Attr(op->stride_w, builder)));
    return;
  }
  if(const auto *op = op_union.AsConv3DOptions()) {
    attributes.emplace_back(builder.getNamedAttr("dilation_d_factor", BuildI32Attr(op->dilation_d_factor, builder)));
    attributes.emplace_back(builder.getNamedAttr("dilation_h_factor", BuildI32Attr(op->dilation_h_factor, builder)));
    attributes.emplace_back(builder.getNamedAttr("dilation_w_factor", BuildI32Attr(op->dilation_w_factor, builder)));
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    attributes.emplace_back(builder.getNamedAttr("padding", BuildTFL_PaddingAttr(op->padding, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_d", BuildI32Attr(op->stride_d, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_h", BuildI32Attr(op->stride_h, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_w", BuildI32Attr(op->stride_w, builder)));
    return;
  }
  if(const auto *op = op_union.AsCumsumOptions()) {
    attributes.emplace_back(builder.getNamedAttr("exclusive", BuildBoolAttr(op->exclusive, builder)));
    attributes.emplace_back(builder.getNamedAttr("reverse", BuildBoolAttr(op->reverse, builder)));
    return;
  }
  if(const auto *op = op_union.AsDepthToSpaceOptions()) {
    attributes.emplace_back(builder.getNamedAttr("block_size", BuildI32Attr(op->block_size, builder)));
    return;
  }
  if(const auto *op = op_union.AsDepthwiseConv2DOptions()) {
    attributes.emplace_back(builder.getNamedAttr("dilation_h_factor", BuildI32Attr(op->dilation_h_factor, builder)));
    attributes.emplace_back(builder.getNamedAttr("dilation_w_factor", BuildI32Attr(op->dilation_w_factor, builder)));
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    attributes.emplace_back(builder.getNamedAttr("padding", BuildTFL_PaddingAttr(op->padding, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_h", BuildI32Attr(op->stride_h, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_w", BuildI32Attr(op->stride_w, builder)));
    attributes.emplace_back(builder.getNamedAttr("depth_multiplier", BuildI32Attr(op->depth_multiplier, builder)));
    return;
  }
  if(const auto *op = op_union.AsDivOptions()) {
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    return;
  }
  if(const auto *op = op_union.AsExpOptions()) {
    return;
  }
  if(const auto *op = op_union.AsExpandDimsOptions()) {
    return;
  }
  if(const auto *op = op_union.AsFakeQuantOptions()) {
    attributes.emplace_back(builder.getNamedAttr("min", BuildF32Attr(op->min, builder)));
    attributes.emplace_back(builder.getNamedAttr("max", BuildF32Attr(op->max, builder)));
    attributes.emplace_back(builder.getNamedAttr("num_bits", BuildI32Attr(op->num_bits, builder)));
    attributes.emplace_back(builder.getNamedAttr("narrow_range", BuildBoolAttr(op->narrow_range, builder)));
    return;
  }
  if(const auto *op = op_union.AsFullyConnectedOptions()) {
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    attributes.emplace_back(builder.getNamedAttr("weights_format", BuildTFL_FullyConnectedOptionsWeightFormatAttr(op->weights_format, builder)));
    attributes.emplace_back(builder.getNamedAttr("keep_num_dims", BuildBoolAttr(op->keep_num_dims, builder)));
    attributes.emplace_back(builder.getNamedAttr("asymmetric_quantize_inputs", BuildBoolAttr(op->asymmetric_quantize_inputs, builder)));
    return;
  }
  if(const auto *op = op_union.AsGatherOptions()) {
    attributes.emplace_back(builder.getNamedAttr("axis", BuildI32Attr(op->axis, builder)));
    attributes.emplace_back(builder.getNamedAttr("batch_dims", BuildI32Attr(op->batch_dims, builder)));
    return;
  }
  if(const auto *op = op_union.AsHashtableOptions()) {
    attributes.emplace_back(builder.getNamedAttr("table_id", BuildI32Attr(op->table_id, builder)));
    attributes.emplace_back(builder.getNamedAttr("key_dtype", BuildTypeAttr(op->key_dtype, builder)));
    attributes.emplace_back(builder.getNamedAttr("value_dtype", BuildTypeAttr(op->value_dtype, builder)));
    return;
  }
  if(const auto *op = op_union.AsL2NormOptions()) {
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    return;
  }
  if(const auto *op = op_union.AsLSTMOptions()) {
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    attributes.emplace_back(builder.getNamedAttr("cell_clip", BuildF32Attr(op->cell_clip, builder)));
    attributes.emplace_back(builder.getNamedAttr("proj_clip", BuildF32Attr(op->proj_clip, builder)));
    attributes.emplace_back(builder.getNamedAttr("kernel_type", BuildTFL_LSTMKernelTypeAttr(op->kernel_type, builder)));
    attributes.emplace_back(builder.getNamedAttr("asymmetric_quantize_inputs", BuildBoolAttr(op->asymmetric_quantize_inputs, builder)));
    return;
  }
  if(const auto *op = op_union.AsLeakyReluOptions()) {
    attributes.emplace_back(builder.getNamedAttr("alpha", BuildF32Attr(op->alpha, builder)));
    return;
  }
  if(const auto *op = op_union.AsLocalResponseNormalizationOptions()) {
    attributes.emplace_back(builder.getNamedAttr("radius", BuildI32Attr(op->radius, builder)));
    attributes.emplace_back(builder.getNamedAttr("bias", BuildF32Attr(op->bias, builder)));
    attributes.emplace_back(builder.getNamedAttr("alpha", BuildF32Attr(op->alpha, builder)));
    attributes.emplace_back(builder.getNamedAttr("beta", BuildF32Attr(op->beta, builder)));
    return;
  }
  if(const auto *op = op_union.AsLogSoftmaxOptions()) {
    return;
  }
  if(const auto *op = op_union.AsPool2DOptions()) {
    attributes.emplace_back(builder.getNamedAttr("padding", BuildTFL_PaddingAttr(op->padding, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_w", BuildI32Attr(op->stride_w, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_h", BuildI32Attr(op->stride_h, builder)));
    attributes.emplace_back(builder.getNamedAttr("filter_width", BuildI32Attr(op->filter_width, builder)));
    attributes.emplace_back(builder.getNamedAttr("filter_height", BuildI32Attr(op->filter_height, builder)));
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    return;
  }
  if(const auto *op = op_union.AsReducerOptions()) {
    attributes.emplace_back(builder.getNamedAttr("keep_dims", BuildBoolAttr(op->keep_dims, builder)));
    return;
  }
  if(const auto *op = op_union.AsMirrorPadOptions()) {
    attributes.emplace_back(builder.getNamedAttr("mode", BuildTFL_MirrorPaddingAttr(op->mode, builder)));
    return;
  }
  if(const auto *op = op_union.AsMulOptions()) {
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    return;
  }
  if(const auto *op = op_union.AsRandomOptions()) {
    attributes.emplace_back(builder.getNamedAttr("seed", BuildI64Attr(op->seed, builder)));
    attributes.emplace_back(builder.getNamedAttr("seed2", BuildI64Attr(op->seed2, builder)));
    return;
  }
  if(const auto *op = op_union.AsNegOptions()) {
    return;
  }
  if(const auto *op = op_union.AsOneHotOptions()) {
    attributes.emplace_back(builder.getNamedAttr("axis", BuildI32Attr(op->axis, builder)));
    return;
  }
  if(const auto *op = op_union.AsPackOptions()) {
    attributes.emplace_back(builder.getNamedAttr("values_count", BuildI32Attr(op->values_count, builder)));
    attributes.emplace_back(builder.getNamedAttr("axis", BuildI32Attr(op->axis, builder)));
    return;
  }
  if(const auto *op = op_union.AsPadOptions()) {
    return;
  }
  if(const auto *op = op_union.AsPadV2Options()) {
    return;
  }
  if(const auto *op = op_union.AsRandomOptions()) {
    attributes.emplace_back(builder.getNamedAttr("seed", BuildI64Attr(op->seed, builder)));
    attributes.emplace_back(builder.getNamedAttr("seed2", BuildI64Attr(op->seed2, builder)));
    return;
  }
  if(const auto *op = op_union.AsRandomOptions()) {
    attributes.emplace_back(builder.getNamedAttr("seed", BuildI64Attr(op->seed, builder)));
    attributes.emplace_back(builder.getNamedAttr("seed2", BuildI64Attr(op->seed2, builder)));
    return;
  }
  if(const auto *op = op_union.AsReducerOptions()) {
    attributes.emplace_back(builder.getNamedAttr("keep_dims", BuildBoolAttr(op->keep_dims, builder)));
    return;
  }
  if(const auto *op = op_union.AsReducerOptions()) {
    attributes.emplace_back(builder.getNamedAttr("keep_dims", BuildBoolAttr(op->keep_dims, builder)));
    return;
  }
  if(const auto *op = op_union.AsReducerOptions()) {
    attributes.emplace_back(builder.getNamedAttr("keep_dims", BuildBoolAttr(op->keep_dims, builder)));
    return;
  }
  if(const auto *op = op_union.AsReducerOptions()) {
    attributes.emplace_back(builder.getNamedAttr("keep_dims", BuildBoolAttr(op->keep_dims, builder)));
    return;
  }
  if(const auto *op = op_union.AsReducerOptions()) {
    attributes.emplace_back(builder.getNamedAttr("keep_dims", BuildBoolAttr(op->keep_dims, builder)));
    return;
  }
  if(const auto *op = op_union.AsResizeBilinearOptions()) {
    attributes.emplace_back(builder.getNamedAttr("align_corners", BuildBoolAttr(op->align_corners, builder)));
    attributes.emplace_back(builder.getNamedAttr("half_pixel_centers", BuildBoolAttr(op->half_pixel_centers, builder)));
    return;
  }
  if(const auto *op = op_union.AsResizeNearestNeighborOptions()) {
    attributes.emplace_back(builder.getNamedAttr("align_corners", BuildBoolAttr(op->align_corners, builder)));
    attributes.emplace_back(builder.getNamedAttr("half_pixel_centers", BuildBoolAttr(op->half_pixel_centers, builder)));
    return;
  }
  if(const auto *op = op_union.AsReverseSequenceOptions()) {
    attributes.emplace_back(builder.getNamedAttr("seq_dim", BuildI32Attr(op->seq_dim, builder)));
    attributes.emplace_back(builder.getNamedAttr("batch_dim", BuildI32Attr(op->batch_dim, builder)));
    return;
  }
  if(const auto *op = op_union.AsSVDFOptions()) {
    attributes.emplace_back(builder.getNamedAttr("rank", BuildI32Attr(op->rank, builder)));
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    attributes.emplace_back(builder.getNamedAttr("asymmetric_quantize_inputs", BuildBoolAttr(op->asymmetric_quantize_inputs, builder)));
    return;
  }
  if(const auto *op = op_union.AsScatterNdOptions()) {
    return;
  }
  if(const auto *op = op_union.AsSelectOptions()) {
    return;
  }
  if(const auto *op = op_union.AsSelectV2Options()) {
    return;
  }
  if(const auto *op = op_union.AsShapeOptions()) {
    return;
  }
  if(const auto *op = op_union.AsSoftmaxOptions()) {
    attributes.emplace_back(builder.getNamedAttr("beta", BuildF32Attr(op->beta, builder)));
    return;
  }
  if(const auto *op = op_union.AsSpaceToDepthOptions()) {
    attributes.emplace_back(builder.getNamedAttr("block_size", BuildI32Attr(op->block_size, builder)));
    return;
  }
  if(const auto *op = op_union.AsSplitOptions()) {
    attributes.emplace_back(builder.getNamedAttr("num_splits", BuildI32Attr(op->num_splits, builder)));
    return;
  }
  if(const auto *op = op_union.AsSplitVOptions()) {
    attributes.emplace_back(builder.getNamedAttr("num_splits", BuildI32Attr(op->num_splits, builder)));
    return;
  }
  if(const auto *op = op_union.AsSquareOptions()) {
    return;
  }
  if(const auto *op = op_union.AsSqueezeOptions()) {
    attributes.emplace_back(builder.getNamedAttr("squeeze_dims", BuildI64ArrayAttr(op->squeeze_dims, builder)));
    return;
  }
  if(const auto *op = op_union.AsStridedSliceOptions()) {
    attributes.emplace_back(builder.getNamedAttr("begin_mask", BuildI32Attr(op->begin_mask, builder)));
    attributes.emplace_back(builder.getNamedAttr("end_mask", BuildI32Attr(op->end_mask, builder)));
    attributes.emplace_back(builder.getNamedAttr("ellipsis_mask", BuildI32Attr(op->ellipsis_mask, builder)));
    attributes.emplace_back(builder.getNamedAttr("new_axis_mask", BuildI32Attr(op->new_axis_mask, builder)));
    attributes.emplace_back(builder.getNamedAttr("shrink_axis_mask", BuildI32Attr(op->shrink_axis_mask, builder)));
    return;
  }
  if(const auto *op = op_union.AsSubOptions()) {
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    return;
  }
  if(const auto *op = op_union.AsReducerOptions()) {
    attributes.emplace_back(builder.getNamedAttr("keep_dims", BuildBoolAttr(op->keep_dims, builder)));
    return;
  }
  if(const auto *op = op_union.AsTopKV2Options()) {
    return;
  }
  if(const auto *op = op_union.AsTransposeConvOptions()) {
    attributes.emplace_back(builder.getNamedAttr("padding", BuildTFL_PaddingAttr(op->padding, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_h", BuildI32Attr(op->stride_h, builder)));
    attributes.emplace_back(builder.getNamedAttr("stride_w", BuildI32Attr(op->stride_w, builder)));
    return;
  }
  if(const auto *op = op_union.AsUnidirectionalSequenceLSTMOptions()) {
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    attributes.emplace_back(builder.getNamedAttr("cell_clip", BuildF32Attr(op->cell_clip, builder)));
    attributes.emplace_back(builder.getNamedAttr("proj_clip", BuildF32Attr(op->proj_clip, builder)));
    attributes.emplace_back(builder.getNamedAttr("time_major", BuildBoolAttr(op->time_major, builder)));
    attributes.emplace_back(builder.getNamedAttr("asymmetric_quantize_inputs", BuildBoolAttr(op->asymmetric_quantize_inputs, builder)));
    return;
  }
  if(const auto *op = op_union.AsSequenceRNNOptions()) {
    attributes.emplace_back(builder.getNamedAttr("time_major", BuildBoolAttr(op->time_major, builder)));
    attributes.emplace_back(builder.getNamedAttr("fused_activation_function", BuildTFL_AFAttr(op->fused_activation_function, builder)));
    attributes.emplace_back(builder.getNamedAttr("asymmetric_quantize_inputs", BuildBoolAttr(op->asymmetric_quantize_inputs, builder)));
    return;
  }
  if(const auto *op = op_union.AsUniqueOptions()) {
    return;
  }
  if(const auto *op = op_union.AsUnpackOptions()) {
    attributes.emplace_back(builder.getNamedAttr("num", BuildI32Attr(op->num, builder)));
    attributes.emplace_back(builder.getNamedAttr("axis", BuildI32Attr(op->axis, builder)));
    return;
  }
  if(const auto *op = op_union.AsVarHandleOptions()) {
    attributes.emplace_back(builder.getNamedAttr("container", BuildStrAttr(op->container, builder)));
    attributes.emplace_back(builder.getNamedAttr("shared_name", BuildStrAttr(op->shared_name, builder)));
    return;
  }
  if(const auto *op = op_union.AsZerosLikeOptions()) {
    return;
  }
}

llvm::MinMax mlir::OperandNumbersMinMax(llvm::StringRef op_name) {
  if (op_name == "tfl.abs") {
    return {1, 1};
  }
  if (op_name == "tfl.add_n") {
    return {1, 1};
  }
  if (op_name == "tfl.add") {
    return {2, 2};
  }
  if (op_name == "tfl.arg_max") {
    return {2, 2};
  }
  if (op_name == "tfl.arg_min") {
    return {2, 2};
  }
  if (op_name == "tfl.assign_variable") {
    return {2, 2};
  }
  if (op_name == "tfl.average_pool_2d") {
    return {1, 1};
  }
  if (op_name == "tfl.basic_lstm") {
    return {5, 5};
  }
  if (op_name == "tfl.batch_matmul") {
    return {2, 2};
  }
  if (op_name == "tfl.batch_to_space_nd") {
    return {3, 3};
  }
  if (op_name == "tfl.bidirectional_sequence_lstm") {
    return {39, 48};
  }
  if (op_name == "tfl.broadcast_args") {
    return {2, 2};
  }
  if (op_name == "tfl.broadcast_to") {
    return {2, 2};
  }
  if (op_name == "tfl.bucketize") {
    return {1, 1};
  }
  if (op_name == "tfl.call_once") {
    return {0, 0};
  }
  if (op_name == "tfl.cast") {
    return {1, 1};
  }
  if (op_name == "tfl.ceil") {
    return {1, 1};
  }
  if (op_name == "tfl.complex_abs") {
    return {1, 1};
  }
  if (op_name == "tfl.concatenation") {
    return {1, 1};
  }
  if (op_name == "tfl.conv_2d") {
    return {2, 3};
  }
  if (op_name == "tfl.conv_3d") {
    return {2, 3};
  }
  if (op_name == "tfl.conv_3d_transpose") {
    return {3, 4};
  }
  if (op_name == "tfl.cos") {
    return {1, 1};
  }
  if (op_name == "tfl.cumsum") {
    return {2, 2};
  }
  if (op_name == "tfl.densify") {
    return {1, 1};
  }
  if (op_name == "tfl.depth_to_space") {
    return {1, 1};
  }
  if (op_name == "tfl.depthwise_conv_2d") {
    return {3, 3};
  }
  if (op_name == "tfl.dequantize") {
    return {1, 1};
  }
  if (op_name == "tfl.div") {
    return {2, 2};
  }
  if (op_name == "tfl.elu") {
    return {1, 1};
  }
  if (op_name == "tfl.embedding_lookup") {
    return {2, 2};
  }
  if (op_name == "tfl.equal") {
    return {2, 2};
  }
  if (op_name == "tfl.exp") {
    return {1, 1};
  }
  if (op_name == "tfl.expand_dims") {
    return {2, 2};
  }
  if (op_name == "tfl.fake_quant") {
    return {1, 1};
  }
  if (op_name == "tfl.fill") {
    return {2, 2};
  }
  if (op_name == "tfl.floor_div") {
    return {2, 2};
  }
  if (op_name == "tfl.floor_mod") {
    return {2, 2};
  }
  if (op_name == "tfl.floor") {
    return {1, 1};
  }
  if (op_name == "tfl.fully_connected") {
    return {2, 3};
  }
  if (op_name == "tfl.gather_nd") {
    return {2, 2};
  }
  if (op_name == "tfl.gather") {
    return {2, 2};
  }
  if (op_name == "tfl.greater_equal") {
    return {2, 2};
  }
  if (op_name == "tfl.greater") {
    return {2, 2};
  }
  if (op_name == "tfl.hard_swish") {
    return {1, 1};
  }
  if (op_name == "tfl.hashtable_find") {
    return {3, 3};
  }
  if (op_name == "tfl.hashtable_import") {
    return {3, 3};
  }
  if (op_name == "tfl.hashtable") {
    return {0, 0};
  }
  if (op_name == "tfl.hashtable_size") {
    return {1, 1};
  }
  if (op_name == "tfl.imag") {
    return {1, 1};
  }
  if (op_name == "tfl.l2_normalization") {
    return {1, 1};
  }
  if (op_name == "tfl.lstm") {
    return {20, 24};
  }
  if (op_name == "tfl.leaky_relu") {
    return {1, 1};
  }
  if (op_name == "tfl.less_equal") {
    return {2, 2};
  }
  if (op_name == "tfl.less") {
    return {2, 2};
  }
  if (op_name == "tfl.local_response_normalization") {
    return {1, 1};
  }
  if (op_name == "tfl.log") {
    return {1, 1};
  }
  if (op_name == "tfl.log_softmax") {
    return {1, 1};
  }
  if (op_name == "tfl.logical_and") {
    return {2, 2};
  }
  if (op_name == "tfl.logical_not") {
    return {1, 1};
  }
  if (op_name == "tfl.logical_or") {
    return {2, 2};
  }
  if (op_name == "tfl.logistic") {
    return {1, 1};
  }
  if (op_name == "tfl.matrix_diag") {
    return {1, 1};
  }
  if (op_name == "tfl.matrix_set_diag") {
    return {2, 2};
  }
  if (op_name == "tfl.max_pool_2d") {
    return {1, 1};
  }
  if (op_name == "tfl.maximum") {
    return {2, 2};
  }
  if (op_name == "tfl.mean") {
    return {2, 2};
  }
  if (op_name == "tfl.minimum") {
    return {2, 2};
  }
  if (op_name == "tfl.mirror_pad") {
    return {2, 2};
  }
  if (op_name == "tfl.mul") {
    return {2, 2};
  }
  if (op_name == "tfl.multinomial") {
    return {2, 2};
  }
  if (op_name == "tfl.neg") {
    return {1, 1};
  }
  if (op_name == "tfl.non_max_suppression_v4") {
    return {5, 5};
  }
  if (op_name == "tfl.non_max_suppression_v5") {
    return {6, 6};
  }
  if (op_name == "tfl.not_equal") {
    return {2, 2};
  }
  if (op_name == "tfl.one_hot") {
    return {4, 4};
  }
  if (op_name == "tfl.prelu") {
    return {2, 2};
  }
  if (op_name == "tfl.pack") {
    return {1, 1};
  }
  if (op_name == "tfl.pad") {
    return {2, 2};
  }
  if (op_name == "tfl.padv2") {
    return {3, 3};
  }
  if (op_name == "tfl.pow") {
    return {2, 2};
  }
  if (op_name == "tfl.quantize") {
    return {1, 1};
  }
  if (op_name == "tfl.rfft2d") {
    return {2, 2};
  }
  if (op_name == "tfl.random_standard_normal") {
    return {1, 1};
  }
  if (op_name == "tfl.random_uniform") {
    return {1, 1};
  }
  if (op_name == "tfl.range") {
    return {3, 3};
  }
  if (op_name == "tfl.rank") {
    return {1, 1};
  }
  if (op_name == "tfl.read_variable") {
    return {1, 1};
  }
  if (op_name == "tfl.real") {
    return {1, 1};
  }
  if (op_name == "tfl.reduce_all") {
    return {2, 2};
  }
  if (op_name == "tfl.reduce_any") {
    return {2, 2};
  }
  if (op_name == "tfl.reduce_max") {
    return {2, 2};
  }
  if (op_name == "tfl.reduce_min") {
    return {2, 2};
  }
  if (op_name == "tfl.reduce_prod") {
    return {2, 2};
  }
  if (op_name == "tfl.relu_n1_to_1") {
    return {1, 1};
  }
  if (op_name == "tfl.relu6") {
    return {1, 1};
  }
  if (op_name == "tfl.relu") {
    return {1, 1};
  }
  if (op_name == "tfl.reshape") {
    return {2, 2};
  }
  if (op_name == "tfl.resize_bilinear") {
    return {2, 2};
  }
  if (op_name == "tfl.resize_nearest_neighbor") {
    return {2, 2};
  }
  if (op_name == "tfl.reverse_sequence") {
    return {2, 2};
  }
  if (op_name == "tfl.reverse_v2") {
    return {2, 2};
  }
  if (op_name == "tfl.round") {
    return {1, 1};
  }
  if (op_name == "tfl.rsqrt") {
    return {1, 1};
  }
  if (op_name == "tfl.svdf") {
    return {5, 5};
  }
  if (op_name == "tfl.scatter_nd") {
    return {3, 3};
  }
  if (op_name == "tfl.segment_sum") {
    return {2, 2};
  }
  if (op_name == "tfl.select") {
    return {3, 3};
  }
  if (op_name == "tfl.select_v2") {
    return {3, 3};
  }
  if (op_name == "tfl.shape") {
    return {1, 1};
  }
  if (op_name == "tfl.sin") {
    return {1, 1};
  }
  if (op_name == "tfl.slice") {
    return {3, 3};
  }
  if (op_name == "tfl.softmax") {
    return {1, 1};
  }
  if (op_name == "tfl.space_to_batch_nd") {
    return {3, 3};
  }
  if (op_name == "tfl.space_to_depth") {
    return {1, 1};
  }
  if (op_name == "tfl.sparse_to_dense") {
    return {4, 4};
  }
  if (op_name == "tfl.split") {
    return {2, 2};
  }
  if (op_name == "tfl.split_v") {
    return {3, 3};
  }
  if (op_name == "tfl.sqrt") {
    return {1, 1};
  }
  if (op_name == "tfl.square") {
    return {1, 1};
  }
  if (op_name == "tfl.squared_difference") {
    return {2, 2};
  }
  if (op_name == "tfl.squeeze") {
    return {1, 1};
  }
  if (op_name == "tfl.strided_slice") {
    return {4, 4};
  }
  if (op_name == "tfl.sub") {
    return {2, 2};
  }
  if (op_name == "tfl.sum") {
    return {2, 2};
  }
  if (op_name == "tfl.tanh") {
    return {1, 1};
  }
  if (op_name == "tfl.tile") {
    return {2, 2};
  }
  if (op_name == "tfl.topk_v2") {
    return {2, 2};
  }
  if (op_name == "tfl.transpose_conv") {
    return {3, 4};
  }
  if (op_name == "tfl.transpose") {
    return {2, 2};
  }
  if (op_name == "tfl.unidirectional_sequence_lstm") {
    return {20, 24};
  }
  if (op_name == "tfl.unidirectional_sequence_rnn") {
    return {5, 5};
  }
  if (op_name == "tfl.unique") {
    return {1, 1};
  }
  if (op_name == "tfl.unpack") {
    return {1, 1};
  }
  if (op_name == "tfl.var_handle") {
    return {0, 0};
  }
  if (op_name == "tfl.where") {
    return {1, 1};
  }
  if (op_name == "tfl.zeros_like") {
    return {1, 1};
  }
  return {0, 0};
}
