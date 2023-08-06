/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

class TflArithmeticCountOpInterface;
namespace detail {
struct TflArithmeticCountOpInterfaceInterfaceTraits {
  struct Concept {
    int64_t (*GetArithmeticCount)(Operation*);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = TflArithmeticCountOpInterface;
    Model() : Concept{GetArithmeticCount} {}

    static inline int64_t GetArithmeticCount(Operation* op);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = TflArithmeticCountOpInterface;
    FallbackModel() : Concept{GetArithmeticCount} {}

    static inline int64_t GetArithmeticCount(Operation* op);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
  };
};template <typename ConcreteOp>
struct TflArithmeticCountOpInterfaceTrait;

} // namespace detail
class TflArithmeticCountOpInterface : public ::mlir::OpInterface<TflArithmeticCountOpInterface, detail::TflArithmeticCountOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<TflArithmeticCountOpInterface, detail::TflArithmeticCountOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::TflArithmeticCountOpInterfaceTrait<ConcreteOp> {};
  int64_t GetArithmeticCount(Operation* op);
};
namespace detail {
  template <typename ConcreteOp>
  struct TflArithmeticCountOpInterfaceTrait : public ::mlir::OpInterface<TflArithmeticCountOpInterface, detail::TflArithmeticCountOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
template<typename ConcreteOp>
int64_t detail::TflArithmeticCountOpInterfaceInterfaceTraits::Model<ConcreteOp>::GetArithmeticCount(Operation* op) {
  return ConcreteOp::GetArithmeticCount(op);
}
template<typename ConcreteOp>
int64_t detail::TflArithmeticCountOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::GetArithmeticCount(Operation* op) {
  return ConcreteOp::GetArithmeticCount(op);
}
class TflRuntimeVerifyOpInterface;
namespace detail {
struct TflRuntimeVerifyOpInterfaceInterfaceTraits {
  struct Concept {
    LogicalResult (*VerifyTflRuntimeConstraints)(Operation*, bool);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = TflRuntimeVerifyOpInterface;
    Model() : Concept{VerifyTflRuntimeConstraints} {}

    static inline LogicalResult VerifyTflRuntimeConstraints(Operation* op, bool emit_error_on_verify_fail);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = TflRuntimeVerifyOpInterface;
    FallbackModel() : Concept{VerifyTflRuntimeConstraints} {}

    static inline LogicalResult VerifyTflRuntimeConstraints(Operation* op, bool emit_error_on_verify_fail);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
  };
};template <typename ConcreteOp>
struct TflRuntimeVerifyOpInterfaceTrait;

} // namespace detail
class TflRuntimeVerifyOpInterface : public ::mlir::OpInterface<TflRuntimeVerifyOpInterface, detail::TflRuntimeVerifyOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<TflRuntimeVerifyOpInterface, detail::TflRuntimeVerifyOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::TflRuntimeVerifyOpInterfaceTrait<ConcreteOp> {};
  LogicalResult VerifyTflRuntimeConstraints(Operation* op, bool emit_error_on_verify_fail);
};
namespace detail {
  template <typename ConcreteOp>
  struct TflRuntimeVerifyOpInterfaceTrait : public ::mlir::OpInterface<TflRuntimeVerifyOpInterface, detail::TflRuntimeVerifyOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
template<typename ConcreteOp>
LogicalResult detail::TflRuntimeVerifyOpInterfaceInterfaceTraits::Model<ConcreteOp>::VerifyTflRuntimeConstraints(Operation* op, bool emit_error_on_verify_fail) {
  return ConcreteOp::VerifyTflRuntimeConstraints(op, emit_error_on_verify_fail);
}
template<typename ConcreteOp>
LogicalResult detail::TflRuntimeVerifyOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::VerifyTflRuntimeConstraints(Operation* op, bool emit_error_on_verify_fail) {
  return ConcreteOp::VerifyTflRuntimeConstraints(op, emit_error_on_verify_fail);
}
class SparseOpInterface;
namespace detail {
struct SparseOpInterfaceInterfaceTraits {
  struct Concept {
    std::vector<int> (*GetSparseOperands)(const Concept *impl, ::mlir::Operation *);
    std::vector<std::vector<int>> (*GetFloatBlockSize)(const Concept *impl, ::mlir::Operation *);
    std::vector<std::vector<int>> (*GetQuantizedBlockSize)(const Concept *impl, ::mlir::Operation *);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = SparseOpInterface;
    Model() : Concept{GetSparseOperands, GetFloatBlockSize, GetQuantizedBlockSize} {}

