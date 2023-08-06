/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Definitions                                                             *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_OP_LIST
#undef GET_OP_LIST

::mlir::TF::_TfrtGetResourceOp,
::mlir::TF::_TfrtSetResourceOp
#endif  // GET_OP_LIST

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace TF {

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_tfrt_ops0(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!(((type.isa<::mlir::TensorType>())) && ([](::mlir::Type elementType) { return ((((elementType.isF16())) || ((elementType.isa<mlir::TF::HalfRefType>()))) || (((elementType.isF32())) || ((elementType.isa<mlir::TF::FloatRefType>()))) || (((elementType.isF64())) || ((elementType.isa<mlir::TF::DoubleRefType>()))) || (((elementType.isBF16())) || ((elementType.isa<mlir::TF::Bfloat16RefType>())))) || (((((elementType.isa<::mlir::ComplexType>())) && ((elementType.cast<::mlir::ComplexType>().getElementType().isF32()))) || ((elementType.isa<mlir::TF::Complex64RefType>()))) || ((((elementType.isa<::mlir::ComplexType>())) && ((elementType.cast<::mlir::ComplexType>().getElementType().isF64()))) || ((elementType.isa<mlir::TF::Complex128RefType>())))) || (((((elementType.isSignlessInteger(8))) || ((elementType.isa<mlir::TF::Int8RefType>()))) || (((elementType.isSignlessInteger(16))) || ((elementType.isa<mlir::TF::Int16RefType>()))) || (((elementType.isSignlessInteger(32))) || ((elementType.isa<mlir::TF::Int32RefType>()))) || (((elementType.isSignlessInteger(64))) || ((elementType.isa<mlir::TF::Int64RefType>())))) || ((((elementType.isUnsignedInteger(8))) || ((elementType.isa<mlir::TF::Uint8RefType>()))) || (((elementType.isUnsignedInteger(16))) || ((elementType.isa<mlir::TF::Uint16RefType>()))) || (((elementType.isUnsignedInteger(32))) || ((elementType.isa<mlir::TF::Uint32RefType>()))) || (((elementType.isUnsignedInteger(64))) || ((elementType.isa<mlir::TF::Uint64RefType>()))))) || (((elementType.isSignlessInteger(1))) || ((elementType.isa<mlir::TF::BoolRefType>()))) || ((elementType.isa<mlir::TF::TensorFlowType>())); }(type.cast<::mlir::ShapedType>().getElementType())))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be tensor of tf.dtype values, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_tfrt_ops0(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !(((attr.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(attr.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64))); })))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: 64-bit integer array attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_tfrt_ops1(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !(((attr.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(attr.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return (attr.isa<::mlir::StringAttr>()); })))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: string array attribute";
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_tfrt_ops2(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !(((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64))))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: 64-bit signless integer attribute";
  }
  return ::mlir::success();
}
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_TfrtGetResourceOp definitions
//===----------------------------------------------------------------------===//

_TfrtGetResourceOpAdaptor::_TfrtGetResourceOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

_TfrtGetResourceOpAdaptor::_TfrtGetResourceOpAdaptor(_TfrtGetResourceOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange _TfrtGetResourceOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> _TfrtGetResourceOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange _TfrtGetResourceOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::DictionaryAttr _TfrtGetResourceOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::ArrayAttr _TfrtGetResourceOpAdaptor::indices() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::ArrayAttr attr = odsAttrs.get("indices").cast<::mlir::ArrayAttr>();
  return attr;
}

::mlir::ArrayAttr _TfrtGetResourceOpAdaptor::shared_name() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::ArrayAttr attr = odsAttrs.get("shared_name").cast<::mlir::ArrayAttr>();
  return attr;
}

::mlir::ArrayAttr _TfrtGetResourceOpAdaptor::container() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::ArrayAttr attr = odsAttrs.get("container").cast<::mlir::ArrayAttr>();
  return attr;
}

