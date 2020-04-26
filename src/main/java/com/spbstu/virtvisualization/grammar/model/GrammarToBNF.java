
package com.spbstu.virtvisualization.grammar.model;

public class GrammarToBNF {

  public static enum RuleDefinitionSign {
    EQUAL,
    COLON_EQUAL,
    COLON_COLON_EQUAL,
  }

  private RuleDefinitionSign ruleDefinitionSign = RuleDefinitionSign.EQUAL;

  public RuleDefinitionSign getRuleDefinitionSign() {
    return ruleDefinitionSign;
  }

  public void setRuleDefinitionSign(RuleDefinitionSign ruleDefinitionSign) {
    this.ruleDefinitionSign = ruleDefinitionSign;
  }

  public static enum LiteralDefinitionSign {
    QUOTE,
    DOUBLE_QUOTE,
  }

  private LiteralDefinitionSign literalDefinitionSign = LiteralDefinitionSign.QUOTE;

  public LiteralDefinitionSign getLiteralDefinitionSign() {
    return literalDefinitionSign;
  }

  public void setLiteralDefinitionSign(LiteralDefinitionSign literalDefinitionSign) {
    this.literalDefinitionSign = literalDefinitionSign;
  }

  private boolean isCommaSeparator;

  public void setCommaSeparator(boolean isCommaSeparator) {
    this.isCommaSeparator = isCommaSeparator;
  }

  public boolean isCommaSeparator() {
    return isCommaSeparator;
  }

  private boolean isUsingMultiplicationTokens;

  public void setUsingMultiplicationTokens(boolean isUsingMultiplicationTokens) {
    this.isUsingMultiplicationTokens = isUsingMultiplicationTokens;
  }

  public boolean isUsingMultiplicationTokens() {
    return isUsingMultiplicationTokens;
  }

  private String ruleConsideredAsLineBreak;

  public void setRuleConsideredAsLineBreak(String ruleConsideredAsLineBreak) {
    this.ruleConsideredAsLineBreak = ruleConsideredAsLineBreak;
  }

  public String getRuleConsideredAsLineBreak() {
    return ruleConsideredAsLineBreak;
  }

  public String convert(Grammar grammar) {
    return grammar.toBNF(this);
  }

}
