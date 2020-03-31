import org.antlr.v4.runtime.ParserRuleContext;

public class ASTwalker extends ASTgrammarBaseListener {

	private StringBuilder result = new StringBuilder();

	@Override
	public void enterT(ASTgrammarParser.TContext ctx) {
		System.out.println( "Entering T : " + ctx.getText() );
		result.append("(");
	}

	@Override
	public void exitT(ASTgrammarParser.TContext ctx) {
		System.out.println( "Exiting T" );
		result.append(")");
	}

	@Override
	public void enterN(ASTgrammarParser.NContext ctx) {
		System.out.println( "Entering N : " + ctx.getText() );
		result.append("[");
	}

	@Override
	public void exitN(ASTgrammarParser.NContext ctx) {
		System.out.println( "Exiting N" );
		result.append("]");
	}

	@Override
	public void enterL(ASTgrammarParser.LContext ctx) {
		System.out.println( "Entering L : " + ctx.getText() );
		result.append("<");
	}

	@Override
	public void exitL(ASTgrammarParser.LContext ctx) {
		System.out.println( "Exiting L" );
		result.append(">");
	}

	@Override
	public void enterC(ASTgrammarParser.CContext ctx) {
		System.out.println( "Entering C : " + ctx.getText() );
		result.append("{");
	}

	@Override
	public void exitC(ASTgrammarParser.CContext ctx) {
		System.out.println( "Exiting C" );
		result.append("}");
	}

	@Override
	public void enterTxt(ASTgrammarParser.TxtContext ctx) {
		System.out.println( "Entering Txt : " + ctx.getText() );
		result.append(ctx.getText());
	}

	@Override
	public void exitTxt(ASTgrammarParser.TxtContext ctx) {
		System.out.println( "Exiting Txt" );
	}

	public void printResult()
	{
		System.out.println(result.toString());
	}
}
