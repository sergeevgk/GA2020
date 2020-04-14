import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Main {

	static ParseTree generateParseTree(String line) {
		ASTgrammarLexer lexer = new ASTgrammarLexer(CharStreams.fromString(line));
		CommonTokenStream tokens = new CommonTokenStream(lexer);
		ASTgrammarParser parser = new ASTgrammarParser(tokens);
		return parser.t();
	}

	static void processFile(String inputFile, String outputFile) throws IOException {
		StringBuilder stringBuilder = new StringBuilder();
		Files.lines(Paths.get(inputFile), StandardCharsets.UTF_8).forEach(stringBuilder::append);

		ParseTree tree = generateParseTree(stringBuilder.toString());
		Repeater repeater = new Repeater(tree);
		System.out.println(repeater.getInitialString());

		DotGenerator generator = new DotGenerator(tree);
		FileWriter writer = new FileWriter(outputFile, false);
		writer.write(generator.generateDot("Tree"));
		writer.flush();
		writer.close();
	}

	static void processFolder(String inputFolder, String outputFolder) throws IOException {
		String outputFile;
		File folder = new File(inputFolder);
		File[] folderEntries = folder.listFiles();
		int fileNumber = 1;
		for (File entry : folderEntries) {
			if (!entry.isDirectory()) {
				outputFile = outputFolder + "dot" + fileNumber + ".txt";
				processFile(entry.getAbsolutePath(), outputFile);
				fileNumber++;
			}
		}
	}

	public static void main(String[] args) {
		if (args.length == 0) {
			System.out.println("No program arguments found");
			return;
		}
		String inputFolder, outputFolder;
		inputFolder = args[0];
		if (args.length > 1) {
			outputFolder = args[1] + "\\";
		} else {
			outputFolder = "";
		}
		try {
			processFolder(inputFolder, outputFolder);
		} catch (IOException e) {
			System.out.println(e.getMessage());
		}
	}
}