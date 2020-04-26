package com.spbstu.virtvisualization.grammar.diagram;

import java.awt.Font;
import java.awt.Insets;
import java.awt.font.FontRenderContext;
import java.awt.font.LineMetrics;
import java.awt.geom.Rectangle2D;

import com.spbstu.virtvisualization.common.Utils;
import com.spbstu.virtvisualization.grammar.diagram.Diagram.SvgContent;
import com.spbstu.virtvisualization.grammar.diagram.DiagramToSVG.BoxShape;


public class Text extends Element {

  public static enum Type {
    LITERAL,
    RULE,
    SPECIAL_SEQUENCE,
  }

  private Type type;
  private String text;
  private String link;

  public Text(Type type, String text, String link) {
    this.type = type;
    this.text = text;
    this.link = link;
  }

  public Type getType() {
    return type;
  }

  public String getText() {
    return text;
  }

  public String getLink() {
    return link;
  }

  private int fontYOffset;

  @Override
  protected void computeLayoutInfo(DiagramToSVG diagramToSVG) {
    FontRenderContext fontRenderContext = new FontRenderContext(null, true, false);
    Font font;
    Insets insets;
    switch(type) {
      case RULE:
        insets = diagramToSVG.getRuleInsets();
        font = diagramToSVG.getRuleFont();
        break;
      case LITERAL:
        insets = diagramToSVG.getLiteralInsets();
        font = diagramToSVG.getLiteralFont();
        break;
      case SPECIAL_SEQUENCE:
        insets = diagramToSVG.getSpecialSequenceInsets();
        font = diagramToSVG.getSpecialSequenceFont();
        break;
      default: throw new IllegalStateException("Unknown type: " + type);
    }
    LineMetrics lineMetrics = font.getLineMetrics(text, fontRenderContext);
    fontYOffset = Math.round(lineMetrics.getDescent());
    Rectangle2D stringBounds = font.getStringBounds(text, fontRenderContext);
    int width = (int)Math.round(stringBounds.getWidth());
    int height = (int)Math.round(stringBounds.getHeight());
    int connectorOffset = insets.top + height - fontYOffset;
    width += insets.left + insets.right;
    height += insets.top + insets.bottom;
    setLayoutInfo(new LayoutInfo(width, height, connectorOffset));
  }

