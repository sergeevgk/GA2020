package com.spbstu.virtvisualization.grammar.model;

import com.spbstu.virtvisualization.grammar.diagram.Element;
import com.spbstu.virtvisualization.grammar.diagram.Text;
import com.spbstu.virtvisualization.grammar.diagram.Text.Type;


public class SpecialSequence extends Expression {

  private String text;

  public SpecialSequence(String text) {
    this.text = text;
  }

  @Override
  protected Element toRRElement(GrammarToDiagram grammarToDiagram) {
    return new Text(Type.SPECIAL_SEQUENCE, text, null);
  }

  @Override
  protected void toBNF(GrammarToBNF grammarToBNF, StringBuilder sb, boolean isNested) {
    sb.append("(? ");
    sb.append(text);
    sb.append(" ?)");
  }

  @Override
  public boolean equals(Object o) {
    if(!(o instanceof SpecialSequence)) {
      return false;
    }
    return text.equals(((SpecialSequence)o).text);
  }

}
