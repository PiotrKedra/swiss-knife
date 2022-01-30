#include "llvm/Transforms/Utils/HelloWorld.h"
#include "llvm/Transforms/Scalar/DCE.h"
#include "llvm/ADT/SetVector.h"
#include "llvm/ADT/SmallVector.h"
#include "llvm/ADT/Statistic.h"
#include "llvm/Analysis/TargetLibraryInfo.h"
#include "llvm/IR/InstIterator.h"
#include "llvm/IR/Instruction.h"
#include "llvm/InitializePasses.h"
#include "llvm/Pass.h"
#include "llvm/Support/DebugCounter.h"
#include "llvm/Transforms/Scalar.h"
#include "llvm/Transforms/Utils/AssumeBundleBuilder.h"
#include "llvm/Transforms/Utils/BasicBlockUtils.h"
#include "llvm/Transforms/Utils/Local.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/Transforms/Scalar/DCE.h"
#include <algorithm>


using namespace llvm;

bool contains(SmallVector<Instruction*, 128> alive, Instruction* I) {
  return std::find(alive.begin(), alive.end(), I) != alive.end();
}

PreservedAnalyses HelloWorldPass::run(Function &F,
                                      FunctionAnalysisManager &AM) {
                                     

  SmallVector<Instruction*, 128> worklist;
  SmallVector<Instruction*, 128> alive;
  bool hasChanged = true;

  while(hasChanged) {
    hasChanged=false;
    for (inst_iterator I = inst_begin(F), E = inst_end(F); I != E; ++I) {

  // if (I.isTerminator() || isa<DbgInfoIntrinsic>(I) || isa<LandingPadInst>(I) || I.mayHaveSideEffects()) {
        if (isInstructionTriviallyDead(&*I)) {
            
            (&*I)->print(errs());
            errs() << " -> ";

            // alive.push_back(&*I);
            worklist.push_back(&*I);
            hasChanged=true;
        }
    }    

  while (!worklist.empty()) {
      Instruction *Curr = worklist.pop_back_val();

      for (unsigned i = 0, e = Curr->getNumOperands(); i != e; ++i) {
          Value *OpV = Curr->getOperand(i);
          Curr->setOperand(i, nullptr);

          if (Instruction *Inst = dyn_cast<Instruction>(OpV)) {
              if (isInstructionTriviallyDead(Inst) || Curr != OpV || OpV->use_empty()) {
                  worklist.push_back(Inst);
              }
          }
      }
    Curr->eraseFromParent();

  }

  }

  return PreservedAnalyses::all();
}

// ./build/bin/opt -S -passes=helloworld ../FunctionWithDeadCode.ll
