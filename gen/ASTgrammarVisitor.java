// Generated from F:/study/term_8/GA/ChartPC_antlr/grammar\ASTgrammar.g4 by ANTLR 4.8
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link ASTgrammarParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface ASTgrammarVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link ASTgrammarParser#t}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitT(ASTgrammarParser.TContext ctx);
	/**
	 * Visit a parse tree produced by {@link ASTgrammarParser#n}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitN(ASTgrammarParser.NContext ctx);
	/**
	 * Visit a parse tree produced by {@link ASTgrammarParser#l}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitL(ASTgrammarParser.LContext ctx);
	/**
	 * Visit a parse tree produced by {@link ASTgrammarParser#c}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitC(ASTgrammarParser.CContext ctx);
	/**
	 * Visit a parse tree produced by {@link ASTgrammarParser#txt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTxt(ASTgrammarParser.TxtContext ctx);
}