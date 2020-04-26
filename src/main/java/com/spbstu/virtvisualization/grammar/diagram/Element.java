package com.spbstu.virtvisualization.grammar.diagram;

import com.spbstu.virtvisualization.grammar.diagram.Diagram.SvgContent;


public abstract class Element {

  protected static class LayoutInfo {

    private int width;
    private int height;
    private int connectorOffset;

    public LayoutInfo(int width, int height, int connectorOffset) {
      this.width = width;
      this.height = height;
      this.connectorOffset = connectorOffset;
    }

    public int getWidth() {
      return width;
    }

    public int getHeight() {
      return height;
    }

    public int getConnectorOffset() {
      return connectorOffset;
    }

  }

  private LayoutInfo layoutInfo;

  public void setLayoutInfo(LayoutInfo layoutInfo) {
    this.layoutInfo = layoutInfo;
  }

  public LayoutInfo getLayoutInfo() {
    return layoutInfo;
  }

  protected abstract void computeLayoutInfo(DiagramToSVG diagramToSVG);

  protected abstract void toSVG(DiagramToSVG diagramToSVG, int xOffset, int yOffset, SvgContent svgContent);

}
