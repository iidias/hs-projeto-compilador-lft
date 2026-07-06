from abc import abstractmethod, ABCMeta

class Program(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor): pass

class SingleDecl(Program):
    def __init__(self, decl):
        self.decl = decl
    def accept(self, visitor):
        return visitor.visitSingleDecl(self)

class CompoundDecl(Program):
    def __init__(self, decl, program):
        self.decl = decl
        self.program = program
    def accept(self, visitor):
        return visitor.visitCompoundDecl(self)

class Decl(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor): pass

class TypeSig(Decl):
    def __init__(self, name, type_expr):
        self.name = name
        self.type_expr = type_expr
    def accept(self, visitor):
        return visitor.visitTypeSig(self)

class FuncDecl(Decl):
    def __init__(self, name, pats, body):
        self.name = name
        self.pats = pats
        self.body = body
    def accept(self, visitor):
        return visitor.visitFuncDecl(self)

class FuncDeclWhere(Decl):
    def __init__(self, name, pats, body, where_decls):
        self.name = name; self.pats = pats
        self.body = body; self.where_decls = where_decls
    def accept(self, visitor):
        return visitor.visitFuncDeclWhere(self)

class FuncDeclGuards(Decl):
    def __init__(self, name, pats, guards):
        self.name = name; self.pats = pats; self.guards = guards
    def accept(self, visitor):
        return visitor.visitFuncDeclGuards(self)

class DataDecl(Decl):
    def __init__(self, name, constructors):
        self.name = name; self.constructors = constructors
    def accept(self, visitor):
        return visitor.visitDataDecl(self)

class TypeExpr(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor): pass

class SimpleType(TypeExpr):
    def __init__(self, name): self.name = name
    def accept(self, visitor): return visitor.visitSimpleType(self)

class ArrowType(TypeExpr):
    def __init__(self, left, right): self.left = left; self.right = right
    def accept(self, visitor): return visitor.visitArrowType(self)

class ListType(TypeExpr):
    def __init__(self, elem): self.elem = elem
    def accept(self, visitor): return visitor.visitListType(self)

class TupleType(TypeExpr):
    def __init__(self, types): self.types = types
    def accept(self, visitor): return visitor.visitTupleType(self)

class UnitType(TypeExpr):
    def accept(self, visitor): return visitor.visitUnitType(self)

class Ctor(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor): pass

class Constructor(Ctor):
    def __init__(self, name): self.name = name
    def accept(self, visitor): return visitor.visitConstructor(self)

class ConstructorArgs(Ctor):
    def __init__(self, name, types): self.name = name; self.types = types
    def accept(self, visitor): return visitor.visitConstructorArgs(self)

class Guard:
    def __init__(self, cond, body): self.cond = cond; self.body = body
    def accept(self, visitor): return visitor.visitGuard(self)

class SingleGuards:
    def __init__(self, guard): self.guard = guard
    def accept(self, visitor): return visitor.visitSingleGuards(self)

class CompoundGuards:
    def __init__(self, guards, guard): self.guards = guards; self.guard = guard
    def accept(self, visitor): return visitor.visitCompoundGuards(self)

class LocalDecls(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor): pass

class SingleLocaldecl(LocalDecls):
    def __init__(self, decl): self.decl = decl
    def accept(self, visitor): return visitor.visitSingleLocaldecl(self)

class CompoundLocaldecl(LocalDecls):
    def __init__(self, decls, decl): self.decls = decls; self.decl = decl
    def accept(self, visitor): return visitor.visitCompoundLocaldecl(self)

class Exp(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor): pass

class VarExp(Exp):
    def __init__(self, name): self.name = name
    def accept(self, visitor): return visitor.visitVarExp(self)

class ConExp(Exp):
    def __init__(self, name): self.name = name
    def accept(self, visitor): return visitor.visitConExp(self)

class IntExp(Exp):
    def __init__(self, value): self.value = value
    def accept(self, visitor): return visitor.visitIntExp(self)

class BoolExp(Exp):
    def __init__(self, value): self.value = value
    def accept(self, visitor): return visitor.visitBoolExp(self)

class CharExp(Exp):
    def __init__(self, value): self.value = value
    def accept(self, visitor): return visitor.visitCharExp(self)

class StringExp(Exp):
    def __init__(self, value): self.value = value
    def accept(self, visitor): return visitor.visitStringExp(self)

class AppExp(Exp):
    def __init__(self, func, arg): self.func = func; self.arg = arg
    def accept(self, visitor): return visitor.visitAppExp(self)

