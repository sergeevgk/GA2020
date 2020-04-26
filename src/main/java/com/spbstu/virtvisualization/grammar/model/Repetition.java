package com.spbstu.virtvisualization.grammar.model;

import com.spbstu.virtvisualization.grammar.diagram.Choice;
import com.spbstu.virtvisualization.grammar.diagram.Element;
import com.spbstu.virtvisualization.grammar.diagram.Line;
import com.spbstu.virtvisualization.grammar.diagram.Loop;


public class Repetition extends Expression {

  private Expression expression;
  private int minRepetitionCount;
  private Integer maxRepetitionCount;

  public Repetition(Expression expression, int minRepetitionCount, Integer maxRepetitionCount) {
    this.expression = expression;
    this.minRepetitionCount = minRepetitionCount;
    this.maxRepetitionCount = maxRepetitionCount;
  }

  public Expression getExpression() {
    return expression;
  }

  public int getMinRepetitionCount() {
    return minRepetitionCount;
  }

  public Integer getMaxRepetitionCount() {
    return maxRepetitionCount;
  }

  @Override
  protected Element toRRElement(GrammarToDiagram grammarToDiagram) {
    Element element = expression.toRRElement(grammarToDiagram);
    if(minRepetitionCount == 0) {
      if(maxRepetitionCount == null || maxRepetitionCount > 1) {
        return new Choice(new Loop(element, null, 0, (maxRepetitionCount == null? null: maxRepetitionCount - 1)), new Line());
      }
      return new Choice(element, new Line());
    }
    return new Loop(element, null, minRepetitionCount - 1, (maxRepetitionCount == null? null: maxRepetitionCount - 1));
  }

  @Override
  protected void toBNF(GrammarToBNF grammarToBNF, StringBuilder sb, boolean isNested) {
    boolean isUsingMultiplicationTokens = grammarToBNF.isUsingMultiplicationTokens();
    if(maxRepetitionCount == null) {
      if(minRepetitionCount > 0) {
        if(minRepetitionCount == 1 && isUsingMultiplicationTokens) {
          expression.toBNF(grammarToBNF, sb, true);
          sb.append("+");
        } else {
          if(isNested) {
            sb.append("( ");
          }
          if(minRepetitionCount > 1) {
            sb.append(minRepetitionCount);
            sb.append(" * ");
          }
          expression.toBNF(grammarToBNF, sb, false);
          if(grammarToBNF.isCommaSeparator()) {
            sb.append(" ,");
          }
          sb.append(" ");
          sb.append("{ ");
          expression.toBNF(grammarToBNF, sb, false);
          sb.append(" }");
          if(isNested) {
            sb.append(" )");
          }
        }
      } else {
        if(isUsingMultiplicationTokens) {
          expression.toBNF(grammarToBNF, sb, true);
          sb.append("*");
        } else {
          sb.append("{ ");
          expression.toBNF(grammarToBNF, sb, false);
          sb.append(" }");
        }
      }
    } else {
      if(minRepetitionCount == 0) {
        if(maxRepetitionCount == 1 && isUsingMultiplicationTokens) {
          expression.toBNF(grammarToBNF, sb, true);
          sb.append("?");
        } else {
          if(maxRepetitionCount > 1) {
            sb.append(maxRepetitionCount);
            sb.append(" * ");
          }
          sb.append("[ ");
          expression.toBNF(grammarToBNF, sb, false);
          sb.append(" ]");
        }
      } else {
        if(minRepetitionCount == maxRepetitionCount) {
          sb.append(minRepetitionCount);
          sb.append(" * ");
          expression.toBNF(grammarToBNF, sb, isNested);
        } else {
          if(isNested) {
            sb.append("( ");
          }
          sb.append(minRepetitionCount);
          sb.append(" * ");
          expression.toBNF(grammarToBNF, sb, false);
          if(grammarToBNF.isCommaSeparator()) {
            sb.append(" ,");
          }
          sb.append(" ");
          sb.append(maxRepetitionCount - minRepetitionCount);
          sb.append(" * ");
          sb.append("[ ");
          expression.toBNF(grammarToBNF, sb, false);
          sb.append(" ]");
          if(isNested) {
            sb.append(" )");
          }
        }
      }
    }
  }

  @Override
  public boolean equals(Object o) {
    if(!(o instanceof Repetition)) {
      return false;
    }
    Repetition exp2 = (Repetition)o;
    return expression.equals(exp2.expression) && minRepetitionCount == exp2.minRepetitionCount && maxRepetitionCount == null? exp2.maxRepetitionCount == null: maxRepetitionCount.equals(exp2.maxRepetitionCount);
  }

}
