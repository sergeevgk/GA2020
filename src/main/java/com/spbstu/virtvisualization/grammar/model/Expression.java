package com.spbstu.virtvisualization.grammar.model;

import com.spbstu.virtvisualization.grammar.diagram.Element;


public abstract class Expression {

  protected abstract Element toRRElement(GrammarToDiagram grammarToDiagram);

  protected abstract void toBNF(GrammarToBNF grammarToBNF, StringBuilder sb, boolean isNested);

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    toBNF(new GrammarToBNF(), sb, false);
    return sb.toString();
  }
}