::mlir::LogicalResult _TfrtGetResourceOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_indices = odsAttrs.get("indices");
    if (!tblgen_indices)
      return emitError(loc, "'tf._TfrtGetResource' op ""requires attribute 'indices'");

    if (tblgen_indices && !(((tblgen_indices.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(tblgen_indices.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return ((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64))); }))))
      return emitError(loc, "'tf._TfrtGetResource' op ""attribute 'indices' failed to satisfy constraint: 64-bit integer array attribute");
  }
  {
    auto tblgen_shared_name = odsAttrs.get("shared_name");
    if (!tblgen_shared_name)
      return emitError(loc, "'tf._TfrtGetResource' op ""requires attribute 'shared_name'");

    if (tblgen_shared_name && !(((tblgen_shared_name.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(tblgen_shared_name.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return (attr.isa<::mlir::StringAttr>()); }))))
      return emitError(loc, "'tf._TfrtGetResource' op ""attribute 'shared_name' failed to satisfy constraint: string array attribute");
  }
  {
    auto tblgen_container = odsAttrs.get("container");
    if (!tblgen_container)
      return emitError(loc, "'tf._TfrtGetResource' op ""requires attribute 'container'");

    if (tblgen_container && !(((tblgen_container.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(tblgen_container.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return (attr.isa<::mlir::StringAttr>()); }))))
      return emitError(loc, "'tf._TfrtGetResource' op ""attribute 'container' failed to satisfy constraint: string array attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> _TfrtGetResourceOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range _TfrtGetResourceOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> _TfrtGetResourceOp::getODSResultIndexAndLength(unsigned index) {
  bool isVariadic[] = {true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumResults() - 0) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::result_range _TfrtGetResourceOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Operation::result_range _TfrtGetResourceOp::results() {
  return getODSResults(0);
}

::mlir::ArrayAttr _TfrtGetResourceOp::indicesAttr() {
  return (*this)->getAttr(indicesAttrName()).cast<::mlir::ArrayAttr>();
}

::mlir::ArrayAttr _TfrtGetResourceOp::indices() {
  auto attr = indicesAttr();
  return attr;
}

::mlir::ArrayAttr _TfrtGetResourceOp::shared_nameAttr() {
  return (*this)->getAttr(shared_nameAttrName()).cast<::mlir::ArrayAttr>();
}

::mlir::ArrayAttr _TfrtGetResourceOp::shared_name() {
  auto attr = shared_nameAttr();
  return attr;
}

::mlir::ArrayAttr _TfrtGetResourceOp::containerAttr() {
  return (*this)->getAttr(containerAttrName()).cast<::mlir::ArrayAttr>();
}

::mlir::ArrayAttr _TfrtGetResourceOp::container() {
  auto attr = containerAttr();
  return attr;
}

void _TfrtGetResourceOp::indicesAttr(::mlir::ArrayAttr attr) {
  (*this)->setAttr(indicesAttrName(), attr);
}

void _TfrtGetResourceOp::shared_nameAttr(::mlir::ArrayAttr attr) {
  (*this)->setAttr(shared_nameAttrName(), attr);
}

void _TfrtGetResourceOp::containerAttr(::mlir::ArrayAttr attr) {
  (*this)->setAttr(containerAttrName(), attr);
}

void _TfrtGetResourceOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange results, ::mlir::ArrayAttr indices, ::mlir::ArrayAttr shared_name, ::mlir::ArrayAttr container) {
  odsState.addAttribute(indicesAttrName(odsState.name), indices);
  odsState.addAttribute(shared_nameAttrName(odsState.name), shared_name);
  odsState.addAttribute(containerAttrName(odsState.name), container);
  odsState.addTypes(results);
}

void _TfrtGetResourceOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 0u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult _TfrtGetResourceOp::verify() {
  {
    auto tblgen_indices = (*this)->getAttr(indicesAttrName());
    if (!tblgen_indices)
      return emitOpError("requires attribute 'indices'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tfrt_ops0(*this, tblgen_indices, "indices")))
      return ::mlir::failure();
  }
  {
    auto tblgen_shared_name = (*this)->getAttr(shared_nameAttrName());
    if (!tblgen_shared_name)
      return emitOpError("requires attribute 'shared_name'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tfrt_ops1(*this, tblgen_shared_name, "shared_name")))
      return ::mlir::failure();
  }
  {
    auto tblgen_container = (*this)->getAttr(containerAttrName());
    if (!tblgen_container)
      return emitOpError("requires attribute 'container'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tfrt_ops1(*this, tblgen_container, "container")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tfrt_ops0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return Verify(*this);
}

void _TfrtGetResourceOp::getEffects(::mlir::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
}

} // namespace TF
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::TF::_TfrtGetResourceOp)

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_TfrtSetResourceOp definitions
//===----------------------------------------------------------------------===//

_TfrtSetResourceOpAdaptor::_TfrtSetResourceOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {}

_TfrtSetResourceOpAdaptor::_TfrtSetResourceOpAdaptor(_TfrtSetResourceOp &op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()) {}

::mlir::ValueRange _TfrtSetResourceOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> _TfrtSetResourceOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange _TfrtSetResourceOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value _TfrtSetResourceOpAdaptor::arg() {
  return *getODSOperands(0).begin();
}

::mlir::DictionaryAttr _TfrtSetResourceOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::IntegerAttr _TfrtSetResourceOpAdaptor::index() {
  assert(odsAttrs && "no attributes when constructing adapter");
  ::mlir::IntegerAttr attr = odsAttrs.get("index").cast<::mlir::IntegerAttr>();
  return attr;
}

::mlir::LogicalResult _TfrtSetResourceOpAdaptor::verify(::mlir::Location loc) {
  {
    auto tblgen_index = odsAttrs.get("index");
    if (!tblgen_index)
      return emitError(loc, "'tf._TfrtSetResource' op ""requires attribute 'index'");

    if (tblgen_index && !(((tblgen_index.isa<::mlir::IntegerAttr>())) && ((tblgen_index.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64)))))
      return emitError(loc, "'tf._TfrtSetResource' op ""attribute 'index' failed to satisfy constraint: 64-bit signless integer attribute");
  }
  return ::mlir::success();
}

std::pair<unsigned, unsigned> _TfrtSetResourceOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range _TfrtSetResourceOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value _TfrtSetResourceOp::arg() {
  return *getODSOperands(0).begin();
}

::mlir::MutableOperandRange _TfrtSetResourceOp::argMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> _TfrtSetResourceOp::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range _TfrtSetResourceOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::IntegerAttr _TfrtSetResourceOp::indexAttr() {
  return (*this)->getAttr(indexAttrName()).cast<::mlir::IntegerAttr>();
}

uint64_t _TfrtSetResourceOp::index() {
  auto attr = indexAttr();
  return attr.getValue().getZExtValue();
}

void _TfrtSetResourceOp::indexAttr(::mlir::IntegerAttr attr) {
  (*this)->setAttr(indexAttrName(), attr);
}

void _TfrtSetResourceOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value arg, ::mlir::IntegerAttr index) {
  odsState.addOperands(arg);
  odsState.addAttribute(indexAttrName(odsState.name), index);
}

void _TfrtSetResourceOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value arg, ::mlir::IntegerAttr index) {
  odsState.addOperands(arg);
  odsState.addAttribute(indexAttrName(odsState.name), index);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void _TfrtSetResourceOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value arg, uint64_t index) {
  odsState.addOperands(arg);
  odsState.addAttribute(indexAttrName(odsState.name), odsBuilder.getIntegerAttr(odsBuilder.getIntegerType(64), index));
}

void _TfrtSetResourceOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value arg, uint64_t index) {
  odsState.addOperands(arg);
  odsState.addAttribute(indexAttrName(odsState.name), odsBuilder.getIntegerAttr(odsBuilder.getIntegerType(64), index));
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void _TfrtSetResourceOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult _TfrtSetResourceOp::verify() {
  {
    auto tblgen_index = (*this)->getAttr(indexAttrName());
    if (!tblgen_index)
      return emitOpError("requires attribute 'index'");

    if (::mlir::failed(__mlir_ods_local_attr_constraint_tfrt_ops2(*this, tblgen_index, "index")))
      return ::mlir::failure();
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_tfrt_ops0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

} // namespace TF
} // namespace mlir
DEFINE_EXPLICIT_TYPE_ID(::mlir::TF::_TfrtSetResourceOp)


#endif  // GET_OP_CLASSES

