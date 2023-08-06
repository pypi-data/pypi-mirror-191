/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Enum Utility Definitions                                                   *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace lmhlo_gpu {
::llvm::StringRef stringifyActivation(Activation val) {
  switch (val) {
    case Activation::None: return "None";
    case Activation::Sigmoid: return "Sigmoid";
    case Activation::Tanh: return "Tanh";
    case Activation::Relu: return "Relu";
    case Activation::Relu6: return "Relu6";
    case Activation::ReluX: return "ReluX";
    case Activation::BandPass: return "BandPass";
  }
  return "";
}

::llvm::Optional<Activation> symbolizeActivation(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<Activation>>(str)
      .Case("None", Activation::None)
      .Case("Sigmoid", Activation::Sigmoid)
      .Case("Tanh", Activation::Tanh)
      .Case("Relu", Activation::Relu)
      .Case("Relu6", Activation::Relu6)
      .Case("ReluX", Activation::ReluX)
      .Case("BandPass", Activation::BandPass)
      .Default(::llvm::None);
}
} // namespace lmhlo_gpu
} // namespace mlir

