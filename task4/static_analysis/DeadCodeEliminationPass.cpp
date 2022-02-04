#include "llvm/Transforms/Utils/DeadCodeElimination.h"
#include "llvm/IR/Constants.h"

using namespace llvm;

PreservedAnalyses DeadCodeEliminationPass::run(Function &F,
                                      FunctionAnalysisManager &AM) {
                                     
  bool wasRemoved = true;
  while (wasRemoved) {
    wasRemoved = false;
    for(auto bb_it = F.begin(), bb_end = F.end(); bb_it != bb_end; ++bb_it) {
      for(auto i_it = bb_it->begin(), i_end = bb_it->end(); i_it != i_end;) {

        if (i_it->isSafeToRemove() == true && i_it->use_empty() == true) {
          i_it = i_it->eraseFromParent();
          wasRemoved = true;
        } else {
          ++i_it;
        }
      }
    }
  }
  
  return PreservedAnalyses::all();
}
