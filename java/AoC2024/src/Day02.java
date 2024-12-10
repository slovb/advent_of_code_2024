import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;


public class Day02 implements Solver<Integer> {
    private final List<int[]> rows = new ArrayList<>();

    public Day02() {
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

    public static void main(String[] args) {
        String folder = String.format("data/%s", Day02.class.getSimpleName());
        new Runner<>(Day02::read, folder).addFirstTest(
                "test_0.txt", 2

        ).addSecondTest(
                "test_0.txt", 4
        ).run();
    }

    private static Day02 read(String pathName) {
        Day02 solver = new Day02();
        try (Stream<String> lines = Files.lines(Path.of(pathName))) {
            lines.forEach(line -> {
                String[] split = line.trim().split(" ");
                int[] row = new int[split.length];

                for (int i = 0; i < split.length; i++) {
                    row[i] = Integer.parseInt(split[i]);
                }
                solver.rows.add(row);
            });
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return solver;
    }

    public Integer first() {
        int output = 0;
        for (int[] row : this.rows) {
            if (is_safe(row)) {
                output += 1;
            }
        }
        return output;
    }

    public Integer second() {
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