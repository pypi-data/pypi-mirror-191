/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Struct Utility Definitions                                                 *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace mhlo {
ChannelHandle ChannelHandle::get(
    ::mlir::IntegerAttr handle,
    ::mlir::IntegerAttr type,
    ::mlir::MLIRContext* context) {
  ::llvm::SmallVector<::mlir::NamedAttribute, 2> fields;

  assert(handle);
  auto handle_id = ::mlir::StringAttr::get(context, "handle");
  fields.emplace_back(handle_id, handle);

  assert(type);
  auto type_id = ::mlir::StringAttr::get(context, "type");
  fields.emplace_back(type_id, type);

  ::mlir::Attribute dict = ::mlir::DictionaryAttr::get(context, fields);
  return dict.dyn_cast<ChannelHandle>();
}

bool ChannelHandle::classof(::mlir::Attribute attr) {
  if (!attr)
    return false;
  auto derived = attr.dyn_cast<::mlir::DictionaryAttr>();
  if (!derived)
    return false;
  int num_absent_attrs = 0;

  auto handle = derived.get("handle");
  if (!handle || !(((handle.isa<::mlir::IntegerAttr>())) && ((handle.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64)))))
    return false;

  auto type = derived.get("type");
  if (!type || !(((type.isa<::mlir::IntegerAttr>())) && ((type.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64)))))
    return false;

  return derived.size() + num_absent_attrs == 2;
}

::mlir::IntegerAttr ChannelHandle::handle() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto handle = derived.get("handle");
  assert(handle && "attribute not found.");
  assert(handle.isa<::mlir::IntegerAttr>() && "incorrect Attribute type found.");
  return handle.cast<::mlir::IntegerAttr>();
}

::mlir::IntegerAttr ChannelHandle::type() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto type = derived.get("type");
  assert(type && "attribute not found.");
  assert(type.isa<::mlir::IntegerAttr>() && "incorrect Attribute type found.");
  return type.cast<::mlir::IntegerAttr>();
}
} // namespace mhlo
} // namespace mlir
