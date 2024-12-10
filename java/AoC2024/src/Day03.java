import java.io.IOException;
import java.util.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class Day03 {
    private final String pathName;
    private String data;

    public Day03(String pathName) {
        this.pathName = pathName;
    }

    private Day03 read() {
        try {
            this.data = Files.readString(Path.of(this.pathName)).strip();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return this;
    }

    private static int sum_products(String text) {
        Pattern pattern = Pattern.compile("mul\\((\\d+),(\\d+)\\)");
        Matcher matcher = pattern.matcher(text);
        int sum = 0;
        while (matcher.find()) {
            sum += Integer.parseInt(matcher.group(1)) * Integer.parseInt(matcher.group(2));
        }
        return sum;
    }

    private static List<String> grab_active(String text) {
        Pattern pattern = Pattern.compile("(?:do\\(\\)|^)(?s)(.*?)(?:don't\\(\\)|$)");
        Matcher matcher = pattern.matcher(text);
        List<String> list = new ArrayList<>();
        while (matcher.find()) {
            list.add(matcher.group(1));
        }
        return list;
    }

    private int first() {
        return sum_products(this.data);
    }

    private int second() {
        return grab_active(this.data).stream().mapToInt(Day03::sum_products).sum();
    }

    // TEST CODE BELOW

    public static int solveFirst(String pathName) {
        return new Day03(pathName).read().first();
    }

    public static int solveSecond(String pathName) {
        return new Day03(pathName).read().second();
    }

    public static void main(String[] args) {
        Map<String, Integer> test_first = new HashMap<>();
        Map<String, Integer> test_second = new HashMap<>();

        String folder = "day_03";
        String mainPathName = String.format("data/%s/input.txt", folder);
        test_first.put(String.format("data/%s/test_0.txt", folder), 161);
        test_second.put(String.format("data/%s/test_1.txt", folder), 48);

        for (Map.Entry<String, Integer> entry : test_first.entrySet()) {
            int solution = solveFirst(entry.getKey());
            System.out.printf("First %s: %s\n", entry.getKey(), solution);
            if (solution != entry.getValue()) {
                System.out.println("Failed test");
                return;
            }
        }
        System.out.printf("First %s: %s\n\n", mainPathName, solveFirst(mainPathName));

        for (Map.Entry<String, Integer> entry : test_second.entrySet()) {
            int solution = solveSecond(entry.getKey());
            System.out.printf("Second %s: %s\n", entry.getKey(), solution);
            if (solution != entry.getValue()) {
                System.out.println("Failed test");
                return;
            }
        }
        System.out.printf("Second %s: %s\n", mainPathName, solveSecond(mainPathName));
    }
}