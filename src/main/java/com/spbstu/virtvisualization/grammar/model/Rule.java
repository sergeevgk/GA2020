package com.spbstu.virtvisualization.grammar.model;

import com.spbstu.virtvisualization.grammar.diagram.Diagram;


public class Rule {

  private String name;
  private Expression expression;
  private String originalExpressionText;

  public Rule(String name, Expression expression) {
    this(name, expression, null);
  }

  public Rule(String name, Expression expression, String originalExpressionText) {
    this.name = name;
    this.expression = expression;
    this.originalExpressionText = originalExpressionText;
  }

  public String getName() {
    return name;
  }

  public String getOriginalExpressionText() {
    return originalExpressionText;
  }

  Diagram toRRDiagram(GrammarToDiagram grammarToDiagram) {
    return new Diagram(expression.toRRElement(grammarToDiagram));
  }

  String toBNF(GrammarToBNF grammarToBNF) {
    StringBuilder sb = new StringBuilder();
    sb.append(name);
    sb.append(" ");
    switch(grammarToBNF.getRuleDefinitionSign()) {
      case EQUAL: sb.append("="); break;
      case COLON_EQUAL: sb.append(":="); break;
      case COLON_COLON_EQUAL: sb.append("::="); break;
    }
    sb.append(" ");
    expression.toBNF(grammarToBNF, sb, false);
    sb.append(";");
    return sb.toString();
  }

  @Override
  public String toString() {
    return toBNF(new GrammarToBNF());
  }
}
