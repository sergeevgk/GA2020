SET CLASSPATH=.;%~dp0antlr-4.8-complete.jar;%CLASSPATH%
doskey antlr4py3=java org.antlr.v4.Tool -Dlanguage=Python3 -visitor $*
