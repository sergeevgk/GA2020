package com.spbstu.virtvisualization.grammar.diagram;

import com.spbstu.virtvisualization.grammar.diagram.Diagram.SvgContent;


public class Line extends Element {

  @Override
  protected void computeLayoutInfo(DiagramToSVG diagramToSVG) {
    setLayoutInfo(new LayoutInfo(0, 10, 5));
  }

  @Override
  protected void toSVG(DiagramToSVG diagramToSVG, int xOffset, int yOffset, SvgContent svgContent) {
  }

}
