/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Dialect Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace tfg {

class TFGraphDialect : public ::mlir::Dialect {
  explicit TFGraphDialect(::mlir::MLIRContext *context)
    : ::mlir::Dialect(getDialectNamespace(), context,
      ::mlir::TypeID::get<TFGraphDialect>()) {
    
    initialize();
  }

  void initialize();
  friend class ::mlir::MLIRContext;
public:
  ~TFGraphDialect() override;
  static constexpr ::llvm::StringLiteral getDialectNamespace() {
    return ::llvm::StringLiteral("tfg");
  }

    Identifier getNameAttrIdentifier() const { return name_key_; }
    static constexpr StringRef getNameAttrKey() { return "_mlir_name"; }

    Identifier getDeviceAttrIdentifier() const { return device_key_; }
    static constexpr StringRef getDeviceAttrKey() { return "_mlir_device"; }

    Identifier getAssignedDeviceAttrIdentifier() const {
      return assigned_device_key_;
    }
    static constexpr StringRef getAssignedDeviceAttrKey() {
      return "_mlir_assigned_device";
    }

    // Cached accessor for the control type.
    ControlType getControlType() const { return control_ty_; }

    // Print an operation that belongs to this dialect if unregistered.
    void printCustomTfOp(Operation *op, OpAsmPrinter &printer) const;

    // Returns the hook to parse an operation belonging to this dialect, even
    // if unregistered.
    Optional<ParseOpHook> getParseOperationHook(StringRef opName) const
      override;

    // Returns the took to print an operation belonging to this dialect, even
    // if unregistered.
    llvm::unique_function<void(Operation *, OpAsmPrinter &)>
    getOperationPrinter(Operation *op) const override;

  private:
    // Cached identifier for efficiency purpose.
    Identifier name_key_;
    Identifier device_key_;
    Identifier assigned_device_key_;
    ControlType control_ty_;
  };
} // namespace tfg
} // namespace mlir
DECLARE_EXPLICIT_TYPE_ID(::mlir::tfg::TFGraphDialect)
