package epc.generator;

import com.intellij.psi.*;
import epc.utils.PsiClassUtils;
import epc.utils.PsiModifierWrapper;
import epc.utils.PsiMembersUtils;
import epc.utils.TemplateProvider;
import org.jetbrains.annotations.NotNull;

import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

import static epc.utils.StringUtils.toFirstLetterLowerCase;
import static epc.utils.StringUtils.toFirstLetterUpperCase;

public class BuilderGenerator extends Generator implements TemplateProvider {

    private static final String BUILDER_CLASS_NAME_SUFFIX = "Builder";

    private static final String BUILDER_ACCESS_METHOD_TEMPLATE = "/templates/builder-access-method";
    private static final String BUILDER_BUILD_METHOD_TEMPLATE = "/templates/build-method";
    private static final String BUILDER_WITH_METHOD_TEMPLATE = "/templates/builder-with-method";

    private static final String BUILDER_BUILD_METHOD_SET_TEMPLATE = "%s.set%s(%s);";

    private List<PsiField> includedFields;
    private List<PsiField> mandatoryFields;
    private String builderClassName;

    public BuilderGenerator(@NotNull PsiClass psiClass, List<PsiField> includedFields, List<PsiField> mandatoryFields) {
        super(psiClass);
        this.includedFields = includedFields;
        this.mandatoryFields = mandatoryFields;
        this.builderClassName = Objects.requireNonNull(psiClass.getName()).concat(BUILDER_CLASS_NAME_SUFFIX);
    }


    @Override
    public void generateJavaClass() {
        prepareParentClass();
        PsiClass innerBuilderClass = generateStuffForBuilderClass();
        psiClass.add(innerBuilderClass);
       // getJavaCodeStyleManager().shortenClassReferences(psiClass);
    }

    private void prepareParentClass() {
        PsiMethod constructor = generateConstructorForParentClass();
        List<PsiMethod> gettersAndSetters = generateGettersAndSettersForParentClass();
        deleteRelated(gettersAndSetters);
        includedFields.forEach(PsiModifierWrapper.PRIVATE::applyModifier);
        psiClass.add(constructor);
        gettersAndSetters.forEach(psiClass::add);
    }

    private PsiMethod generateConstructorForParentClass() {
        PsiMethod constructorForParentClass = PsiMembersUtils.generateConstructorForClass(psiClass, mandatoryFields);
        PsiModifierWrapper.PRIVATE.applyModifier(constructorForParentClass);
        return constructorForParentClass;
    }

    private List<PsiMethod> generateGettersAndSettersForParentClass() {
        List<PsiMethod> gettersAndSetters = PsiMembersUtils.generateGettersAndSettersForClass(includedFields, psiClass);
        gettersAndSetters.forEach(PsiModifierWrapper.PUBLIC::applyModifier);
        return gettersAndSetters;
    }

    private void deleteRelated(List<PsiMethod> gettersAndSetters) {
        Arrays.stream(psiClass.getInnerClasses())
                .filter(innerClass -> innerClass.getName() != null && innerClass.getName().equals(builderClassName))
                .forEach(PsiMember::delete);
        Arrays.stream(psiClass.getConstructors())
                .forEach(PsiMember::delete);
        List<String> gettersAndSettersNames = gettersAndSetters.stream().map(PsiMethod::getName).collect(Collectors.toList());
        Arrays.stream(psiClass.getMethods())
                .filter(parentClassMethod -> gettersAndSettersNames.contains(parentClassMethod.getName()))
                .forEach(PsiMethod::delete);
    }

    private PsiClass generateStuffForBuilderClass() {
        PsiClass builderClass = generateBuilderClass();
        generateBuilderFields().forEach(builderClass::add);
        builderClass.add(generateBuilderConstructor(builderClass));
        builderClass.add(generateBuilderAccessMethod());
        List<PsiField> includedFieldsWithoutMandatoryFields = includedFields.stream().filter(includedField -> !mandatoryFields.contains(includedField)).collect(Collectors.toList());
        generateBuilderWithMethods(builderClass, includedFieldsWithoutMandatoryFields).forEach(builderClass::add);
        builderClass.add(generateBuildMethod(builderClass, includedFieldsWithoutMandatoryFields));
        return builderClass;
    }

