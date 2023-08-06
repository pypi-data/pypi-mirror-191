/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Struct Utility Definitions                                                 *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace TFL {
DimensionMetadataAttr DimensionMetadataAttr::get(
    ::mlir::StringAttr format,
    ::mlir::IntegerAttr dense_size,
    ::mlir::ArrayAttr segments,
    ::mlir::ArrayAttr indices,
    ::mlir::MLIRContext* context) {
  ::llvm::SmallVector<::mlir::NamedAttribute, 4> fields;

  assert(format);
  auto format_id = ::mlir::StringAttr::get(context, "format");
  fields.emplace_back(format_id, format);

  assert(dense_size);
  auto dense_size_id = ::mlir::StringAttr::get(context, "dense_size");
  fields.emplace_back(dense_size_id, dense_size);

  assert(segments);
  auto segments_id = ::mlir::StringAttr::get(context, "segments");
  fields.emplace_back(segments_id, segments);

  assert(indices);
  auto indices_id = ::mlir::StringAttr::get(context, "indices");
  fields.emplace_back(indices_id, indices);

  ::mlir::Attribute dict = ::mlir::DictionaryAttr::get(context, fields);
  return dict.dyn_cast<DimensionMetadataAttr>();
}

bool DimensionMetadataAttr::classof(::mlir::Attribute attr) {
  if (!attr)
    return false;
  auto derived = attr.dyn_cast<::mlir::DictionaryAttr>();
  if (!derived)
    return false;
  int num_absent_attrs = 0;

  auto format = derived.get("format");
  if (!format || !(((format.isa<::mlir::StringAttr>())) && (((format.cast<::mlir::StringAttr>().getValue() == "DENSE")) || ((format.cast<::mlir::StringAttr>().getValue() == "SPARSE_CSR")))))
    return false;

  auto dense_size = derived.get("dense_size");
  if (!dense_size || !(((dense_size.isa<::mlir::IntegerAttr>())) && ((dense_size.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32)))))
    return false;

  auto segments = derived.get("segments");
  if (!segments || !(((segments.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(segments.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32))); }))))
    return false;

  auto indices = derived.get("indices");
  if (!indices || !(((indices.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(indices.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32))); }))))
    return false;

  return derived.size() + num_absent_attrs == 4;
}

::mlir::StringAttr DimensionMetadataAttr::format() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto format = derived.get("format");
  assert(format && "attribute not found.");
  assert(format.isa<::mlir::StringAttr>() && "incorrect Attribute type found.");
  return format.cast<::mlir::StringAttr>();
}

::mlir::IntegerAttr DimensionMetadataAttr::dense_size() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto dense_size = derived.get("dense_size");
  assert(dense_size && "attribute not found.");
  assert(dense_size.isa<::mlir::IntegerAttr>() && "incorrect Attribute type found.");
  return dense_size.cast<::mlir::IntegerAttr>();
}

::mlir::ArrayAttr DimensionMetadataAttr::segments() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto segments = derived.get("segments");
  assert(segments && "attribute not found.");
  assert(segments.isa<::mlir::ArrayAttr>() && "incorrect Attribute type found.");
  return segments.cast<::mlir::ArrayAttr>();
}

::mlir::ArrayAttr DimensionMetadataAttr::indices() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto indices = derived.get("indices");
  assert(indices && "attribute not found.");
  assert(indices.isa<::mlir::ArrayAttr>() && "incorrect Attribute type found.");
  return indices.cast<::mlir::ArrayAttr>();
}
} // namespace TFL
} // namespace mlir
namespace mlir {
namespace TFL {
SparsityParameterAttr SparsityParameterAttr::get(
    ::mlir::ArrayAttr traversal_order,
    ::mlir::ArrayAttr block_map,
    ::mlir::ArrayAttr dim_metadata,
    ::mlir::MLIRContext* context) {
  ::llvm::SmallVector<::mlir::NamedAttribute, 3> fields;

  assert(traversal_order);
  auto traversal_order_id = ::mlir::StringAttr::get(context, "traversal_order");
  fields.emplace_back(traversal_order_id, traversal_order);

  assert(block_map);
  auto block_map_id = ::mlir::StringAttr::get(context, "block_map");
  fields.emplace_back(block_map_id, block_map);

  assert(dim_metadata);
  auto dim_metadata_id = ::mlir::StringAttr::get(context, "dim_metadata");
  fields.emplace_back(dim_metadata_id, dim_metadata);

  ::mlir::Attribute dict = ::mlir::DictionaryAttr::get(context, fields);
  return dict.dyn_cast<SparsityParameterAttr>();
}

bool SparsityParameterAttr::classof(::mlir::Attribute attr) {
  if (!attr)
    return false;
  auto derived = attr.dyn_cast<::mlir::DictionaryAttr>();
  if (!derived)
    return false;
  int num_absent_attrs = 0;

  auto traversal_order = derived.get("traversal_order");
  if (!traversal_order || !(((traversal_order.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(traversal_order.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32))); }))))
    return false;

  auto block_map = derived.get("block_map");
  if (!block_map || !(((block_map.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(block_map.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32))); }))))
    return false;

  auto dim_metadata = derived.get("dim_metadata");
  if (!dim_metadata || !(((dim_metadata.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(dim_metadata.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return (attr.isa<::mlir::TFL::DimensionMetadataAttr>()); }))))
    return false;

  return derived.size() + num_absent_attrs == 3;
}

::mlir::ArrayAttr SparsityParameterAttr::traversal_order() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto traversal_order = derived.get("traversal_order");
  assert(traversal_order && "attribute not found.");
  assert(traversal_order.isa<::mlir::ArrayAttr>() && "incorrect Attribute type found.");
  return traversal_order.cast<::mlir::ArrayAttr>();
}

::mlir::ArrayAttr SparsityParameterAttr::block_map() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto block_map = derived.get("block_map");
  assert(block_map && "attribute not found.");
  assert(block_map.isa<::mlir::ArrayAttr>() && "incorrect Attribute type found.");
  return block_map.cast<::mlir::ArrayAttr>();
}

::mlir::ArrayAttr SparsityParameterAttr::dim_metadata() const {
  auto derived = this->cast<::mlir::DictionaryAttr>();
  auto dim_metadata = derived.get("dim_metadata");
  assert(dim_metadata && "attribute not found.");
  assert(dim_metadata.isa<::mlir::ArrayAttr>() && "incorrect Attribute type found.");
  return dim_metadata.cast<::mlir::ArrayAttr>();
}
} // namespace TFL
} // namespace mlir
