/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Dialect Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace deallocation {

class DeallocationDialect : public ::mlir::Dialect {
  explicit DeallocationDialect(::mlir::MLIRContext *context);

  void initialize();
  friend class ::mlir::MLIRContext;
public:
  ~DeallocationDialect() override;
  static constexpr ::llvm::StringLiteral getDialectNamespace() {
    return ::llvm::StringLiteral("deallocation");
  }
};
} // namespace deallocation
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::deallocation::DeallocationDialect)
