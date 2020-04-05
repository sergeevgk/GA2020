package epc.action;

import com.intellij.ide.util.TreeFileChooser;
import com.intellij.ide.util.TreeFileChooserFactory;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.command.WriteCommandAction;
import com.intellij.openapi.fileChooser.FileChooser;
import com.intellij.openapi.fileChooser.FileChooserDescriptor;
import com.intellij.openapi.fileChooser.FileChooserDescriptorFactory;
import com.intellij.openapi.fileTypes.FileType;
import com.intellij.openapi.fileTypes.StdFileTypes;
import com.intellij.openapi.module.Module;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.psi.*;

import com.intellij.psi.impl.PsiFileFactoryImpl;
import com.intellij.psi.search.FilenameIndex;
import com.intellij.psi.search.GlobalSearchScope;
import epc.generator.SingletonGenerator;
import epc.generator.VisitorGenerator;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;
import java.io.File;
import java.io.IOException;
import java.util.List;

public class VisitorAction extends EpcAction {

    PsiClass[] concreteComponents;

    PsiClass interfaceVisitor;

    PsiClass interfaceComponent;

    @Override
    public void safeActionPerformed(AnActionEvent anActionEvent) {
        PsiClass psiClass = extractPsiClass(anActionEvent);
        Project project = psiClass.getProject();

        final FileChooserDescriptor descriptor = FileChooserDescriptorFactory.createMultipleFilesNoJarsDescriptor();
        descriptor.setTitle("Components chooser");
        descriptor.setShowFileSystemRoots(false);
        descriptor.setDescription("Choose components to be visited: ");
        descriptor.setHideIgnored(true);
        descriptor.setRoots(project.getBaseDir());
        descriptor.setForcedToUseIdeaFileChooser(true);
        descriptor.withFileFilter(file -> file.getFileType().equals(StdFileTypes.JAVA));
        VirtualFile[] components = FileChooser.chooseFiles(descriptor, project, project.getBaseDir());

        generateCode(psiClass, components);
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

    private void generateCode(PsiClass psiClass, VirtualFile[] components) {
        if (components == null) {
            return;
        }

        WriteCommandAction.runWriteCommandAction(
                psiClass.getProject(),
                () -> new VisitorGenerator(psiClass, components)
                        .generateJavaClass()
        );
    }
}
