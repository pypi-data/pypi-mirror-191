// Copyright (C) 2013 Eric Schulte
// Copyright (C) 2019 Jhe-Yu Liou

// Default in LDG mode, define LDCG for disable L1 cache in CMakeFile
#define LDCG
// #define LDG

#include "Mutate.h"
#include <fstream>
#include "llvm/Support/CommandLine.h"

using namespace llvm;

static cl::list<std::string, bool> InstList1("inst1", cl::desc("first statement to mutate"), cl::ZeroOrMore);
cl::opt<std::string> Inst1ID("inst1ID", cl::init(""), cl::desc("The Unique ID of first statement to mutate"));

static cl::list<std::string, bool> InstList2("inst2", cl::desc("second statement to mutate"), cl::ZeroOrMore);
cl::opt<std::string> Inst2ID("inst2ID", cl::init(""), cl::desc("The Unique ID of first statement to mutate"));

cl::opt<bool> use_result("use_result", cl::init(1), cl::desc("Whether to perform the use_result after changing the instruction"));
cl::opt<bool> deterministic("deterministic", cl::init(0), cl::desc("Whether the random process needs to be deterministic"));
cl::opt<int> rnd_seed("seed", cl::init(1), cl::desc("seed for the random sqeuence if deterministic is set. "));

namespace {
  struct Ids : public ModulePass {
    static char ID;
    Ids() : ModulePass(ID) {}

    bool runOnModule(Module &M){
      count = 0;
      for (Module::iterator I = M.begin(), E = M.end(); I != E; ++I)
        walkFunction(&*I);

      errs() << count << "\n";

      return false;
    }

    // We don't modify the program, so we preserve all analyses
    virtual void getAnalysisUsage(AnalysisUsage &AU) const {
      AU.setPreservesAll(); }

  private:
    int unsigned count;
    void walkFunction(Function *F){
      for (inst_iterator I = inst_begin(F), E = inst_end(F); I != E; ++I) {
        if (I->getName().find("nop") == StringRef::npos)
          count += 1;
      }
    }
  };
}

namespace {
  struct List : public ModulePass {
    static char ID;
    List() : ModulePass(ID) {}

    bool runOnModule(Module &M){
      listf.open("/tmp/llvm_mutate_list.txt", std::ios::out);
      if (!listf.is_open())
        return 1;

      for (Function &F: M) {
      for (Instruction &TI : instructions(F)) {
        StringRef UID = getUID(&TI);
        if (UID.empty())
          continue;
        if (!isValidTarget(&TI))
          continue;

        // Cut
        if (TI.use_empty())
          listf << "[('-c', '" << UID.str() << "')]\n";
        else {
          std::vector<std::pair<Value*, StringRef>> resultVec;
          CollectValueBeforeI(&F, &TI, cast<Value>(&TI), resultVec);
          // Equivalent to replaceAllUsesWithReport
          for (std::pair<Value*, StringRef> metaV : resultVec) {
            listf << "[('-c', '" << UID.str() << "')";
            for (Use &U : TI.uses()) {
              Instruction *UI = cast<Instruction>(U.getUser());
              std::string UIID = getUID(UI).str();
              UIID = UIID + ".OP" + std::to_string(U.getOperandNo());
              listf << ", ('-p', '" << UIID << "," << metaV.second.str() << "')";
            }
            listf << "]\n";
          }
        }
        // Insert
        for (Function &_F: M) {
        for (Instruction &SI : instructions(_F)) {
          bool failed = false;
          if (!isValidTarget(&SI))
            continue;

          Instruction* SIclone = SI.clone();
          // We have to truely insert the cloned instruction so that the dominate analysis
          // can work.
          SIclone->insertBefore(&TI);
          updateMetadata(SIclone, "i");
          std::string mainMu = "[('-i', '" + getUID(TI).str() + "," + getUID(SI).str() + "')";
 
          bool printSucceed = iterInstComb(listf, SIclone, &SI, 0, mainMu);
          SIclone->eraseFromParent();
        }}
      }}
      listf.close();
      return RET_SUCCESS;
    }

  private:
    std::vector<std::string> mutatePool;
    std::fstream listf;
  };
}

namespace {
  struct Name : public ModulePass {
    static char ID;
    Name() : ModulePass(ID) {}

