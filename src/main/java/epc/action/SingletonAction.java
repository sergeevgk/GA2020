package epc.action;

import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.command.WriteCommandAction;
import com.intellij.psi.PsiClass;
import com.intellij.psi.PsiModifier;
import epc.generator.SingletonGenerator;
import org.jetbrains.annotations.NotNull;

public class SingletonAction extends EpcAction {
    @Override
    public void safeActionPerformed(AnActionEvent anActionEvent) {
        PsiClass psiClass = extractPsiClass(anActionEvent);
        generateCode(psiClass);
    }

    @Override
    public void update(@NotNull AnActionEvent anActionEvent) {
        safeExecute(() -> {
            super.update(anActionEvent);
            PsiClass psiClass = extractPsiClass(anActionEvent);
            if (psiClass.getModifierList() != null && psiClass.getModifierList().hasModifierProperty(PsiModifier.STATIC)) {
                throw new RuntimeException();
            }
        }, anActionEvent);
    }

    private void generateCode(PsiClass psiClass) {
        WriteCommandAction.runWriteCommandAction(
                psiClass.getProject(),
                () -> new SingletonGenerator(psiClass)
                        .generateJavaClass()
        );
    }
}
