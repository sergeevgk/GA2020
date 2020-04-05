package epc.utils;

public class StringUtils {

    public static String toFirstLetterUpperCase(String word) {
        return word.substring(0, 1).toUpperCase() + word.substring(1);
    }

    public static String toFirstLetterLowerCase(String word) {
        return word.substring(0, 1).toLowerCase() + word.substring(1);
    }
}