    bool runOnModule(Module &M){
      Icount = 0;
      Acount = 0;;
      for (Function &F : M)
        walkFunction(&F);
      return false;
    }

    // We don't modify the program, so we preserve all analyses
    virtual void getAnalysisUsage(AnalysisUsage &AU) const {
      AU.setPreservesAll(); }

  private:
    unsigned Icount, Acount;

    void walkFunction(Function *F){
      for (Argument &A : F->args()) {
        Acount++;
        std::string AID = "A" + std::to_string(Acount);
        A.setName(AID);
      }

      for (inst_iterator I = inst_begin(F), E = inst_end(F); I != E; ++I) {
        Icount += 1;
        std::string UID = "U" + std::to_string(Icount);
        setUID(&*I, UID);
        if (!I->getType()->isVoidTy())
          I->setName(UID);
      }
    }
  };
}

// We don't stack query operation with others, so no need to pop the insturction list
namespace {
  struct Query : public ModulePass {
    static char ID;
    Query() : ModulePass(ID) {}

    bool runOnModule(Module &M){;
      std::string Inst1 = InstList1[0];
      Instruction *I = dyn_cast_or_null<Instruction>(walkExact(Inst1, Inst1ID, M, NULL, false));
      if (I == NULL) {
        errs() << "Query failed. Cannot find " << Inst1 << "\n";
        return RET_ERROR;
      }
      DILocation *Loc = I->getDebugLoc();
      if (Loc == NULL) {
        errs() << "Query failed. " << Inst1 << " has no source line info\n";
        return RET_ERROR; 
      }
      if (Loc->isImplicitCode())
        errs() << "Query uncertain. " << Inst1 << " is implicit code\n";
      errs() << Loc->getDirectory() << '/' << Loc->getFilename() 
             << ':' << Loc->getLine() << ':' << Loc->getColumn();
      if (DebugLoc InlinedAtDL = Loc->getInlinedAt()) {
        errs() << " @[ ";
        InlinedAtDL.print(errs());
        errs() << " ]";
      }
      errs() << "\n";
      return RET_SUCCESS;
    }

    // We don't modify the program, so we preserve all analyses
    virtual void getAnalysisUsage(AnalysisUsage &AU) const {
      AU.setPreservesAll(); }
  };
}

namespace {
  struct Cut : public ModulePass {
    static char ID;
    Cut() : ModulePass(ID) {}

    bool runOnModule(Module &M){
      if (deterministic)
        gen.seed(unsigned(rnd_seed));

      std::string Inst1 = InstList1[0];
      InstList1.erase(InstList1.begin());
      InstList2.erase(InstList2.begin());
      Instruction *I = dyn_cast_or_null<Instruction>(walkExact(Inst1, Inst1ID, M, NULL, true));
      if (I == NULL) {
        errs() << "cut failed("<< Inst1 << "). Cannot find/use " << Inst1 << "\n";
        return RET_ERROR; }

      insertNOP(I);
      // decouple the dependence from later instructions
      // This cannot be omitted, otherwise the llvm-dis will have segfault
      if(!I->use_empty()){
        std::pair<Value*, StringRef> Val =
          randValueBeforeI(I->getFunction(), I, cast<Value>(I), deterministic);
        if(Val.first != NULL)
          replaceAllUsesWithReport(I, Val);
      }
      // TODO: have a function as a recycle bin to store deleted inst
      I->eraseFromParent();
      errs() << "cut " << Inst1ID << "\n";
      return RET_SUCCESS;}
  };
}

namespace {
  struct Insert : public ModulePass {
    static char ID;
    Insert() : ModulePass(ID) {}

