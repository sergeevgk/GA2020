package com.spbstu.virtvisualization.grammar.model;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.spbstu.virtvisualization.grammar.diagram.Element;


public class Choice extends Expression {

  private Expression[] expressions;

  public Choice(Expression... expressions) {
    this.expressions = expressions;
  }

  public Expression[] getExpressions() {
    return expressions;
  }

  @Override
  protected Element toRRElement(GrammarToDiagram grammarToDiagram) {
    Element[] elements = new Element[expressions.length];
    for(int i = 0; i< elements.length; i++) {
      elements[i] = expressions[i].toRRElement(grammarToDiagram);
    }
    return new com.spbstu.virtvisualization.grammar.diagram.Choice(elements);
  }

  @Override
  protected void toBNF(GrammarToBNF grammarToBNF, StringBuilder sb, boolean isNested) {
    List<Expression> expressionList = new ArrayList<Expression>();
    boolean hasNoop = false;
    for(Expression expression: expressions) {
      if(expression instanceof Sequence && ((Sequence)expression).getExpressions().length == 0) {
        hasNoop = true;
      } else {
        expressionList.add(expression);
      }
    }
    if(expressionList.isEmpty()) {
      sb.append("( )");
    } else if(hasNoop && expressionList.size() == 1) {
      boolean isUsingMultiplicationTokens = grammarToBNF.isUsingMultiplicationTokens();
      if(!isUsingMultiplicationTokens) {
        sb.append("[ ");
      }
      expressionList.get(0).toBNF(grammarToBNF, sb, isUsingMultiplicationTokens);
      if(!isUsingMultiplicationTokens) {
        sb.append(" ]");
      }
    } else {
      boolean isUsingMultiplicationTokens = grammarToBNF.isUsingMultiplicationTokens();
      if(hasNoop && !isUsingMultiplicationTokens) {
        sb.append("[ ");
      } else if(hasNoop || isNested && expressionList.size() > 1) {
        sb.append("( ");
      }
      int count = expressionList.size();
      for(int i=0; i<count; i++) {
        if(i > 0) {
          sb.append(" | ");
        }
        expressionList.get(i).toBNF(grammarToBNF, sb, false);
      }
      if(hasNoop && !isUsingMultiplicationTokens) {
        sb.append(" ]");
      } else if(hasNoop || isNested && expressionList.size() > 1) {
        sb.append(" )");
        if(hasNoop) {
          sb.append("?");
        }
      }
    }
  }

  @Override
  public boolean equals(Object o) {
    if(!(o instanceof Choice)) {
      return false;
    }
    return Arrays.equals(expressions, ((Choice)o).expressions);
  }

}
