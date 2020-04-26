package com.spbstu.virtvisualization.grammar.model;

import com.spbstu.virtvisualization.grammar.model.GrammarToBNF.LiteralDefinitionSign;
import com.spbstu.virtvisualization.grammar.diagram.Element;
import com.spbstu.virtvisualization.grammar.diagram.Text;
import com.spbstu.virtvisualization.grammar.diagram.Text.Type;


public class Literal extends Expression {

  private String text;

  public Literal(String text) {
    this.text = text;
  }

  @Override
  protected Element toRRElement(GrammarToDiagram grammarToDiagram) {
    return new Text(Type.LITERAL, text, null);
  }

  @Override
  protected void toBNF(GrammarToBNF grammarToBNF, StringBuilder sb, boolean isNested) {
    char c = grammarToBNF.getLiteralDefinitionSign() == LiteralDefinitionSign.DOUBLE_QUOTE? '"': '\'';
    sb.append(c);
    sb.append(text);
    sb.append(c);
  }

  @Override
  public boolean equals(Object o) {
    if(!(o instanceof Literal)) {
      return false;
    }
    return text.equals(((Literal)o).text);
  }

}