    static inline std::vector<int> GetSparseOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline std::vector<std::vector<int>> GetFloatBlockSize(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline std::vector<std::vector<int>> GetQuantizedBlockSize(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = SparseOpInterface;
    FallbackModel() : Concept{GetSparseOperands, GetFloatBlockSize, GetQuantizedBlockSize} {}

    static inline std::vector<int> GetSparseOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline std::vector<std::vector<int>> GetFloatBlockSize(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline std::vector<std::vector<int>> GetQuantizedBlockSize(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
  };
};template <typename ConcreteOp>
struct SparseOpInterfaceTrait;

} // namespace detail
class SparseOpInterface : public ::mlir::OpInterface<SparseOpInterface, detail::SparseOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<SparseOpInterface, detail::SparseOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::SparseOpInterfaceTrait<ConcreteOp> {};
  std::vector<int> GetSparseOperands();
  std::vector<std::vector<int>> GetFloatBlockSize();
  std::vector<std::vector<int>> GetQuantizedBlockSize();
};
namespace detail {
  template <typename ConcreteOp>
  struct SparseOpInterfaceTrait : public ::mlir::OpInterface<SparseOpInterface, detail::SparseOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
template<typename ConcreteOp>
std::vector<int> detail::SparseOpInterfaceInterfaceTraits::Model<ConcreteOp>::GetSparseOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).GetSparseOperands();
}
template<typename ConcreteOp>
std::vector<std::vector<int>> detail::SparseOpInterfaceInterfaceTraits::Model<ConcreteOp>::GetFloatBlockSize(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).GetFloatBlockSize();
}
template<typename ConcreteOp>
std::vector<std::vector<int>> detail::SparseOpInterfaceInterfaceTraits::Model<ConcreteOp>::GetQuantizedBlockSize(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).GetQuantizedBlockSize();
}
template<typename ConcreteOp>
std::vector<int> detail::SparseOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::GetSparseOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->GetSparseOperands(tablegen_opaque_val);
}
template<typename ConcreteOp>
std::vector<std::vector<int>> detail::SparseOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::GetFloatBlockSize(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->GetFloatBlockSize(tablegen_opaque_val);
}
template<typename ConcreteOp>
std::vector<std::vector<int>> detail::SparseOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::GetQuantizedBlockSize(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->GetQuantizedBlockSize(tablegen_opaque_val);
}
class StatefulOpInterface;
namespace detail {
struct StatefulOpInterfaceInterfaceTraits {
  struct Concept {
    std::vector<int> (*GetStatefulOperands)(const Concept *impl, ::mlir::Operation *);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = StatefulOpInterface;
    Model() : Concept{GetStatefulOperands} {}

    static inline std::vector<int> GetStatefulOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = StatefulOpInterface;
    FallbackModel() : Concept{GetStatefulOperands} {}

    static inline std::vector<int> GetStatefulOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
  };
};template <typename ConcreteOp>
struct StatefulOpInterfaceTrait;

} // namespace detail
class StatefulOpInterface : public ::mlir::OpInterface<StatefulOpInterface, detail::StatefulOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<StatefulOpInterface, detail::StatefulOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::StatefulOpInterfaceTrait<ConcreteOp> {};
  std::vector<int> GetStatefulOperands();
};
namespace detail {
  template <typename ConcreteOp>
  struct StatefulOpInterfaceTrait : public ::mlir::OpInterface<StatefulOpInterface, detail::StatefulOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
template<typename ConcreteOp>
std::vector<int> detail::StatefulOpInterfaceInterfaceTraits::Model<ConcreteOp>::GetStatefulOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).GetStatefulOperands();
}
template<typename ConcreteOp>
std::vector<int> detail::StatefulOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::GetStatefulOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->GetStatefulOperands(tablegen_opaque_val);
}
