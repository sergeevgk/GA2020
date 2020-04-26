package com.spbstu.virtvisualization.grammar.diagram;


public class Break extends Element {

  @Override
  protected void computeLayoutInfo(DiagramToSVG diagramToSVG) {
    throw new IllegalStateException("This element must not be nested and should have been processed before entering generation.");
  }

  @Override
  protected void toSVG(DiagramToSVG diagramToSVG, int xOffset, int yOffset, Diagram.SvgContent svgContent) {
    throw new IllegalStateException("This element must not be nested and should have been processed before entering generation.");
  }

}
