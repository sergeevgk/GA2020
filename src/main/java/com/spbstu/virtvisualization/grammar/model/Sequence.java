package com.spbstu.virtvisualization.grammar.model;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.spbstu.virtvisualization.grammar.diagram.Element;
import com.spbstu.virtvisualization.grammar.diagram.Loop;


public class Sequence extends Expression {

  private Expression[] expressions;

  public Sequence(Expression... expressions) {
    this.expressions = expressions;
  }

  public Expression[] getExpressions() {
    return expressions;
  }

  @Override
  protected Element toRRElement(GrammarToDiagram grammarToDiagram) {
    List<Element> elementList = new ArrayList<Element>();
    for(int i=0; i<expressions.length; i++) {
      Expression expression = expressions[i];
      Element element = expression.toRRElement(grammarToDiagram);
      // Treat special case of: "a (',' a)*" and "a (a)*"
      if(i < expressions.length - 1 && expressions[i + 1] instanceof Repetition) {
        Repetition repetition = (Repetition)expressions[i + 1];
        Expression repetitionExpression = repetition.getExpression();
        if(repetitionExpression instanceof Sequence) {
          // Treat special case of: "expr (',' expr)*"
          Expression[] subExpressions = ((Sequence)repetitionExpression).getExpressions();
          if(subExpressions.length == 2 && subExpressions[0] instanceof Literal) {
            if(expression.equals(subExpressions[1])) {
              Integer maxRepetitionCount = repetition.getMaxRepetitionCount();
              if(maxRepetitionCount == null || maxRepetitionCount > 1) {
                element = new Loop(expression.toRRElement(grammarToDiagram), subExpressions[0].toRRElement(grammarToDiagram), repetition.getMinRepetitionCount(), (maxRepetitionCount == null? null: maxRepetitionCount));
                i++;
              }
            }
          }
        } else if(expression instanceof RuleReference) {
          RuleReference ruleLink = (RuleReference)expression;
          // Treat special case of: a (a)*
          if(repetitionExpression instanceof RuleReference && ((RuleReference)repetitionExpression).getRuleName().equals(ruleLink.getRuleName())) {
            Integer maxRepetitionCount = repetition.getMaxRepetitionCount();
            if(maxRepetitionCount == null || maxRepetitionCount > 1) {
              element = new Loop(ruleLink.toRRElement(grammarToDiagram), null, repetition.getMinRepetitionCount(), (maxRepetitionCount == null? null: maxRepetitionCount));
              i++;
            }
          }
        }
      }
      elementList.add(element);
    }
    return new com.spbstu.virtvisualization.grammar.diagram.Sequence(elementList.toArray(new Element[0]));
  }

  @Override
  protected void toBNF(GrammarToBNF grammarToBNF, StringBuilder sb, boolean isNested) {
    if(expressions.length == 0) {
      sb.append("( )");
      return;
    }
    if(isNested && expressions.length > 1) {
      sb.append("( ");
    }
    boolean isCommaSeparator = grammarToBNF.isCommaSeparator();
    for(int i=0; i<expressions.length; i++) {
      if(i > 0) {
        if(isCommaSeparator) {
          sb.append(" ,");
        }
        sb.append(" ");
      }
      expressions[i].toBNF(grammarToBNF, sb, expressions.length == 1 && isNested || !isCommaSeparator);
    }
    if(isNested && expressions.length > 1) {
      sb.append(" )");
    }
  }

  @Override
  public boolean equals(Object o) {
    if(!(o instanceof Sequence)) {
      return false;
    }
    return Arrays.equals(expressions, ((Sequence)o).expressions);
  }

}
