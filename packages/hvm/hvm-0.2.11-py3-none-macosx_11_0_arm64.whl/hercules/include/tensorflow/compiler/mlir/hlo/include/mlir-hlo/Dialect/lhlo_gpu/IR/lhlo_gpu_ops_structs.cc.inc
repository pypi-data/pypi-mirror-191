/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Struct Utility Definitions                                                 *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace lmhlo_gpu {
ConvolutionBackendConfig ConvolutionBackendConfig::get(
    ::mlir::IntegerAttr algorithm,
    ::mlir::BoolAttr tensor_ops_enabled,
    ::mlir::ArrayAttr knob_ids,
    ::mlir::ArrayAttr knob_values,
    ::mlir::BoolAttr is_cudnn_frontend,
    ::mlir::IntegerAttr workspace_size,
    ::mlir::ArrayAttr operand_0_layout,
    ::mlir::ArrayAttr operand_1_layout,
    ::mlir::ArrayAttr result_layout,
    ::mlir::MLIRContext* context) {
  ::llvm::SmallVector<::mlir::NamedAttribute, 9> fields;

  assert(algorithm);
  auto algorithm_id = ::mlir::StringAttr::get(context, "algorithm");
  fields.emplace_back(algorithm_id, algorithm);

  assert(tensor_ops_enabled);
  auto tensor_ops_enabled_id = ::mlir::StringAttr::get(context, "tensor_ops_enabled");
  fields.emplace_back(tensor_ops_enabled_id, tensor_ops_enabled);

  assert(knob_ids);
  auto knob_ids_id = ::mlir::StringAttr::get(context, "knob_ids");
  fields.emplace_back(knob_ids_id, knob_ids);

  assert(knob_values);
  auto knob_values_id = ::mlir::StringAttr::get(context, "knob_values");
  fields.emplace_back(knob_values_id, knob_values);

  assert(is_cudnn_frontend);
  auto is_cudnn_frontend_id = ::mlir::StringAttr::get(context, "is_cudnn_frontend");
  fields.emplace_back(is_cudnn_frontend_id, is_cudnn_frontend);

  assert(workspace_size);
  auto workspace_size_id = ::mlir::StringAttr::get(context, "workspace_size");
  fields.emplace_back(workspace_size_id, workspace_size);

  assert(operand_0_layout);
  auto operand_0_layout_id = ::mlir::StringAttr::get(context, "operand_0_layout");
  fields.emplace_back(operand_0_layout_id, operand_0_layout);

  assert(operand_1_layout);
  auto operand_1_layout_id = ::mlir::StringAttr::get(context, "operand_1_layout");
  fields.emplace_back(operand_1_layout_id, operand_1_layout);

  assert(result_layout);
  auto result_layout_id = ::mlir::StringAttr::get(context, "result_layout");
  fields.emplace_back(result_layout_id, result_layout);

  ::mlir::Attribute dict = ::mlir::DictionaryAttr::get(context, fields);
  return dict.dyn_cast<ConvolutionBackendConfig>();
}

bool ConvolutionBackendConfig::classof(::mlir::Attribute attr) {
  if (!attr)
    return false;
  auto derived = attr.dyn_cast<::mlir::DictionaryAttr>();
  if (!derived)
    return false;
  int num_absent_attrs = 0;

  auto algorithm = derived.get("algorithm");
  if (!algorithm || !(((algorithm.isa<::mlir::IntegerAttr>())) && ((algorithm.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64)))))
    return false;

  auto tensor_ops_enabled = derived.get("tensor_ops_enabled");
  if (!tensor_ops_enabled || !((tensor_ops_enabled.isa<::mlir::BoolAttr>())))
    return false;

  auto knob_ids = derived.get("knob_ids");
  if (!knob_ids || !(((knob_ids.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(knob_ids.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64))); }))))
    return false;

  auto knob_values = derived.get("knob_values");
  if (!knob_values || !(((knob_values.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(knob_values.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64))); }))))
    return false;

  auto is_cudnn_frontend = derived.get("is_cudnn_frontend");
  if (!is_cudnn_frontend || !((is_cudnn_frontend.isa<::mlir::BoolAttr>())))
    return false;

  auto workspace_size = derived.get("workspace_size");
  if (!workspace_size || !(((workspace_size.isa<::mlir::IntegerAttr>())) && ((workspace_size.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64)))))
    return false;

  auto operand_0_layout = derived.get("operand_0_layout");
  if (!operand_0_layout || !(((operand_0_layout.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(operand_0_layout.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64))); }))))
    return false;

  auto operand_1_layout = derived.get("operand_1_layout");
  if (!operand_1_layout || !(((operand_1_layout.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(operand_1_layout.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64))); }))))
    return false;

  auto result_layout = derived.get("result_layout");
  if (!result_layout || !(((result_layout.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(result_layout.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64))); }))))
    return false;

  return derived.size() + num_absent_attrs == 9;
}