    private PsiClass generateBuilderClass() {
        PsiClass builderClass = PsiClassUtils.generateClassForProjectWithName(psiClass.getProject(), builderClassName);
        PsiModifierWrapper.PUBLIC_STATIC.applyModifier(builderClass);
        return builderClass;
    }

    private List<PsiField> generateBuilderFields() {
        List<PsiField> builderFields = includedFields.stream()
                .map(includedField -> JavaPsiFacade.getElementFactory(psiClass.getProject()).createField(Objects.requireNonNull(includedField.getName()), includedField.getType()))
                .collect(Collectors.toList());
        builderFields.forEach(PsiModifierWrapper.PRIVATE::applyModifier);
        return builderFields;
    }

    private PsiMethod generateBuilderConstructor(PsiClass builderClass) {
        PsiMethod builderConstructor = PsiMembersUtils.generateConstructorForClass(builderClass, mandatoryFields);
        PsiModifierWrapper.PRIVATE.applyModifier(builderConstructor);
        return builderConstructor;
    }

    private PsiMethod generateBuilderAccessMethod() {
        String argumentsWithTypes = PsiMembersUtils.generateArgumentsWithTypesFromFields(mandatoryFields);
        String argumentsWithoutTypes = PsiMembersUtils.generateArgumentsWithoutTypesFromFields(mandatoryFields);
        String builderAccessMethodContent = String.format(provideTemplateContent(BUILDER_ACCESS_METHOD_TEMPLATE), builderClassName, psiClass.getName(), argumentsWithTypes, builderClassName, argumentsWithoutTypes);
        PsiMethod builderAccessMethod = JavaPsiFacade.getElementFactory(psiClass.getProject()).createMethodFromText(builderAccessMethodContent, psiClass);
        PsiModifierWrapper.PUBLIC_STATIC.applyModifier(builderAccessMethod);
        return builderAccessMethod;
    }

    private PsiMethod generateBuildMethod(PsiClass builderClass, List<PsiField> includedFieldsWithoutMandatoryFields) {
        String parentClassName = Objects.requireNonNull(psiClass.getName());
        String lowercaseParentClassName = toFirstLetterLowerCase(parentClassName);
        String argumentsWithoutTypes = PsiMembersUtils.generateArgumentsWithoutTypesFromFields(mandatoryFields);
        String setters = includedFieldsWithoutMandatoryFields.stream()
                .map(psiField -> String.format(BUILDER_BUILD_METHOD_SET_TEMPLATE, lowercaseParentClassName,
                        toFirstLetterUpperCase(Objects.requireNonNull(psiField.getName())),
                        toFirstLetterLowerCase(Objects.requireNonNull(psiField.getName()))))
                .collect(Collectors.joining("\n"));
        String buildMethodContent = String.format(provideTemplateContent(BUILDER_BUILD_METHOD_TEMPLATE),
                parentClassName, parentClassName, lowercaseParentClassName, parentClassName, argumentsWithoutTypes, setters, lowercaseParentClassName);
        PsiMethod builderMethod = JavaPsiFacade.getElementFactory(psiClass.getProject()).createMethodFromText(buildMethodContent, builderClass);
        PsiModifierWrapper.PUBLIC.applyModifier(builderMethod);
        return builderMethod;
    }

    private List<PsiMethod> generateBuilderWithMethods(PsiClass builderClass, List<PsiField> withFields) {
        return withFields.stream()
                .map(psiField -> {
                    String upperName = toFirstLetterUpperCase(Objects.requireNonNull(psiField.getName()));
                    String name = psiField.getName();
                    String type = psiField.getType().getCanonicalText();
                    String content = String.format(provideTemplateContent(BUILDER_WITH_METHOD_TEMPLATE), builderClassName, upperName, type, name, name, name);
                    return JavaPsiFacade.getElementFactory(psiClass.getProject()).createMethodFromText(content, builderClass);
                })
                .peek(PsiModifierWrapper.PUBLIC::applyModifier)
                .collect(Collectors.toList());
    }
}
