import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class Day03 implements Solver<Integer> {
    private String data;

    public Day03() {
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

    public static void main(String[] args) {
        String folder = String.format("data/%s", Day03.class.getSimpleName());
        new Runner<>(Day03::read, folder).addFirstTest(
                "test_0.txt", 161
        ).addSecondTest(
                "test_1.txt", 48
        ).run();
    }

    private static Day03 read(String pathName) {
        Day03 solver = new Day03();
        try {
            solver.data = Files.readString(Path.of(pathName)).strip();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return solver;
    }

    public Integer first() {
        return sum_products(this.data);
    }

    public Integer second() {
        return grab_active(this.data).stream().mapToInt(Day03::sum_products).sum();
    }
}