::mlir::IntegerAttr ConvolutionBackendConfig::algorithm() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto algorithm = derived.get("algorithm");
  assert(algorithm && "attribute not found.");
  assert(algorithm.isa<::mlir::IntegerAttr>() && "incorrect Attribute type found.");
  return algorithm.cast<::mlir::IntegerAttr>();
}

::mlir::BoolAttr ConvolutionBackendConfig::tensor_ops_enabled() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto tensor_ops_enabled = derived.get("tensor_ops_enabled");
  assert(tensor_ops_enabled && "attribute not found.");
  assert(tensor_ops_enabled.isa<::mlir::BoolAttr>() && "incorrect Attribute type found.");
  return tensor_ops_enabled.cast<::mlir::BoolAttr>();
}

::mlir::ArrayAttr ConvolutionBackendConfig::knob_ids() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto knob_ids = derived.get("knob_ids");
  assert(knob_ids && "attribute not found.");
  assert(knob_ids.isa<::mlir::ArrayAttr>() && "incorrect Attribute type found.");
  return knob_ids.cast<::mlir::ArrayAttr>();
}

::mlir::ArrayAttr ConvolutionBackendConfig::knob_values() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto knob_values = derived.get("knob_values");
  assert(knob_values && "attribute not found.");
  assert(knob_values.isa<::mlir::ArrayAttr>() && "incorrect Attribute type found.");
  return knob_values.cast<::mlir::ArrayAttr>();
}

::mlir::BoolAttr ConvolutionBackendConfig::is_cudnn_frontend() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto is_cudnn_frontend = derived.get("is_cudnn_frontend");
  assert(is_cudnn_frontend && "attribute not found.");
  assert(is_cudnn_frontend.isa<::mlir::BoolAttr>() && "incorrect Attribute type found.");
  return is_cudnn_frontend.cast<::mlir::BoolAttr>();
}

::mlir::IntegerAttr ConvolutionBackendConfig::workspace_size() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto workspace_size = derived.get("workspace_size");
  assert(workspace_size && "attribute not found.");
  assert(workspace_size.isa<::mlir::IntegerAttr>() && "incorrect Attribute type found.");
  return workspace_size.cast<::mlir::IntegerAttr>();
}

::mlir::ArrayAttr ConvolutionBackendConfig::operand_0_layout() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto operand_0_layout = derived.get("operand_0_layout");
  assert(operand_0_layout && "attribute not found.");
  assert(operand_0_layout.isa<::mlir::ArrayAttr>() && "incorrect Attribute type found.");
  return operand_0_layout.cast<::mlir::ArrayAttr>();
}

::mlir::ArrayAttr ConvolutionBackendConfig::operand_1_layout() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto operand_1_layout = derived.get("operand_1_layout");
  assert(operand_1_layout && "attribute not found.");
  assert(operand_1_layout.isa<::mlir::ArrayAttr>() && "incorrect Attribute type found.");
  return operand_1_layout.cast<::mlir::ArrayAttr>();
}

::mlir::ArrayAttr ConvolutionBackendConfig::result_layout() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto result_layout = derived.get("result_layout");
  assert(result_layout && "attribute not found.");
  assert(result_layout.isa<::mlir::ArrayAttr>() && "incorrect Attribute type found.");
  return result_layout.cast<::mlir::ArrayAttr>();
}
} // namespace lmhlo_gpu
} // namespace mlir
