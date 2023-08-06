/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* AttrDef Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_ATTRDEF_CLASSES
#undef GET_ATTRDEF_CLASSES


namespace mlir {
class AsmParser;
class AsmPrinter;
} // namespace mlir
namespace mlir {
namespace tf_type {
class FuncAttr;
class PlaceholderAttr;
class ShapeAttr;
class VersionAttr;
namespace detail {
struct FuncAttrStorage;
} // namespace detail
class FuncAttr : public ::mlir::Attribute::AttrBase<FuncAttr, ::mlir::Attribute, detail::FuncAttrStorage> {
public:
  using Base::Base;
public:
  static FuncAttr get(::mlir::MLIRContext *context, SymbolRefAttr name, DictionaryAttr attrs);
  static FuncAttr get(::mlir::MLIRContext *context, StringRef name, DictionaryAttr attr);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"func"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &parser, ::mlir::Type type);
  void print(::mlir::AsmPrinter &printer) const;
  SymbolRefAttr getName() const;
  DictionaryAttr getAttrs() const;
};
namespace detail {
struct PlaceholderAttrStorage;
} // namespace detail
class PlaceholderAttr : public ::mlir::Attribute::AttrBase<PlaceholderAttr, ::mlir::Attribute, detail::PlaceholderAttrStorage> {
public:
  using Base::Base;
public:
  static PlaceholderAttr get(::mlir::MLIRContext *context, ::llvm::StringRef value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"placeholder"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &parser, ::mlir::Type type);
  void print(::mlir::AsmPrinter &printer) const;
  ::llvm::StringRef getValue() const;
};
namespace detail {
struct ShapeAttrStorage;
} // namespace detail
class ShapeAttr : public ::mlir::Attribute::AttrBase<ShapeAttr, ::mlir::Attribute, detail::ShapeAttrStorage> {
public:
  using Base::Base;
  // Returns true if this shape is ranked and has only known dimensions size.
  bool hasStaticShape() const;

  // Returns true if this shape attribute has a statically known rank.
  bool hasRank() const;

  // Returns the rank. Aborts if unranked.
  int64_t getRank() const;

  // Returns the shape array if ranked, or None if unranked.
  llvm::Optional<ArrayRef<int64_t>> getValue() const;
public:
  static ShapeAttr get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> shape, bool unranked);
  static ShapeAttr get(::mlir::MLIRContext *context, llvm::Optional<ArrayRef<int64_t>> dimensions);
  static ShapeAttr get(::mlir::MLIRContext *context, ShapedType shaped_type);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"shape"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &parser, ::mlir::Type type);
  void print(::mlir::AsmPrinter &printer) const;
  ::llvm::ArrayRef<int64_t> getShape() const;
  bool getUnranked() const;
};
namespace detail {
struct VersionAttrStorage;
} // namespace detail
class VersionAttr : public ::mlir::Attribute::AttrBase<VersionAttr, ::mlir::Attribute, detail::VersionAttrStorage> {
public:
  using Base::Base;
public:
  static VersionAttr get(::mlir::MLIRContext *context, int32_t producer, int32_t minConsumer, ::llvm::ArrayRef<int32_t> badConsumers);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"version"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &parser, ::mlir::Type type);
  void print(::mlir::AsmPrinter &printer) const;
  int32_t getProducer() const;
  int32_t getMinConsumer() const;
  ::llvm::ArrayRef<int32_t> getBadConsumers() const;
};
} // namespace tf_type
} // namespace mlir
DECLARE_EXPLICIT_TYPE_ID(::mlir::tf_type::FuncAttr)
DECLARE_EXPLICIT_TYPE_ID(::mlir::tf_type::PlaceholderAttr)
DECLARE_EXPLICIT_TYPE_ID(::mlir::tf_type::ShapeAttr)
DECLARE_EXPLICIT_TYPE_ID(::mlir::tf_type::VersionAttr)

#endif  // GET_ATTRDEF_CLASSES

