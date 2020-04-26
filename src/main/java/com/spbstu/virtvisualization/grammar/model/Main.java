package com.spbstu.virtvisualization.grammar.model;

import java.io.*;

import com.spbstu.virtvisualization.grammar.diagram.DiagramToSVG;

public class Main {
    public static void main(String[] args) {
        try {
            StringReader reader = new StringReader("<digit>          ::= \"0\" | \"1\" | \"2\" | \"3\" | \"4\" | " +
                    "\"5\" | \"6\" | \"7\" | \"8\" | \"9\";" +
                    "<signed>::=\"+\"<digit>|\"-\"<digit>;");

            System.out.println(args.length);
            System.out.println(args[0]);
            if (args.length != 1) {
                System.out.println("Expected filename in args");
                return;
            }
            FileReader fileReader = new FileReader(new File(args[0]));
            BNFToGrammar bnfToGrammar = new BNFToGrammar();
            Grammar grammar = bnfToGrammar.convert(fileReader);
            System.out.println(grammar.toString());

            int i = 0;
            for (Rule r : grammar.getRules()) {
                DiagramToSVG diagramToSVG = new DiagramToSVG();
                GrammarToDiagram grr = new GrammarToDiagram();
                String svg = diagramToSVG.convert(r.toRRDiagram(grr));
                String outfilename = r.getName().substring(1, r.getName().length() - 1);
                System.out.println(svg);
                System.out.println(outfilename);
                FileWriter writer = new FileWriter(outfilename + ".svg", false);
                try
                {
                    writer.write(svg);
                    writer.flush();
                }
                catch(IOException ex){

                    System.out.println(ex.getMessage());
                }
            }

            /*
            Diagram rrDiagram = new Diagram(rrElement);
            DiagramToSVG rrDiagramToSVG = new DiagramToSVG();
            String svg = rrDiagramToSVG.convert(rrDiagram);
            */
        } catch (IOException e) {
            System.out.println("File not found!");
        }


    }
}
