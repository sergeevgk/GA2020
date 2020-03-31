// Generated from F:/study/term_8/GA/ChartPC_antlr/grammar\ASTgrammar.g4 by ANTLR 4.8
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link ASTgrammarParser}.
 */
public interface ASTgrammarListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link ASTgrammarParser#t}.
	 * @param ctx the parse tree
	 */
	void enterT(ASTgrammarParser.TContext ctx);
	/**
	 * Exit a parse tree produced by {@link ASTgrammarParser#t}.
	 * @param ctx the parse tree
	 */
	void exitT(ASTgrammarParser.TContext ctx);
	/**
	 * Enter a parse tree produced by {@link ASTgrammarParser#n}.
	 * @param ctx the parse tree
	 */
	void enterN(ASTgrammarParser.NContext ctx);
	/**
	 * Exit a parse tree produced by {@link ASTgrammarParser#n}.
	 * @param ctx the parse tree
	 */
	void exitN(ASTgrammarParser.NContext ctx);
	/**
	 * Enter a parse tree produced by {@link ASTgrammarParser#l}.
	 * @param ctx the parse tree
	 */
	void enterL(ASTgrammarParser.LContext ctx);
	/**
	 * Exit a parse tree produced by {@link ASTgrammarParser#l}.
	 * @param ctx the parse tree
	 */
	void exitL(ASTgrammarParser.LContext ctx);
	/**
	 * Enter a parse tree produced by {@link ASTgrammarParser#c}.
	 * @param ctx the parse tree
	 */
	void enterC(ASTgrammarParser.CContext ctx);
	/**
	 * Exit a parse tree produced by {@link ASTgrammarParser#c}.
	 * @param ctx the parse tree
	 */
	void exitC(ASTgrammarParser.CContext ctx);
	/**
	 * Enter a parse tree produced by {@link ASTgrammarParser#txt}.
	 * @param ctx the parse tree
	 */
	void enterTxt(ASTgrammarParser.TxtContext ctx);
	/**
	 * Exit a parse tree produced by {@link ASTgrammarParser#txt}.
	 * @param ctx the parse tree
	 */
	void exitTxt(ASTgrammarParser.TxtContext ctx);
}