  @Override
  protected void toSVG(DiagramToSVG diagramToSVG, int xOffset, int yOffset, SvgContent svgContent) {
    LayoutInfo layoutInfo = getLayoutInfo();
    int width = layoutInfo.getWidth();
    int height = layoutInfo.getHeight();
    if(link != null) {
      svgContent.addElement("<a xlink:href=\"" + Utils.escapeXML(link)/* + "\" xlink:title=\"" + Utils.escapeXML(text)*/ + "\">");
    }
    Insets insets;
    Font font;
    String cssClass;
    String cssTextClass;
    BoxShape shape;
    switch(type) {
      case RULE:
        insets = diagramToSVG.getRuleInsets();
        font = diagramToSVG.getRuleFont();
        cssClass = svgContent.getDefinedCSSClass(Diagram.CSS_RULE_CLASS);
        cssTextClass = svgContent.getDefinedCSSClass(Diagram.CSS_RULE_TEXT_CLASS);
        if(cssClass == null) {
          String ruleBorderColor = Utils.convertColorToHtml(diagramToSVG.getRuleBorderColor());
          String ruleFillColor = Utils.convertColorToHtml(diagramToSVG.getRuleFillColor());
          Font ruleFont = diagramToSVG.getRuleFont();
          String ruleTextColor = Utils.convertColorToHtml(diagramToSVG.getRuleTextColor());
          cssClass = svgContent.setCSSClass(Diagram.CSS_RULE_CLASS, "fill:" + ruleFillColor + ";stroke:" + ruleBorderColor + ";");
          cssTextClass = svgContent.setCSSClass(Diagram.CSS_RULE_TEXT_CLASS, "fill:" + ruleTextColor + ";" + Utils.convertFontToCss(ruleFont));
        }
        shape = diagramToSVG.getRuleShape();
        break;
      case LITERAL:
        insets = diagramToSVG.getLiteralInsets();
        font = diagramToSVG.getLiteralFont();
        cssClass = svgContent.getDefinedCSSClass(Diagram.CSS_LITERAL_CLASS);
        cssTextClass = svgContent.getDefinedCSSClass(Diagram.CSS_LITERAL_TEXT_CLASS);
        if(cssClass == null) {
          String literalBorderColor = Utils.convertColorToHtml(diagramToSVG.getLiteralBorderColor());
          String literalFillColor = Utils.convertColorToHtml(diagramToSVG.getLiteralFillColor());
          Font literalFont = diagramToSVG.getLiteralFont();
          String literalTextColor = Utils.convertColorToHtml(diagramToSVG.getLiteralTextColor());
          cssClass = svgContent.setCSSClass(Diagram.CSS_LITERAL_CLASS, "fill:" + literalFillColor + ";stroke:" + literalBorderColor + ";");
          cssTextClass = svgContent.setCSSClass(Diagram.CSS_LITERAL_TEXT_CLASS, "fill:" + literalTextColor + ";" + Utils.convertFontToCss(literalFont));
        }
        shape = diagramToSVG.getLiteralShape();
        break;
      case SPECIAL_SEQUENCE:
        insets = diagramToSVG.getSpecialSequenceInsets();
        font = diagramToSVG.getSpecialSequenceFont();
        cssClass = svgContent.getDefinedCSSClass(Diagram.CSS_SPECIAL_SEQUENCE_CLASS);
        cssTextClass = svgContent.getDefinedCSSClass(Diagram.CSS_SPECIAL_SEQUENCE_TEXT_CLASS);
        if(cssClass == null) {
          String specialSequenceBorderColor = Utils.convertColorToHtml(diagramToSVG.getSpecialSequenceBorderColor());
          String specialSequenceFillColor = Utils.convertColorToHtml(diagramToSVG.getSpecialSequenceFillColor());
          Font specialSequenceFont = diagramToSVG.getSpecialSequenceFont();
          String specialSequenceTextColor = Utils.convertColorToHtml(diagramToSVG.getSpecialSequenceTextColor());
          cssClass = svgContent.setCSSClass(Diagram.CSS_SPECIAL_SEQUENCE_CLASS, "fill:" + specialSequenceFillColor + ";stroke:" + specialSequenceBorderColor + ";");
          cssTextClass = svgContent.setCSSClass(Diagram.CSS_SPECIAL_SEQUENCE_TEXT_CLASS, "fill:" + specialSequenceTextColor + ";" + Utils.convertFontToCss(specialSequenceFont));
        }
        shape = diagramToSVG.getSpecialSequenceShape();
        break;
      default:
        throw new IllegalStateException("Unknown type: " + type);
    }
    switch(shape) {
      case RECTANGLE:
        svgContent.addElement("<rect class=\"" + cssClass + "\" x=\"" + xOffset + "\" y=\"" + yOffset + "\" width=\"" + width + "\" height=\"" + height + "\"/>");
        break;
      case ROUNDED_RECTANGLE:
        // Connector may be in rounded area if there are huge margins at top, but this is an unrealistic case so we don't add lines to complete the connector.
        int rx = (insets.left + insets.right + insets.top + insets.bottom) / 4;
        svgContent.addElement("<rect class=\"" + cssClass + "\" x=\"" + xOffset + "\" y=\"" + yOffset + "\" width=\"" + width + "\" height=\"" + height + "\" rx=\"" + rx + "\"/>");
        break;
      case HEXAGON:
        // We don't calculate the exact length of the connector: it goes behind the shape.
        // We should calculate if we want to support transparent shapes.
        int connectorOffset = layoutInfo.getConnectorOffset();
        svgContent.addLineConnector(xOffset, yOffset + connectorOffset, xOffset + insets.left, yOffset + connectorOffset);
        svgContent.addElement("<polygon class=\"" + cssClass + "\" points=\"" + xOffset + " " + (yOffset + height / 2) + " " + (xOffset + insets.left) + " " + yOffset + " " + (xOffset + width - insets.right) + " " + yOffset + " " + (xOffset + width) + " " + (yOffset + height / 2) + " " + (xOffset + width - insets.right) + " " + (yOffset + height) + " " + (xOffset + insets.left) + " " + (yOffset + height) + "\"/>");
        svgContent.addLineConnector(xOffset + width, yOffset + connectorOffset, xOffset + width - insets.right, yOffset + connectorOffset);
        break;
    }
    FontRenderContext fontRenderContext = new FontRenderContext(null, true, false);
    Rectangle2D stringBounds = font.getStringBounds(text, fontRenderContext);
    int textXOffset = xOffset + insets.left;
    int textYOffset = yOffset + insets.top + (int)Math.round(stringBounds.getHeight()) - fontYOffset;
    svgContent.addElement("<text class=\"" + cssTextClass + "\" x=\"" + textXOffset + "\" y=\"" + textYOffset + "\">" + Utils.escapeXML(text) + "</text>");
    if(link != null) {
      svgContent.addElement("</a>");
    }
  }

}