    bool runOnModule(Module &M){
      if (deterministic)
        gen.seed(unsigned(rnd_seed));

      Instruction *temp;
      std::string Inst1 = InstList1[0];
      std::string Inst2 = InstList2[0];
      InstList1.erase(InstList1.begin());
      InstList2.erase(InstList2.begin());
      Instruction *SI = walkCollect(Inst2, Inst2ID, M);
      Instruction *DI = walkPosition(Inst1, Inst1ID, M);
      if (SI == NULL or DI == NULL) {
        errs()<<"insertion failed("<< Inst1 << "," << Inst2 << "). Cannot find/use ";
        if (DI == NULL) errs()<<Inst1 << " ";
        if (SI == NULL) errs()<<Inst2 << " ";
        errs() << "\n";
        return RET_ERROR; }

      temp = SI->clone();
      // TODO: figure why the new API droplocation() has to consider callInst 
      temp->setDebugLoc(DebugLoc()); // remove debug information if any 
      Inst2ID = getUID(SI).str();

      temp->insertBefore(&*DI); // insert temp before DI
      updateMetadata(temp, "i");
      replaceUnfulfillOperands(temp, deterministic); // wire incoming edges of CFG into temp
      // check if I generates a result which is used, if not then
      // it is probably run for side effects and we don't need to
      // wire the result of the copy of I to something later on
      bool result_ignorable_p = SI->use_empty();
      if(!result_ignorable_p && use_result)
        useResult(temp, deterministic); // wire outgoing results of temp into CFG

      errs()<<"inserted " << Inst1ID << "," << Inst2ID << "\n";
      return RET_SUCCESS;
    }
  };
}

namespace {
  struct Replace : public ModulePass {
    static char ID; // pass identification
    Replace() : ModulePass(ID) {}

    bool runOnModule(Module &M){
      if (deterministic)
        gen.seed(unsigned(rnd_seed));

      Instruction *temp;
      std::string Inst1 = InstList1[0];
      std::string Inst2 = InstList2[0];
      InstList1.erase(InstList1.begin());
      InstList2.erase(InstList2.begin());
      Instruction *SI = walkCollect(Inst2, Inst2ID, M);
      Instruction *DI = walkPosition(Inst1, Inst1ID, M);
      if (SI == NULL or DI == NULL) {
        errs()<<"replace failed("<< Inst1 << "," << Inst2 << "). Cannot find/use ";
        if (DI == NULL) errs()<<Inst1 << " ";
        if (SI == NULL) errs()<<Inst2 << " ";
        errs() << "\n";
        
        return RET_ERROR; }

      if (DI->getType() != SI->getType()) {
        errs()<<"replace failed("<< Inst1 << "," << Inst2 << "). could find no use for the result.\n";
        return RET_ERROR;
      }

      temp = SI->clone();
      temp->setDebugLoc(DebugLoc()); // remove debug information if any 

      insertNOP(&*DI);
      ReplaceInstWithInst(DI, temp);
      updateMetadata(temp, "r");
      replaceUnfulfillOperands(temp, deterministic);

      errs()<<"replaced "<< Inst1ID << "," << Inst2ID << "\n";
      return RET_SUCCESS; }
  };
}

namespace {
  struct OPRepl : public ModulePass {
    static char ID; // pass identification
    OPRepl() : ModulePass(ID) {}

