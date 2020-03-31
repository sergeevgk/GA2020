import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;

public class Main {
	static private String line = "( [ + {это имя узла} ] < 0 {это имя дуги} > ( [ A ] ) < 1 > ( [" +
			" * ] < 0 > ( [ B ] ) < 1 > ( [ C ] ) ) )";

	public static void main(String[] args) throws Exception {
		ASTgrammarLexer lexer = new ASTgrammarLexer(CharStreams.fromString(line));
		CommonTokenStream tokens = new CommonTokenStream(lexer);
		ASTgrammarParser parser = new ASTgrammarParser(tokens);
		ParseTree tree = parser.t();
		ParseTreeWalker walker = new ParseTreeWalker();
		ASTwalker asTwalker = new ASTwalker();
		walker.walk(asTwalker, tree);
		asTwalker.printResult();
	}
}