package com.spbstu.virtvisualization.grammar.model;

import com.spbstu.virtvisualization.grammar.model.GrammarToDiagram.RuleLinkProvider;
import com.spbstu.virtvisualization.grammar.diagram.Break;
import com.spbstu.virtvisualization.grammar.diagram.Element;
import com.spbstu.virtvisualization.grammar.diagram.Text;
import com.spbstu.virtvisualization.grammar.diagram.Text.Type;


public class RuleReference extends Expression {

  private String ruleName;

  public RuleReference(String ruleName) {
    this.ruleName = ruleName;
  }

  public String getRuleName() {
    return ruleName;
  }

  @Override
  protected Element toRRElement(GrammarToDiagram grammarToDiagram) {
    String ruleConsideredAsLineBreak = grammarToDiagram.getRuleConsideredAsLineBreak();
    if(ruleConsideredAsLineBreak != null && ruleConsideredAsLineBreak.equals(ruleName)) {
      return new Break();
    }
    RuleLinkProvider ruleLinkProvider = grammarToDiagram.getRuleLinkProvider();
    return new Text(Type.RULE, ruleName, ruleLinkProvider == null? null: ruleLinkProvider.getLink(ruleName));
  }

  @Override
  protected void toBNF(GrammarToBNF grammarToBNF, StringBuilder sb, boolean isNested) {
    sb.append(ruleName);
    String ruleConsideredAsLineBreak = grammarToBNF.getRuleConsideredAsLineBreak();
    if(ruleConsideredAsLineBreak != null && ruleConsideredAsLineBreak.equals(ruleName)) {
      sb.append("\n");
    }
  }

  @Override
  public boolean equals(Object o) {
    if(!(o instanceof RuleReference)) {
      return false;
    }
    return ruleName.equals(((RuleReference)o).ruleName);
  }

}
