package epc.generator;

import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.LocalFileSystem;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.psi.*;

import java.io.File;
import java.util.Objects;

public abstract class Generator {
    protected static final String DEFAULT_JAVA_SRC_PATH = "/src/main/java/";
    protected PsiClass psiClass;
    protected Project project;

    public Generator(PsiClass psiClass) {
        this.psiClass = psiClass;
        this.project = psiClass.getProject();
    }

    public abstract void generateJavaClass();

}
