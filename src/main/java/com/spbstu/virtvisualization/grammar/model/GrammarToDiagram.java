package com.spbstu.virtvisualization.grammar.model;

import com.spbstu.virtvisualization.grammar.diagram.Diagram;

public class GrammarToDiagram {

  public static interface RuleLinkProvider {
    public String getLink(String ruleName);
  }

  private RuleLinkProvider ruleLinkProvider = new RuleLinkProvider() {
    @Override
    public String getLink(String ruleName) {
      return "#" + ruleName;
    }
  };

  public void setRuleLinkProvider(RuleLinkProvider ruleLinkProvider) {
    this.ruleLinkProvider = ruleLinkProvider;
  }

  public RuleLinkProvider getRuleLinkProvider() {
    return ruleLinkProvider;
  }

  private String ruleConsideredAsLineBreak;

  public void setRuleConsideredAsLineBreak(String ruleConsideredAsLineBreak) {
    this.ruleConsideredAsLineBreak = ruleConsideredAsLineBreak;
  }

  public String getRuleConsideredAsLineBreak() {
    return ruleConsideredAsLineBreak;
  }

  public Diagram convert(Rule rule) {
    return rule.toRRDiagram(this);
  }

}
