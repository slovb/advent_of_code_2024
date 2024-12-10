import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Stream;


public class Day01 implements Solver<Integer> {
    private final List<Integer> left = new ArrayList<>();
    private final List<Integer> right = new ArrayList<>();

    public Day01() {
    }

    public static void main(String[] args) {
        String folder = String.format("data/%s", Day01.class.getSimpleName());
        new Runner<>(Day01::read, folder).addFirstTest(
                "test_0.txt", 11

        ).addSecondTest(
                "test_0.txt", 31
        ).run();
    }

    private static Day01 read(String pathName) {
        Day01 solver = new Day01();
        try (Stream<String> lines = Files.lines(Path.of(pathName))) {
            lines.forEach(line -> {
                String[] parts = line.trim().split(" {3}"); // three space separator
                if (parts.length != 2) {
                    throw new RuntimeException("Unexpected input format");
                }
                solver.left.add(Integer.valueOf(parts[0]));
                solver.right.add(Integer.valueOf(parts[1]));
            });
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        return solver;
    }

    public Integer first() {
        Collections.sort(left);
        Collections.sort(right);

        int sum = 0;
        for (int i = 0; i < left.size(); i++) {
            sum += Math.abs(left.get(i) - right.get(i));
        }
        return sum;
    }

    public Integer second() {
        HashMap<Integer, Integer> counts = new HashMap<>();
        for (Integer value : right) {
            counts.put(value, counts.getOrDefault(value, 0) + 1);
        }
        int sum = 0;
        for (Integer value : left) {
            sum += value * counts.getOrDefault(value, 0);
        }
        return sum;
    }
}