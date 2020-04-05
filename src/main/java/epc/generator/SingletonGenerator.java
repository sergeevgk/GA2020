package epc.generator;

import com.intellij.psi.*;
import epc.utils.PsiModifierWrapper;
import epc.utils.PsiMembersUtils;
import epc.utils.StringUtils;
import epc.utils.TemplateProvider;

import java.util.Arrays;
import java.util.Collections;
import java.util.Objects;

public class SingletonGenerator extends Generator implements TemplateProvider {

    private static final String INSTANCE_METHOD_TEMPLATE_PATH = "/templates/instance-method";

    private static final String INSTANCE_FIELD_SUFFIX = "Instance";
    private static final String INSTANCE_METHOD_NAME = String.format("get%s", INSTANCE_FIELD_SUFFIX);

    public SingletonGenerator(PsiClass psiClass) {
        super(psiClass);
    }

    @Override
    public void generateJavaClass() {
        String instanceFieldName = StringUtils
                .toFirstLetterLowerCase(
                        Objects.requireNonNull(psiClass.getName())
                                .concat(INSTANCE_FIELD_SUFFIX)
                );
        deleteRelated(psiClass, instanceFieldName);
        psiClass.add(generatePrivateConstructor(psiClass));
        psiClass.add(generateInstanceField(psiClass, instanceFieldName));
        psiClass.add(generateInstanceMethod(psiClass, instanceFieldName));
    }

    private void deleteRelated(PsiClass psiClass, String instanceFieldName) {
        Arrays.stream(psiClass.getConstructors())
                .forEach(PsiMember::delete);
        Arrays.stream(psiClass.getFields())
                .filter(member -> member.getName() != null && member.getName().equals(instanceFieldName))
                .forEach(PsiMember::delete);
        Arrays.stream(psiClass.getMethods())
                .filter(member -> member.getName().equals(INSTANCE_METHOD_NAME))
                .forEach(PsiMember::delete);
    }

    private PsiElement generatePrivateConstructor(PsiClass psiClass) {
        PsiMethod constructor = PsiMembersUtils.generateConstructorForClass(psiClass, Collections.emptyList());
        PsiModifierWrapper.PRIVATE.applyModifier(constructor);
        return constructor;
    }

    private PsiField generateInstanceField(PsiClass psiClass, String instanceFieldName) {
        PsiField instanceField = JavaPsiFacade.getElementFactory(psiClass.getProject()).createField(instanceFieldName, JavaPsiFacade.getInstance(psiClass.getProject()).getElementFactory().createType(psiClass));
        PsiModifierWrapper.PRIVATE_STATIC.applyModifier(instanceField);
        return instanceField;
    }

    private PsiMethod generateInstanceMethod(PsiClass psiClass, String instanceFieldName) {
        String instanceMethodContent = String.format(provideTemplateContent(INSTANCE_METHOD_TEMPLATE_PATH), psiClass.getName(), INSTANCE_METHOD_NAME, instanceFieldName, instanceFieldName, psiClass.getName(), instanceFieldName);
        PsiMethod instanceMethod = JavaPsiFacade.getElementFactory(psiClass.getProject()).createMethodFromText(instanceMethodContent, psiClass);
        PsiModifierWrapper.PUBLIC_STATIC_SYNCHRONIZED.applyModifier(instanceMethod);
        return instanceMethod;
    }
}
