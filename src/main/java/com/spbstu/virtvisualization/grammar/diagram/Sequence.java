package com.spbstu.virtvisualization.grammar.diagram;

import com.spbstu.virtvisualization.grammar.diagram.Diagram.SvgContent;


public class Sequence extends Element {

  private Element[] elements;

  public Sequence(Element... elements) {
    this.elements = elements;
  }

  public Element[] getRRElements() {
    return elements;
  }

  @Override
  protected void computeLayoutInfo(DiagramToSVG diagramToSVG) {
    int width = 0;
    int aboveConnector = 0;
    int belowConnector = 0;
    for (int i = 0; i < elements.length; i++) {
      Element element = elements[i];
      element.computeLayoutInfo(diagramToSVG);
      if(i > 0) {
        width += 10;
      }
      LayoutInfo layoutInfo = element.getLayoutInfo();
      width += layoutInfo.getWidth();
      int height = layoutInfo.getHeight();
      int connectorOffset = layoutInfo.getConnectorOffset();
      aboveConnector = Math.max(aboveConnector, connectorOffset);
      belowConnector = Math.max(belowConnector, height - connectorOffset);
    }
    setLayoutInfo(new LayoutInfo(width, aboveConnector + belowConnector, aboveConnector));
  }

  @Override
  protected void toSVG(DiagramToSVG diagramToSVG, int xOffset, int yOffset, SvgContent svgContent) {
    LayoutInfo layoutInfo = getLayoutInfo();
    int connectorOffset = layoutInfo.getConnectorOffset();
    int widthOffset = 0;
    for (int i = 0; i < elements.length; i++) {
      Element element = elements[i];
      LayoutInfo layoutInfo2 = element.getLayoutInfo();
      int width2 = layoutInfo2.getWidth();
      int connectorOffset2 = layoutInfo2.getConnectorOffset();
      int xOffset2 = widthOffset + xOffset;
      int yOffset2 = yOffset + connectorOffset - connectorOffset2;
      if(i > 0) {
        svgContent.addLineConnector(xOffset2 - 10, yOffset + connectorOffset, xOffset2, yOffset + connectorOffset);
      }
      element.toSVG(diagramToSVG, xOffset2, yOffset2, svgContent);
      widthOffset += 10;
      widthOffset += width2;
    }
  }

}