class InfixExp(Exp):
    def __init__(self, op, left, right): self.op = op; self.left = left; self.right = right
    def accept(self, visitor): return visitor.visitInfixExp(self)

class NegExp(Exp):
    def __init__(self, expr): self.expr = expr
    def accept(self, visitor): return visitor.visitNegExp(self)

class NotExp(Exp):
    def __init__(self, expr): self.expr = expr
    def accept(self, visitor): return visitor.visitNotExp(self)

class IfExp(Exp):
    def __init__(self, cond, then_e, else_e):
        self.cond = cond; self.then_e = then_e; self.else_e = else_e
    def accept(self, visitor): return visitor.visitIfExp(self)

class CaseExp(Exp):
    def __init__(self, expr, alts): self.expr = expr; self.alts = alts
    def accept(self, visitor): return visitor.visitCaseExp(self)

class LetExp(Exp):
    def __init__(self, decls, body): self.decls = decls; self.body = body
    def accept(self, visitor): return visitor.visitLetExp(self)

class DoExp(Exp):
    def __init__(self, stmts): self.stmts = stmts
    def accept(self, visitor): return visitor.visitDoExp(self)

class LambdaExp(Exp):
    def __init__(self, pats, body): self.pats = pats; self.body = body
    def accept(self, visitor): return visitor.visitLambdaExp(self)

class ListExp(Exp):
    def __init__(self, elems): self.elems = elems
    def accept(self, visitor): return visitor.visitListExp(self)

class EmptyListExp(Exp):
    def accept(self, visitor): return visitor.visitEmptyListExp(self)

class RangeExp(Exp):
    def __init__(self, start, end): self.start = start; self.end = end
    def accept(self, visitor): return visitor.visitRangeExp(self)

class TupleExp(Exp):
    def __init__(self, elems): self.elems = elems
    def accept(self, visitor): return visitor.visitTupleExp(self)

class CaseAlts(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor): pass

class SingleCaseAlts(CaseAlts):
    def __init__(self, alt): self.alt = alt
    def accept(self, visitor): return visitor.visitSingleCaseAlts(self)

class CompoundCaseAlts(CaseAlts):
    def __init__(self, alts, alt): self.alts = alts; self.alt = alt
    def accept(self, visitor): return visitor.visitCompoundCaseAlts(self)

class CaseAlt:
    def __init__(self, pat, body): self.pat = pat; self.body = body
    def accept(self, visitor): return visitor.visitCaseAlt(self)

class DoStmts(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor): pass

class SingleDoStmts(DoStmts):
    def __init__(self, stmt): self.stmt = stmt
    def accept(self, visitor): return visitor.visitSingleDoStmts(self)

class CompoundDoStmts(DoStmts):
    def __init__(self, stmts, stmt): self.stmts = stmts; self.stmt = stmt
    def accept(self, visitor): return visitor.visitCompoundDoStmts(self)

class BindStmt:
    def __init__(self, var, expr): self.var = var; self.expr = expr
    def accept(self, visitor): return visitor.visitBindStmt(self)

class LetDoStmt:
    def __init__(self, decls): self.decls = decls
    def accept(self, visitor): return visitor.visitLetDoStmt(self)

class ExprDoStmt:
    def __init__(self, expr): self.expr = expr
    def accept(self, visitor): return visitor.visitExprDoStmt(self)

class Pat(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor): pass

class WildcardPat(Pat):
    def accept(self, visitor): return visitor.visitWildcardPat(self)

class VarPat(Pat):
    def __init__(self, name): self.name = name
    def accept(self, visitor): return visitor.visitVarPat(self)

class ConPat(Pat):
    def __init__(self, name): self.name = name
    def accept(self, visitor): return visitor.visitConPat(self)

class IntPat(Pat):
    def __init__(self, value): self.value = value
    def accept(self, visitor): return visitor.visitIntPat(self)

class BoolPat(Pat):
    def __init__(self, value): self.value = value
    def accept(self, visitor): return visitor.visitBoolPat(self)

class CharPat(Pat):
    def __init__(self, value): self.value = value
    def accept(self, visitor): return visitor.visitCharPat(self)

class ConsPat(Pat):
    def __init__(self, head, tail): self.head = head; self.tail = tail
    def accept(self, visitor): return visitor.visitConsPat(self)

class TuplePat(Pat):
    def __init__(self, pats): self.pats = pats
    def accept(self, visitor): return visitor.visitTuplePat(self)

class ListPat(Pat):
    def __init__(self, pats): self.pats = pats
    def accept(self, visitor): return visitor.visitListPat(self)

class EmptyListPat(Pat):
    def accept(self, visitor): return visitor.visitEmptyListPat(self)
