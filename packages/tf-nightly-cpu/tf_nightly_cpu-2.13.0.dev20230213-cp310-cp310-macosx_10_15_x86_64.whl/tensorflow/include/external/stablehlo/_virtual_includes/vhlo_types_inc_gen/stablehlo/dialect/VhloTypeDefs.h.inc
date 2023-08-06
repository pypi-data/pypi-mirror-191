/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* TypeDef Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_TYPEDEF_CLASSES
#undef GET_TYPEDEF_CLASSES


namespace mlir {
class AsmParser;
class AsmPrinter;
} // namespace mlir
namespace mlir {
namespace vhlo {
class BFloat16V1Type;
class ComplexV1Type;
class Float16V1Type;
class Float32V1Type;
class Float64V1Type;
class Float8E4M3FNV1Type;
class Float8E5M2V1Type;
class FunctionV1Type;
class IndexV1Type;
class IntegerI16V1Type;
class IntegerI1V1Type;
class IntegerI32V1Type;
class IntegerI4V1Type;
class IntegerI64V1Type;
class IntegerI8V1Type;
class IntegerUI16V1Type;
class IntegerUI32V1Type;
class IntegerUI4V1Type;
class IntegerUI64V1Type;
class IntegerUI8V1Type;
class RankedTensorV1Type;
class TokenV1Type;
class TupleV1Type;
class UniformQuantizedV1Type;
class UnrankedTensorV1Type;
class WitnessV1Type;
class BFloat16V1Type : public ::mlir::Type::TypeBase<BFloat16V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in bf16");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in bf16");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"bf16"};
  }

};
namespace detail {
struct ComplexV1TypeStorage;
} // namespace detail
class ComplexV1Type : public ::mlir::Type::TypeBase<ComplexV1Type, ::mlir::Type, detail::ComplexV1TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in complex");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in complex");
    return *version;
  }
  using Base::getChecked;
  static ComplexV1Type get(::mlir::MLIRContext *context, Type elementType);
  static ComplexV1Type getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, Type elementType);
  static ::mlir::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, Type elementType);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"complex"};
  }

  static ::mlir::Type parse(::mlir::AsmParser &odsParser);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  Type getElementType() const;
};
class Float16V1Type : public ::mlir::Type::TypeBase<Float16V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in f16");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in f16");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"f16"};
  }

};
class Float32V1Type : public ::mlir::Type::TypeBase<Float32V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in f32");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in f32");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"f32"};
  }

};
class Float64V1Type : public ::mlir::Type::TypeBase<Float64V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in f64");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in f64");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"f64"};
  }

};
class Float8E4M3FNV1Type : public ::mlir::Type::TypeBase<Float8E4M3FNV1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.4.0");
    if (failed(version)) llvm_unreachable("invalid version 0.4.0 in f8E4M3FN");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in f8E4M3FN");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"f8E4M3FN"};
  }

};
class Float8E5M2V1Type : public ::mlir::Type::TypeBase<Float8E5M2V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.4.0");
    if (failed(version)) llvm_unreachable("invalid version 0.4.0 in f8E5M2");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in f8E5M2");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"f8E5M2"};
  }

};
namespace detail {
struct FunctionV1TypeStorage;
} // namespace detail
class FunctionV1Type : public ::mlir::Type::TypeBase<FunctionV1Type, ::mlir::Type, detail::FunctionV1TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in func");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in func");
    return *version;
  }
  using Base::getChecked;
  static FunctionV1Type get(::mlir::MLIRContext *context, ::llvm::ArrayRef<::mlir::Type> inputs, ::llvm::ArrayRef<mlir::Type> results);
  static FunctionV1Type getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::llvm::ArrayRef<::mlir::Type> inputs, ::llvm::ArrayRef<mlir::Type> results);
  static ::mlir::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::llvm::ArrayRef<::mlir::Type> inputs, ::llvm::ArrayRef<mlir::Type> results);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"func"};
  }

  static ::mlir::Type parse(::mlir::AsmParser &odsParser);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::llvm::ArrayRef<::mlir::Type> getInputs() const;
  ::llvm::ArrayRef<mlir::Type> getResults() const;
};
class IndexV1Type : public ::mlir::Type::TypeBase<IndexV1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in index");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in index");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"index"};
  }

};
class IntegerI16V1Type : public ::mlir::Type::TypeBase<IntegerI16V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in i16");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in i16");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"i16"};
  }

};
class IntegerI1V1Type : public ::mlir::Type::TypeBase<IntegerI1V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in i1");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in i1");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"i1"};
  }

};
class IntegerI32V1Type : public ::mlir::Type::TypeBase<IntegerI32V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in i32");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in i32");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"i32"};
  }

};
class IntegerI4V1Type : public ::mlir::Type::TypeBase<IntegerI4V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in i4");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in i4");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"i4"};
  }

};
class IntegerI64V1Type : public ::mlir::Type::TypeBase<IntegerI64V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in i64");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in i64");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"i64"};
  }

};
class IntegerI8V1Type : public ::mlir::Type::TypeBase<IntegerI8V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in i8");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in i8");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"i8"};
  }

};
class IntegerUI16V1Type : public ::mlir::Type::TypeBase<IntegerUI16V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in ui16");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in ui16");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"ui16"};
  }

};
class IntegerUI32V1Type : public ::mlir::Type::TypeBase<IntegerUI32V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in ui32");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in ui32");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"ui32"};
  }

};
class IntegerUI4V1Type : public ::mlir::Type::TypeBase<IntegerUI4V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in ui4");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in ui4");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"ui4"};
  }

};
class IntegerUI64V1Type : public ::mlir::Type::TypeBase<IntegerUI64V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in ui64");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in ui64");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"ui64"};
  }

};
class IntegerUI8V1Type : public ::mlir::Type::TypeBase<IntegerUI8V1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in ui8");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in ui8");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"ui8"};
  }

};
namespace detail {
struct RankedTensorV1TypeStorage;
} // namespace detail
class RankedTensorV1Type : public ::mlir::Type::TypeBase<RankedTensorV1Type, ::mlir::Type, detail::RankedTensorV1TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in tensor");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in tensor");
    return *version;
  }
  using Base::getChecked;
  static RankedTensorV1Type get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> shape, ::mlir::Type elementType, ::mlir::Attribute encoding);
  static RankedTensorV1Type getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> shape, ::mlir::Type elementType, ::mlir::Attribute encoding);
  static ::mlir::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::llvm::ArrayRef<int64_t> shape, ::mlir::Type elementType, ::mlir::Attribute encoding);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"tensor"};
  }

  static ::mlir::Type parse(::mlir::AsmParser &odsParser);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::llvm::ArrayRef<int64_t> getShape() const;
  ::mlir::Type getElementType() const;
  ::mlir::Attribute getEncoding() const;
};
class TokenV1Type : public ::mlir::Type::TypeBase<TokenV1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in token");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in token");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"token"};
  }

};
namespace detail {
struct TupleV1TypeStorage;
} // namespace detail
class TupleV1Type : public ::mlir::Type::TypeBase<TupleV1Type, ::mlir::Type, detail::TupleV1TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in tuple");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in tuple");
    return *version;
  }
  using Base::getChecked;
  static TupleV1Type get(::mlir::MLIRContext *context, ::llvm::ArrayRef<::mlir::Type> types);
  static TupleV1Type getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::llvm::ArrayRef<::mlir::Type> types);
  static ::mlir::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::llvm::ArrayRef<::mlir::Type> types);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"tuple"};
  }

  static ::mlir::Type parse(::mlir::AsmParser &odsParser);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::llvm::ArrayRef<::mlir::Type> getTypes() const;
};
namespace detail {
struct UniformQuantizedV1TypeStorage;
} // namespace detail
class UniformQuantizedV1Type : public ::mlir::Type::TypeBase<UniformQuantizedV1Type, ::mlir::Type, detail::UniformQuantizedV1TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in quant");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in quant");
    return *version;
  }
  using Base::getChecked;
  static UniformQuantizedV1Type get(::mlir::MLIRContext *context, unsigned flags, ::mlir::Type storageType, ::mlir::Type expressedType, ::llvm::APFloat scale, int64_t zeroPoint, int64_t storageTypeMin, int64_t storageTypeMax);
  static UniformQuantizedV1Type getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, unsigned flags, ::mlir::Type storageType, ::mlir::Type expressedType, ::llvm::APFloat scale, int64_t zeroPoint, int64_t storageTypeMin, int64_t storageTypeMax);
  static ::mlir::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, unsigned flags, ::mlir::Type storageType, ::mlir::Type expressedType, ::llvm::APFloat scale, int64_t zeroPoint, int64_t storageTypeMin, int64_t storageTypeMax);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"quant"};
  }

  static ::mlir::Type parse(::mlir::AsmParser &odsParser);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  unsigned getFlags() const;
  ::mlir::Type getStorageType() const;
  ::mlir::Type getExpressedType() const;
  ::llvm::APFloat getScale() const;
  int64_t getZeroPoint() const;
  int64_t getStorageTypeMin() const;
  int64_t getStorageTypeMax() const;
};
namespace detail {
struct UnrankedTensorV1TypeStorage;
} // namespace detail
class UnrankedTensorV1Type : public ::mlir::Type::TypeBase<UnrankedTensorV1Type, ::mlir::Type, detail::UnrankedTensorV1TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in unranked_tensor");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in unranked_tensor");
    return *version;
  }
  using Base::getChecked;
  static UnrankedTensorV1Type get(::mlir::MLIRContext *context, ::mlir::Type elementType);
  static UnrankedTensorV1Type getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::mlir::Type elementType);
  static ::mlir::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::Type elementType);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"unranked_tensor"};
  }

  static ::mlir::Type parse(::mlir::AsmParser &odsParser);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::Type getElementType() const;
};
class WitnessV1Type : public ::mlir::Type::TypeBase<WitnessV1Type, ::mlir::Type, ::mlir::TypeStorage, ::mlir::vhlo::VersionedTypeInterface::Trait> {
public:
  using Base::Base;
  mlir::vhlo::Version getMinVersion() {
    auto version = mlir::vhlo::Version::fromString("0.3.0");
    if (failed(version)) llvm_unreachable("invalid version 0.3.0 in witness");
    return *version;
  }
  mlir::vhlo::Version getMaxVersion() {
    if (!strcmp("current", "current")) return Version::getCurrentVersion();
    auto version = mlir::vhlo::Version::fromString("current");
    if (failed(version)) llvm_unreachable("invalid version current in witness");
    return *version;
  }
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"witness"};
  }

};
} // namespace vhlo
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::BFloat16V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::ComplexV1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::Float16V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::Float32V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::Float64V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::Float8E4M3FNV1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::Float8E5M2V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::FunctionV1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::IndexV1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::IntegerI16V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::IntegerI1V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::IntegerI32V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::IntegerI4V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::IntegerI64V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::IntegerI8V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::IntegerUI16V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::IntegerUI32V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::IntegerUI4V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::IntegerUI64V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::IntegerUI8V1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::RankedTensorV1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::TokenV1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::TupleV1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::UniformQuantizedV1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::UnrankedTensorV1Type)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::vhlo::WitnessV1Type)

#endif  // GET_TYPEDEF_CLASSES