    bool runOnModule(Module &M){
      if (deterministic)
        gen.seed(unsigned(rnd_seed));

      int err = 0;
      std::string Inst1 = InstList1[0];
      std::string Inst2 = InstList2[0];
      InstList1.erase(InstList1.begin());
      InstList2.erase(InstList2.begin());
      // Type* T;
      if (Inst1 == "Rand" && Inst2 != "Rand") {
        Value* sval = walkExact(Inst2, Inst2ID, M, NULL, false);
        if (sval == NULL){
          errs() << "oprepl failed("<< Inst1 << "," << Inst2 << "). cannot find " << Inst2 << "\n";
          return RET_ERROR;
        }
        std::pair<Instruction*, unsigned> result;
        if (Inst2[0] == 'A')
          result = randOperandAfterI(
            *cast<Argument>(sval)->getParent(),
            NULL, // search from the start of function
            sval->getType(),
            deterministic
          );
        else
          result = randOperandAfterI(
            *cast<Instruction>(sval)->getFunction(),
            cast<Instruction>(sval),
            sval->getType(),
            deterministic
          );
        if (result.first == NULL) {
          errs() << "oprepl failed("<< Inst1 << "," << Inst2 << "). cannot find an OP that has the same type as " << Inst2 << "\n";
          return RET_ERROR;
        }

        Instruction* DI = result.first;
        unsigned OPidx = result.second;
        DI->setOperand(OPidx, sval);
        Inst1ID = getUID(DI).str();
        Inst1ID = Inst1ID + ".OP" + std::to_string(OPidx);
        errs()<<"opreplaced "<< Inst1ID << "," << Inst2ID << "\n";
        return RET_SUCCESS;
      }
      else if (Inst1 != "Rand" && Inst2 == "Rand") {
        StringRef dstInstBase = (StringRef(Inst1)).rsplit('.').first;
        StringRef dstOP = (StringRef(Inst1)).rsplit('.').second;
        assert(dstOP.find("OP") != StringRef::npos && "Not a valid operand description!");
        unsigned OPidx = std::stoi(dstOP.drop_front(2).str());// remove "OP"
        Instruction *DI = dyn_cast_or_null<Instruction>(walkExact(dstInstBase.str(), Inst1ID, M, NULL, false));
        if (DI == NULL){
          errs() << "oprepl failed("<< Inst1 << "," << Inst2 << "). cannot find" << dstInstBase << "\n";
          return RET_ERROR;
        }
        Inst1ID = Inst1ID + ".OP" + std::to_string(OPidx);
        Value *Dop = DI->getOperand(OPidx);
        std::pair<Value*, StringRef> sval = randValueBeforeI(DI->getFunction(), DI, Dop, deterministic);
        DI->setOperand(OPidx, sval.first);
        Inst2ID = sval.second.str();

        errs()<<"opreplaced "<< Inst1ID << "," << Inst2ID << "\n";
        return RET_SUCCESS;
      }
      else if (Inst1 == "Rand" && Inst2 == "Rand") {
        std::pair<Value*, StringRef> val = randValue(M, deterministic);
        Value *sval = val.first;
        Inst2ID = val.second.str();
        std::pair<Instruction*, unsigned> result;
        if (Inst2ID[0] == 'A')
          result = randOperandAfterI(
            *cast<Argument>(sval)->getParent(),
            NULL, // search from the start of function
            sval->getType(),
            deterministic
          );
        else
          result = randOperandAfterI(
            *cast<Instruction>(sval)->getFunction(),
            cast<Instruction>(sval),
            sval->getType(),
            deterministic
          );
        if (result.first == NULL) {
          errs() << "oprepl failed("<< Inst1 << "," << Inst2 << "). cannot find an OP that has the same type as " << Inst2ID << "\n";
          return RET_ERROR;
        }

        Instruction* DI = result.first;
        unsigned OPidx = result.second;
        DI->setOperand(OPidx, sval);
        Inst1ID = getUID(DI).str();
        Inst1ID = Inst1ID + ".OP" + std::to_string(OPidx);
        errs()<<"opreplaced "<< Inst1ID << "," << Inst2ID << "\n";
        return RET_SUCCESS;
      }
      else { // both != "Rand"
        err = replaceOperands(Inst1, Inst2, M);
        if (err == 0)
          return RET_SUCCESS;
        else if (err == 1) {
          errs() << "Warning: oprepl ignored. Source and Destination are the same" << "\n";
          return RET_WARNING;
        }
        else if (err == -1)
          errs() << "oprepl failed("<< Inst1 << "," << Inst2 << "). cannot find " << Inst1 << "\n";
        else if (err == -2)
          errs() << "oprepl failed("<< Inst1 << "," << Inst2 << "). out of operand index range" << "\n";
        else if (err == -3)
          errs() << "oprepl failed("<< Inst1 << "," << Inst2 << "). source instruction does not have an output" << "\n";
        else if (err == -4)
          errs() << "oprepl failed("<< Inst1 << "," << Inst2 << "). type mismatched" << "\n";
        else if (err == -5)
          errs() << "oprepl failed("<< Inst1 << "," << Inst2 << "). cannot find " << Inst2 << "\n";
        else if (err == -6)
          errs() << "oprepl failed("<< Inst1 << "," << Inst2 << "). dest operand " << Inst1 << " is a function argument with immarg attribute\n";
        else if (err == -7)
          errs() << "oprepl failed("<< Inst1 << "," << Inst2 << "). "<< Inst2 << " does not dominate " << Inst1 << "\n";
        return RET_ERROR;
      }
    }
  };
}

namespace {
  struct Move : public ModulePass {
    static char ID; // pass identification
    Move() : ModulePass(ID) {}

