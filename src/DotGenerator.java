import org.antlr.v4.runtime.misc.Pair;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;

import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Stack;


public class DotGenerator {

	private enum States {
		TREE,
		NODE,
		LINK,
		COMMENT_NODE,
		COMMENT_LINK
	}

	private class DotListener extends ASTgrammarBaseListener {

		private Stack<States> _statesStack = new Stack<>();
		private Stack<HashMap<String, String>> _nodesStack = new Stack<>();
		private Stack<HashMap<String, String>> _linksStack = new Stack<>();

		private int _nodeID = 0;
		private String _idKey = "__ID__";

		@Override
		public void enterT(ASTgrammarParser.TContext ctx) {
			_statesStack.push(States.TREE);
		}

		@Override
		public void exitT(ASTgrammarParser.TContext ctx) {
			popAndCheck(States.TREE);
			_nodesStack.pop();
		}

		@Override
		public void enterN(ASTgrammarParser.NContext ctx) {
			_statesStack.push(States.NODE);
		}

		@Override
		public void exitN(ASTgrammarParser.NContext ctx) {
			int nodesAmount = _nodesStack.size();
			HashMap<String, String> current;
			popAndCheck(States.NODE);
			if (nodesAmount == 0) {
				System.err.println("No nodes on the stack when exiting N");
				return;
			}

			// generate node declaration
			current = _nodesStack.peek();
			_stringBuilder.append('\t').append(getIDAndCheck(current)).append(" ");
			printAttributes(current);
			_stringBuilder.append('\n');

			// generate link with parent node
			if (nodesAmount > 1) {
				HashMap<String, String> previous = _nodesStack.get(nodesAmount - 2);
				if (_linksStack.empty()) {
					System.err.println("No links on the stack with several nodes");
					return;
				}
				_stringBuilder.append('\t').append(getIDAndCheck(previous));
				_stringBuilder.append(" -- ").append(getIDAndCheck(current)).append(" ");
				printAttributes(_linksStack.pop());
				_stringBuilder.append(" ").append('\n');
			}
		}

		@Override
		public void enterL(ASTgrammarParser.LContext ctx) {
			_statesStack.push(States.LINK);
		}

		@Override
		public void exitL(ASTgrammarParser.LContext ctx) {
			popAndCheck(States.LINK);
		}

		@Override
		public void enterC(ASTgrammarParser.CContext ctx) {
			if (_statesStack.empty()) {
				System.err.println("Comment as the only state on the stack");
			}
			switch (_statesStack.peek()) {
				case LINK:
					_statesStack.push(States.COMMENT_LINK);
					break;
				case NODE:
					_statesStack.push(States.COMMENT_NODE);
					break;
				default:
					System.err.println("Wrong state before comment" + _statesStack.peek());
			}
		}

		@Override
		public void exitC(ASTgrammarParser.CContext ctx) {
			States top = _statesStack.pop();
			if (top != States.COMMENT_NODE && top != States.COMMENT_LINK) {
				System.err.println("Wrong state before exiting comment" + top);
			}
		}

		@Override
		public void enterTxt(ASTgrammarParser.TxtContext ctx) {
			String text = ctx.getText();
			Pair<String, String> pair;
			if (_statesStack.empty()) {
				System.err.println("Empty stack before text");
				return;
			}
			switch (_statesStack.peek()) {
				case NODE:
					HashMap<String, String> node = new HashMap<>();
					node.put("label", text);
					node.put(_idKey, Integer.toString(_nodeID));
					_nodeID++;
					_nodesStack.push(node);
					break;
				case COMMENT_NODE:
					pair = parseAttribute(text);
					if (pair != null) {
						_nodesStack.peek().put(pair.a, pair.b);
					}
					break;
				case LINK:
					HashMap<String, String> link = new HashMap<>();
					link.put("label", text);
					_linksStack.push(link);
					break;
				case COMMENT_LINK:
					pair = parseAttribute(text);
					if (pair != null) {
						_linksStack.peek().put(pair.a, pair.b);
					}
					break;
				default:
					System.err.println("Wrong state before text:" + _statesStack.peek());
					break;
			}
		}

		@Override
		public void exitTxt(ASTgrammarParser.TxtContext ctx) {
		}

		private boolean popAndCheck(States expectedState) {
			if (_statesStack.empty()) {
				System.err.println("Pop from empty stack");
				return false;
			}
			States top = _statesStack.pop();
			if (top != expectedState) {
				System.err.println("Got " + top + ", expected " + expectedState);
				return false;
			} else {
				return true;
			}
		}

		private Pair<String, String> parseAttribute(String text) {
			String[] values = text.split("=");
			if (values.length != 2)
				return null;
			return new Pair<>(values[0].trim(), values[1].trim());
		}

		private void printAttributes(HashMap<String, String> attrMap) {
			String key;
			_stringBuilder.append("[ ");
			for (Map.Entry pair : attrMap.entrySet()) {
				key = (String) pair.getKey();
				if (!key.equals(_idKey)) {
					_stringBuilder.append(key);
					_stringBuilder.append("=\"").append((String) pair.getValue()).append("\" ");
				}
			}
			_stringBuilder.append(']');
		}

		private String getIDAndCheck(HashMap<String, String> attrMap) {
			if (!attrMap.containsKey(_idKey)) {
				System.err.println("Missing node ID");
				return "__MISSING__ID__";
			}
			return attrMap.get(_idKey);
		}
	} // end DotListener


	private ParseTree _tree;
	private StringBuilder _stringBuilder;
	private ParseTreeWalker _walker = new ParseTreeWalker();


	public DotGenerator(ParseTree tree) {
		_tree = tree;
	}

	public String generateDot(String graphName) {
		DotListener listener = new DotListener();
		_stringBuilder = new StringBuilder();

		_stringBuilder.append("graph ").append(graphName).append(" {\n");
		_walker.walk(listener, _tree);
		_stringBuilder.append('}');
		return _stringBuilder.toString();
	}
}
