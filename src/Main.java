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

	static String _defaultInput = "random_generated_tree.txt";
	static String _defaultOutput = "generated_dot.txt";

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

		pythonScriptExecute("DOTURLGenerator.py", outputFile);
	}

	static void processFolder(String inputFolder, String outputFolder) throws IOException {
		String outputFile;
		File folder = new File(inputFolder);
		File[] folderEntries = folder.listFiles();
		int fileNumber = 1;
		for (File entry : folderEntries) {
			if (!entry.isDirectory()) {
				outputFile = outputFolder + "\\generated_dot" + fileNumber + ".txt";
				processFile(entry.getAbsolutePath(), outputFile);
				fileNumber++;
			}
		}
	}

	static void pythonScriptExecute(String script, String scriptArgs) {
		String command = "python " + script + " " + scriptArgs;
		try {
			Process p = Runtime.getRuntime().exec(command);
			while (p.isAlive()) {
				Thread.sleep(100);
			}
		} catch (Exception e) {
			System.err.println("Can't call python script " + script);
		}
	}

	public static void main(String[] args) {
		String inputFile = _defaultInput, outputFile = _defaultOutput;

		switch (args.length) {
			case 0:
				System.out.println("No program arguments found, generating random tree...");
				pythonScriptExecute("random_tree_generator.py", _defaultInput);
				break;
			case 1:
				System.out.println("Output will be generated to " + _defaultOutput);
				inputFile = args[0];
				break;
			default:
				inputFile = args[0];
				outputFile = args[1];
		}
		try {
			processFile(inputFile, outputFile);
		} catch (IOException e) {
			System.err.println(e.getMessage());
		}
	}
}