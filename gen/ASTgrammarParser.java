// Generated from F:/study/term_8/GA/ChartPC_antlr/grammar\ASTgrammar.g4 by ANTLR 4.8
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class ASTgrammarParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.8", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, SPACE=9, 
		SYMBOL=10;
	public static final int
		RULE_t = 0, RULE_n = 1, RULE_l = 2, RULE_c = 3, RULE_txt = 4;
	private static String[] makeRuleNames() {
		return new String[] {
			"t", "n", "l", "c", "txt"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'('", "')'", "'['", "']'", "'<'", "'>'", "'{'", "'}'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, "SPACE", "SYMBOL"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "ASTgrammar.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public ASTgrammarParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class TContext extends ParserRuleContext {
		public NContext n() {
			return getRuleContext(NContext.class,0);
		}
		public List<TerminalNode> SPACE() { return getTokens(ASTgrammarParser.SPACE); }
		public TerminalNode SPACE(int i) {
			return getToken(ASTgrammarParser.SPACE, i);
		}
		public List<LContext> l() {
			return getRuleContexts(LContext.class);
		}
		public LContext l(int i) {
			return getRuleContext(LContext.class,i);
		}
		public List<TContext> t() {
			return getRuleContexts(TContext.class);
		}
		public TContext t(int i) {
			return getRuleContext(TContext.class,i);
		}
		public TContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_t; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ASTgrammarListener ) ((ASTgrammarListener)listener).enterT(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ASTgrammarListener ) ((ASTgrammarListener)listener).exitT(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ASTgrammarVisitor ) return ((ASTgrammarVisitor<? extends T>)visitor).visitT(this);
			else return visitor.visitChildren(this);
		}
	}

	public final TContext t() throws RecognitionException {
		TContext _localctx = new TContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_t);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(10);
			match(T__0);
			setState(12);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SPACE) {
				{
				setState(11);
				match(SPACE);
				}
			}

			setState(14);
			n();
			setState(16);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SPACE) {
				{
				setState(15);
				match(SPACE);
				}
			}

			setState(28);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__4) {
				{
				{
				setState(18);
				l();
				setState(20);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==SPACE) {
					{
					setState(19);
					match(SPACE);
					}
				}

				setState(22);
				t();
				setState(24);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==SPACE) {
					{
					setState(23);
					match(SPACE);
					}
				}

				}
				}
				setState(30);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(31);
			match(T__1);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class NContext extends ParserRuleContext {
		public TxtContext txt() {
			return getRuleContext(TxtContext.class,0);
		}
		public List<TerminalNode> SPACE() { return getTokens(ASTgrammarParser.SPACE); }
		public TerminalNode SPACE(int i) {
			return getToken(ASTgrammarParser.SPACE, i);
		}
		public List<CContext> c() {
			return getRuleContexts(CContext.class);
		}
		public CContext c(int i) {
			return getRuleContext(CContext.class,i);
		}
		public NContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_n; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ASTgrammarListener ) ((ASTgrammarListener)listener).enterN(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ASTgrammarListener ) ((ASTgrammarListener)listener).exitN(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ASTgrammarVisitor ) return ((ASTgrammarVisitor<? extends T>)visitor).visitN(this);
			else return visitor.visitChildren(this);
		}
	}

	public final NContext n() throws RecognitionException {
		NContext _localctx = new NContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_n);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(33);
			match(T__2);
			setState(35);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SPACE) {
				{
				setState(34);
				match(SPACE);
				}
			}

			setState(37);
			txt();
			setState(39);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SPACE) {
				{
				setState(38);
				match(SPACE);
				}
			}

			setState(47);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__6) {
				{
				{
				setState(41);
				c();
				setState(43);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==SPACE) {
					{
					setState(42);
					match(SPACE);
					}
				}

				}
				}
				setState(49);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(50);
			match(T__3);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class LContext extends ParserRuleContext {
		public TxtContext txt() {
			return getRuleContext(TxtContext.class,0);
		}
		public List<TerminalNode> SPACE() { return getTokens(ASTgrammarParser.SPACE); }
		public TerminalNode SPACE(int i) {
			return getToken(ASTgrammarParser.SPACE, i);
		}
		public List<CContext> c() {
			return getRuleContexts(CContext.class);
		}
		public CContext c(int i) {
			return getRuleContext(CContext.class,i);
		}
		public LContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_l; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ASTgrammarListener ) ((ASTgrammarListener)listener).enterL(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ASTgrammarListener ) ((ASTgrammarListener)listener).exitL(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ASTgrammarVisitor ) return ((ASTgrammarVisitor<? extends T>)visitor).visitL(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LContext l() throws RecognitionException {
		LContext _localctx = new LContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_l);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(52);
			match(T__4);
			setState(54);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SPACE) {
				{
				setState(53);
				match(SPACE);
				}
			}

			setState(56);
			txt();
			setState(58);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SPACE) {
				{
				setState(57);
				match(SPACE);
				}
			}

			setState(66);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__6) {
				{
				{
				setState(60);
				c();
				setState(62);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==SPACE) {
					{
					setState(61);
					match(SPACE);
					}
				}

				}
				}
				setState(68);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(69);
			match(T__5);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class CContext extends ParserRuleContext {
		public TxtContext txt() {
			return getRuleContext(TxtContext.class,0);
		}
		public List<TerminalNode> SPACE() { return getTokens(ASTgrammarParser.SPACE); }
		public TerminalNode SPACE(int i) {
			return getToken(ASTgrammarParser.SPACE, i);
		}
		public CContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_c; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ASTgrammarListener ) ((ASTgrammarListener)listener).enterC(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ASTgrammarListener ) ((ASTgrammarListener)listener).exitC(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ASTgrammarVisitor ) return ((ASTgrammarVisitor<? extends T>)visitor).visitC(this);
			else return visitor.visitChildren(this);
		}
	}

	public final CContext c() throws RecognitionException {
		CContext _localctx = new CContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_c);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(71);
			match(T__6);
			setState(73);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SPACE) {
				{
				setState(72);
				match(SPACE);
				}
			}

			setState(75);
			txt();
			setState(77);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SPACE) {
				{
				setState(76);
				match(SPACE);
				}
			}

			setState(79);
			match(T__7);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class TxtContext extends ParserRuleContext {
		public List<TerminalNode> SYMBOL() { return getTokens(ASTgrammarParser.SYMBOL); }
		public TerminalNode SYMBOL(int i) {
			return getToken(ASTgrammarParser.SYMBOL, i);
		}
		public List<TerminalNode> SPACE() { return getTokens(ASTgrammarParser.SPACE); }
		public TerminalNode SPACE(int i) {
			return getToken(ASTgrammarParser.SPACE, i);
		}
		public TxtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_txt; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ASTgrammarListener ) ((ASTgrammarListener)listener).enterTxt(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ASTgrammarListener ) ((ASTgrammarListener)listener).exitTxt(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ASTgrammarVisitor ) return ((ASTgrammarVisitor<? extends T>)visitor).visitTxt(this);
			else return visitor.visitChildren(this);
		}
	}

	public final TxtContext txt() throws RecognitionException {
		TxtContext _localctx = new TxtContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_txt);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(81);
			match(SYMBOL);
			setState(88);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,16,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(83);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==SPACE) {
						{
						setState(82);
						match(SPACE);
						}
					}

					setState(85);
					match(SYMBOL);
					}
					} 
				}
				setState(90);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,16,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\f^\4\2\t\2\4\3\t"+
		"\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\3\2\5\2\17\n\2\3\2\3\2\5\2\23\n\2\3\2\3"+
		"\2\5\2\27\n\2\3\2\3\2\5\2\33\n\2\7\2\35\n\2\f\2\16\2 \13\2\3\2\3\2\3\3"+
		"\3\3\5\3&\n\3\3\3\3\3\5\3*\n\3\3\3\3\3\5\3.\n\3\7\3\60\n\3\f\3\16\3\63"+
		"\13\3\3\3\3\3\3\4\3\4\5\49\n\4\3\4\3\4\5\4=\n\4\3\4\3\4\5\4A\n\4\7\4C"+
		"\n\4\f\4\16\4F\13\4\3\4\3\4\3\5\3\5\5\5L\n\5\3\5\3\5\5\5P\n\5\3\5\3\5"+
		"\3\6\3\6\5\6V\n\6\3\6\7\6Y\n\6\f\6\16\6\\\13\6\3\6\2\2\7\2\4\6\b\n\2\2"+
		"\2i\2\f\3\2\2\2\4#\3\2\2\2\6\66\3\2\2\2\bI\3\2\2\2\nS\3\2\2\2\f\16\7\3"+
		"\2\2\r\17\7\13\2\2\16\r\3\2\2\2\16\17\3\2\2\2\17\20\3\2\2\2\20\22\5\4"+
		"\3\2\21\23\7\13\2\2\22\21\3\2\2\2\22\23\3\2\2\2\23\36\3\2\2\2\24\26\5"+
		"\6\4\2\25\27\7\13\2\2\26\25\3\2\2\2\26\27\3\2\2\2\27\30\3\2\2\2\30\32"+
		"\5\2\2\2\31\33\7\13\2\2\32\31\3\2\2\2\32\33\3\2\2\2\33\35\3\2\2\2\34\24"+
		"\3\2\2\2\35 \3\2\2\2\36\34\3\2\2\2\36\37\3\2\2\2\37!\3\2\2\2 \36\3\2\2"+
		"\2!\"\7\4\2\2\"\3\3\2\2\2#%\7\5\2\2$&\7\13\2\2%$\3\2\2\2%&\3\2\2\2&\'"+
		"\3\2\2\2\')\5\n\6\2(*\7\13\2\2)(\3\2\2\2)*\3\2\2\2*\61\3\2\2\2+-\5\b\5"+
		"\2,.\7\13\2\2-,\3\2\2\2-.\3\2\2\2.\60\3\2\2\2/+\3\2\2\2\60\63\3\2\2\2"+
		"\61/\3\2\2\2\61\62\3\2\2\2\62\64\3\2\2\2\63\61\3\2\2\2\64\65\7\6\2\2\65"+
		"\5\3\2\2\2\668\7\7\2\2\679\7\13\2\28\67\3\2\2\289\3\2\2\29:\3\2\2\2:<"+
		"\5\n\6\2;=\7\13\2\2<;\3\2\2\2<=\3\2\2\2=D\3\2\2\2>@\5\b\5\2?A\7\13\2\2"+
		"@?\3\2\2\2@A\3\2\2\2AC\3\2\2\2B>\3\2\2\2CF\3\2\2\2DB\3\2\2\2DE\3\2\2\2"+
		"EG\3\2\2\2FD\3\2\2\2GH\7\b\2\2H\7\3\2\2\2IK\7\t\2\2JL\7\13\2\2KJ\3\2\2"+
		"\2KL\3\2\2\2LM\3\2\2\2MO\5\n\6\2NP\7\13\2\2ON\3\2\2\2OP\3\2\2\2PQ\3\2"+
		"\2\2QR\7\n\2\2R\t\3\2\2\2SZ\7\f\2\2TV\7\13\2\2UT\3\2\2\2UV\3\2\2\2VW\3"+
		"\2\2\2WY\7\f\2\2XU\3\2\2\2Y\\\3\2\2\2ZX\3\2\2\2Z[\3\2\2\2[\13\3\2\2\2"+
		"\\Z\3\2\2\2\23\16\22\26\32\36%)-\618<@DKOUZ";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}