import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;


public class Day02 {
    private final String pathName;
    private final List<int[]> rows = new ArrayList<>();

    public Day02(String pathName) {
        this.pathName = pathName;
    }

    private static boolean is_safe(int[] row, int skip) {
        int last_diff = 0;
        int i = 0;
        if (skip == i) {
            i += 1;
        }
        int prev = row[i];
        for (i = i + 1; i < row.length; i++) {
            if (skip == i) {
                continue;
            }
            int diff = prev - row[i];
            if (diff == 0 || Math.abs(diff) > 3) {
                return false;
            }
            if (diff * last_diff < 0) { // swap signs
                return false;
            }
            last_diff = diff;
            prev = row[i];
        }
        return true;
    }

    private static boolean is_safe(int[] row) {
        // -1 won't be an index so this is without skip, but a bit messy
        return is_safe(row, -1);
    }

    public static int solveFirst(String pathName) {
        return new Day02(pathName).read().first();
    }

    public static int solveSecond(String pathName) {
        return new Day02(pathName).read().second();
    }

    public static void main(String[] args) {
        Map<String, Integer> test_first = new HashMap<>();
        Map<String, Integer> test_second = new HashMap<>();

        String folder = "day_02";
        String mainPathName = String.format("data/%s/input.txt", folder);
        test_first.put(String.format("data/%s/test_0.txt", folder), 2);
        test_second.put(String.format("data/%s/test_0.txt", folder), 4);

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

    // TEST CODE BELOW

    private Day02 read() {
        try (Stream<String> lines = Files.lines(Path.of(pathName))) {
            lines.forEach(line -> {
                String[] split = line.trim().split(" ");
                int[] row = new int[split.length];

                for (int i = 0; i < split.length; i++) {
                    row[i] = Integer.parseInt(split[i]);
                }
                this.rows.add(row);
            });
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return this;
    }

    private int first() {
        int output = 0;
        for (int[] row : this.rows) {
            if (is_safe(row)) {
                output += 1;
            }
        }
        return output;
    }

    private int second() {
        int output = 0;
        for (int[] row : this.rows) {
            if (is_safe(row)) {
                output += 1;
            } else {
                for (int i = 0; i < row.length; i++) {
                    if (is_safe(row, i)) {
                        output += 1;
                        break;
                    }
                }
            }
        }
        return output;
    }
}