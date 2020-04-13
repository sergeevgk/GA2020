import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;

public class Repeater extends ASTgrammarBaseListener {

	private StringBuilder _initialString = new StringBuilder();

	public Repeater(ParseTree tree) {
		ParseTreeWalker walker = new ParseTreeWalker();
		walker.walk(this, tree);
	}

	@Override
	public void enterT(ASTgrammarParser.TContext ctx) {
		_initialString.append("(");
	}

	@Override
	public void exitT(ASTgrammarParser.TContext ctx) {
		_initialString.append(")");
	}

	@Override
	public void enterN(ASTgrammarParser.NContext ctx) {
		_initialString.append("[");
	}

	@Override
	public void exitN(ASTgrammarParser.NContext ctx) {
		_initialString.append("]");
	}

	@Override
	public void enterL(ASTgrammarParser.LContext ctx) {
		_initialString.append("<");
	}

	@Override
	public void exitL(ASTgrammarParser.LContext ctx) {
		_initialString.append(">");
	}

	@Override
	public void enterC(ASTgrammarParser.CContext ctx) {
		_initialString.append("{");
	}

	@Override
	public void exitC(ASTgrammarParser.CContext ctx) {
		_initialString.append("}");
	}

	@Override
	public void enterTxt(ASTgrammarParser.TxtContext ctx) {
		_initialString.append(ctx.getText());
	}

	@Override
	public void exitTxt(ASTgrammarParser.TxtContext ctx) {

	}

	public String getInitialString() {
		return _initialString.toString();
	}
}
