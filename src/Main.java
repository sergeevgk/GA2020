import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Main {

	static private String _inputFolder = "examples";
	static private String _outputFolder = "gen_dot";

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
		generator.generateDot(outputFile, "Tree");
	}

	static void processFolder(String inputFolder, String outputFolder) throws IOException {
		File folder = new File(inputFolder);
		File[] folderEntries = folder.listFiles();
		int fileNumber = 1;
		for (File entry : folderEntries) {
			if (!entry.isDirectory()) {
				processFile(entry.getAbsolutePath(), outputFolder + "/dot" + fileNumber);
				fileNumber++;
			}
		}
	}

	public static void main(String[] args) {
		try {
			processFolder(_inputFolder, _outputFolder);
		} catch (IOException e) {
			System.out.println(e.getMessage());
		}
	}
}