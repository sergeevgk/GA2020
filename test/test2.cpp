#include <cstdio>

void test_func(int c) {
c = c+3;	
}

int main() {
	int c = 3;
	if (c ==3) {
		if (c-2== 1) {
			printf("%d\n", c);
		}
	} else if (c == 5) { return 1; }
	return 0;
}