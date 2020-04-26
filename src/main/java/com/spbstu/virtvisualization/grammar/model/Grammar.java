package com.spbstu.virtvisualization.grammar.model;


public class Grammar {

  private Rule[] rules;

  public Grammar(Rule... rules) {
    this.rules = rules;
  }

  public Rule[] getRules() {
    return rules;
  }

  String toBNF(GrammarToBNF grammarToBNF) {
    StringBuilder sb = new StringBuilder();
    for(int i=0; i<rules.length; i++) {
      if(i > 0) {
        sb.append("\n");
      }
      sb.append(rules[i].toBNF(grammarToBNF));
    }
    return sb.toString();
  }

  @Override
  public String toString() {
    return toBNF(new GrammarToBNF());
  }
}
