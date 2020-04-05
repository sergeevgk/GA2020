package epc.generator;

import com.intellij.openapi.fileTypes.StdFileTypes;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.psi.*;
import epc.utils.PsiModifierWrapper;
import epc.utils.TemplateProvider;

import java.io.File;
import java.util.Arrays;

import static epc.utils.StringUtils.toFirstLetterLowerCase;

public class VisitorGenerator extends Generator implements TemplateProvider {

    private static final String INTERFACE_COMPONENT_NAME = "Component.java";
    private static final String INTERFACE_VISITOR_NAME = "Visitor.java";
    private static final String CONCRETE_VISITOR_NAME = "ConcreteVisitor.java";
    private static final String CONCRETE_VISITOR_TEMPLATE_PATH = "/templates/concrete-visitor";
    private static final String INTERFACE_COMPONENT_TEMPLATE_PATH = "/templates/interface-component";
    private static final String INTERFACE_VISITOR_TEMPLATE_PATH = "/templates/interface-visitor";
    private static final String METHOD_VISITOR_SIGNATURE = "/templates/visit-method-signature";
    private static final String METHOD_ACCEPT = "/templates/accept-method";
    private static final String METHOD_VISIT_IMPLEMENTATION_PATH = "/templates/visit-method-implementation";

    private PsiClass[] concreteComponents;
    PsiClass interfaceVisitor;
    PsiClass interfaceComponent;

    public VisitorGenerator(PsiClass psiClass, VirtualFile[] components) {
        super(psiClass);
        createPsiClasses(psiClass.getProject(), components);
    }

    @Override
    public void generateJavaClass() {
        interfaceComponent = generatePsiClass(INTERFACE_COMPONENT_TEMPLATE_PATH, INTERFACE_COMPONENT_NAME);
        String[] signatures = new String[concreteComponents.length];

        for (int i = 0; i < signatures.length; i++) {
            String className = concreteComponents[i].getName();
            signatures[i] = String.format(
                    provideTemplateContent(METHOD_VISITOR_SIGNATURE),
                    className,
                    className,
                    toFirstLetterLowerCase(className));
        }
        String allSignatures = String.join("\n", signatures);
        interfaceVisitor = generatePsiClass(INTERFACE_VISITOR_TEMPLATE_PATH, INTERFACE_VISITOR_NAME, allSignatures);

        PsiElementFactory psiElementFactory = PsiElementFactory.getInstance(psiClass.getProject());
        PsiJavaCodeReferenceElement referenceInterfaceComponent = psiElementFactory.createClassReferenceElement(interfaceComponent);

        Arrays.asList(concreteComponents).forEach(el -> {
            PsiReferenceList psiReferenceList = el.getImplementsList();
            psiReferenceList.add(referenceInterfaceComponent);

            addAcceptMethod(el);
        });

        String[] visitMethods = new String[concreteComponents.length];

        for (int i = 0; i < visitMethods.length; i++) {
            String className = concreteComponents[i].getName();
            visitMethods[i] = String.format(
                    provideTemplateContent(METHOD_VISIT_IMPLEMENTATION_PATH),
                    className,
                    className,
                    toFirstLetterLowerCase(className));
        }

        String allMethods = String.join("\n", visitMethods);

        String concreteVisitorClassName = CONCRETE_VISITOR_NAME.substring(0, CONCRETE_VISITOR_NAME.indexOf('.'));
        //CONCRETE_VISITOR_NAME.split(".")[0];
        generatePsiClass(CONCRETE_VISITOR_TEMPLATE_PATH, CONCRETE_VISITOR_NAME, concreteVisitorClassName, allMethods);
    }

    private PsiClass generatePsiClass(String templateName, String fileName, String... parameters) {
        String absolutePath = concreteComponents[0].getContainingFile().getContainingDirectory() + "/" + fileName;
        String absolutePath1 = concreteComponents[0].getContainingFile().getContainingDirectory().getVirtualFile().getPath() + "/" + fileName;
        String text = String.format(provideTemplateContent(templateName), parameters);
        final PsiFileFactory factory = PsiFileFactory.getInstance(psiClass.getProject());

        File f = new File(absolutePath1);

        if (f.exists()) {
            PsiFile psiFile = psiClass.getContainingFile().getContainingDirectory().findFile(fileName);
            psiFile.delete();
            f.delete();
        }

        final PsiFile file = factory.createFileFromText(absolutePath, StdFileTypes.JAVA, text);

        PsiJavaFile psiJavaFile = (PsiJavaFile) file;
        PsiClass componentPsiClass = psiJavaFile.getClasses()[0];
        psiClass.getContainingFile().getContainingDirectory().add(componentPsiClass);

        return componentPsiClass;
    }

    private void createPsiClasses(Project project, VirtualFile[] components) {
        concreteComponents = new PsiClass[components.length];

        for (int i = 0; i < components.length; ++i) {
            VirtualFile v = components[i];
            PsiFile curFile = PsiManager.getInstance(project).findFile(v);
            PsiJavaFile psiJavaFile = (PsiJavaFile) curFile;

            concreteComponents[i] = psiJavaFile.getClasses()[0];
        }
    }

    private void addAcceptMethod(PsiClass psiClass) {
        String acceptMethodContent = String.format(provideTemplateContent(METHOD_ACCEPT), psiClass.getName());
        PsiMethod acceptMethod = JavaPsiFacade.getElementFactory(psiClass.getProject()).createMethodFromText(acceptMethodContent, psiClass);
        PsiModifierWrapper.PUBLIC.applyModifier(acceptMethod);
        psiClass.add(acceptMethod);
    }
}