    bool runOnModule(Module &M){
      if (deterministic)
        gen.seed(unsigned(rnd_seed));

      std::string Inst1 = InstList1[0];
      std::string Inst2 = InstList2[0];
      InstList1.erase(InstList1.begin());
      InstList2.erase(InstList2.begin());
      Instruction *temp;
      Instruction *SI = dyn_cast_or_null<Instruction>(walkExact(Inst2, Inst2ID, M, NULL, true));
      Instruction *DI = walkPosition(Inst1, Inst1ID, M);

      if (SI == NULL or DI == NULL) {
        errs()<<"Move failed("<< Inst1 << "," << Inst2 << "). Cannot find/use ";
        if (DI == NULL) errs()<<Inst1 << " ";
        if (SI == NULL) errs()<<Inst2 << " ";
        errs() << "\n";
        return RET_ERROR; }

      temp = SI->clone();
      temp->setDebugLoc(DebugLoc()); // remove debug information if any 
      Inst2ID = getUID(SI).str();

      temp->insertBefore(&*DI); // insert temp before DI
      updateMetadata(temp, "m");
      insertNOP(SI);

      replaceUnfulfillOperands(temp, deterministic);
      bool result_ignorable_p = SI->use_empty();
      if(!result_ignorable_p && use_result)
        useResult(temp, deterministic);
      // Delete the source instruction if it is there
      if(!SI->use_empty()){
        std::pair<Value*, StringRef> Val =
          randValueBeforeI(SI->getFunction(), SI, cast<Value>(SI), deterministic);
        if(Val.first != NULL)
          replaceAllUsesWithReport(SI, Val);
      }

      // TODO: have a function as a recycle bin to store deleted inst
      SI->eraseFromParent();

      errs()<<"moved " << Inst1ID << "," << Inst2ID << "\n";
      return RET_SUCCESS; }
  };
}

namespace {
  struct Swap : public ModulePass {
    static char ID; // pass identification
    Swap() : ModulePass(ID) {}

    bool runOnModule(Module &M){
      if (deterministic)
        gen.seed(unsigned(rnd_seed));

      std::string Inst1 = InstList1[0];
      std::string Inst2 = InstList2[0];
      InstList1.erase(InstList1.begin());
      InstList2.erase(InstList2.begin());
      Instruction *temp1, *temp2;
      Instruction *I1 = dyn_cast_or_null<Instruction>(walkExact(Inst1, Inst1ID, M, NULL, true));
      Instruction *I2 = dyn_cast_or_null<Instruction>(walkExact(Inst2, Inst2ID, M, NULL, true));
      if (I1 == NULL or I2 == NULL) {
        errs()<<"swap failed("<< Inst1 << "," << Inst2 << "). Cannot find/use ";
        if (I1 == NULL) errs()<<Inst1 << " ";
        if (I2 == NULL) errs()<<Inst2 << " ";
        errs() << "\n";
        return RET_ERROR; }

      temp1 = I1->clone();
      temp1->setDebugLoc(DebugLoc());
      temp2 = I2->clone();
      temp2->setDebugLoc(DebugLoc());

      // confirm that the types match
      if(temp1->getType() != temp2->getType()) {
        errs() << "type mismatch " <<
          temp1->getType() << " and " <<
          temp2->getType() << "\n";
        temp1->deleteValue();
        temp2->deleteValue();
        return RET_ERROR; }

      insertNOP(&*I1);
      insertNOP(&*I2);
      bool result_ignorable_p1 = I1->use_empty();
      bool result_ignorable_p2 = I2->use_empty();
      ReplaceInstWithInst(I2, temp1);
      updateMetadata(temp1, "s");
      replaceUnfulfillOperands(temp1, deterministic);
      if(!result_ignorable_p1 && use_result)
        useResult(temp1, deterministic);
      ReplaceInstWithInst(I1, temp2);
      updateMetadata(temp2, "s");
      replaceUnfulfillOperands(temp2, deterministic);
      if(!result_ignorable_p2 && use_result)
        useResult(temp2, deterministic);

      errs()<<"swapped " << Inst1ID << "," << Inst2ID << "\n";

      return RET_SUCCESS; }
  };
}

namespace {
  struct Cache : public ModulePass {
    static char ID; // pass identification
    Cache() : ModulePass(ID) {}
    bool runOnModule(Module &M){
      if (deterministic)
        gen.seed(unsigned(rnd_seed));

      std::string Inst1 = InstList1[0];
      std::string Inst2 = InstList2[0];
      InstList1.erase(InstList1.begin());
      InstList2.erase(InstList2.begin());
      Instruction *I;
      if (Inst1 == "Rand") {
        std::pair<Instruction*, StringRef> result = randTexCachableI(M, deterministic);
        I = result.first;
        Inst1ID = result.second.str();
      }
      else {
        I = dyn_cast_or_null<Instruction>(walkExact(Inst1, Inst1ID, M, NULL, true));
        if (I == NULL) {
          errs() << "cache failed("<< Inst1 << "," << Inst2 << "). Cannot find/use " << Inst1 << "\n";
          return RET_ERROR; }
      }

      Instruction *newI;
      if (isa<LoadInst>(I)) {
        std::vector<Value*>args;
        args.push_back(I->getOperand(0));
#ifdef LDCG
        InlineAsm *ldcgF;
        ldcgF = ldcgGen(M, I->getOperand(0)->getType(), I->getType());
        newI = CallInst::Create(ldcgF->getFunctionType(), ldcgF, args, I->getName());
#else
        Function *ldgFun;
        ldgFun = ldgGen(M, I->getOperand(0)->getType(), I->getType());
        args.push_back(ConstantInt::get(
          Type::getInt32Ty(M.getContext()),
          cast<LoadInst>(I)->getAlignment()
        ));
        newI = CallInst::Create(ldgFun, args, I->getName());
#endif
      }
      else if (isa<CallInst>(I)){
        if (cast<CallInst>(I)->isIndirectCall()) {
          errs() << Inst1 << " is not a proper instruction for manipulating cache behavior.\n";
          return RET_ERROR;
        }
        // // Check if called function is ldg()
        // if (!cast<CallInst>(I)->getCalledFunction()->getName().contains(ldgPre)) {
        //   errs() << Inst1 << " is not a proper instruction for manipulating cache behavior.\n";
        //   return RET_ERROR;
        // }
        newI = new LoadInst(
          I->getType(),     // output type
          I->getOperand(0), // address value
          I->getName(),     // Instruction name
          false,            // is volatile?
#ifdef LDCG
          Align(getAlignFromType(M, I->getOperand(0)->getType()))
#else
          Align(cast<ConstantInt>(I->getOperand(1))->getValue().getSExtValue())   // align
#endif
        );
      }
      else{
        errs() << Inst1 << " is not a proper instruction for manipulating cache behavior.\n";
        return RET_ERROR;
      }

      setUID(newI, getUID(I));
      newI->setMetadata("tbaa", I->getMetadata("tbaa"));
      ReplaceInstWithInst(I, newI);
      updateMetadata(newI, "x");

      errs()<<"cache " << Inst1ID << "\n";
      return RET_SUCCESS;
    }
  };
}

char Ids::ID = 0;
char List::ID = 0;
char Name::ID = 0;
char Query::ID = 0;
char Cut::ID = 0;
char Insert::ID = 0;
char Move::ID = 0;
char Replace::ID = 0;
char OPRepl::ID = 0;
char Cache::ID = 0;
char Swap::ID = 0;
static RegisterPass<Ids>     S("ids",     "print the number of instructions");
static RegisterPass<List>    T("list",    "list all possible mutation");
static RegisterPass<Name>    U("name",    "name each instruction by its id");
static RegisterPass<Query>   V("query",   "query the instruction's source line info");
static RegisterPass<Cut>     W("cut",     "cut instruction number inst1");
static RegisterPass<Insert>  X("insert",  "insert inst2 before inst1");
static RegisterPass<Replace> Y("replace", "replace inst1 with inst2");
static RegisterPass<Move>    ZA("move",   "move inst2 before inst1");
static RegisterPass<OPRepl>  ZB("oprepl", "replace operand with inst");
static RegisterPass<Cache>   ZC("cache",  "toggle cache behavior of a load instruction");
static RegisterPass<Swap>    Z("swap",    "swap inst1 and inst2");
