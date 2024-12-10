import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.stream.Stream;


public class Day01 {
    private final String pathName;
    private final List<Integer> left = new ArrayList<>();
    private final List<Integer> right = new ArrayList<>();

    public Day01(String pathName) {
        this.pathName = pathName;
    }

    public static int solveFirst(String pathName) {
        return new Day01(pathName).read().first();
    }

    public static int solveSecond(String pathName) {
        return new Day01(pathName).read().second();
    }

    public static void main(String[] args) {
        Map<String, Integer> test_first = new HashMap<>();
        Map<String, Integer> test_second = new HashMap<>();

        String folder = "day_01";
        String mainPathName = String.format("data/%s/input.txt", folder);
        test_first.put(String.format("data/%s/test_0.txt", folder), 11);
        test_second.put(String.format("data/%s/test_0.txt", folder), 31);

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

    private Day01 read() {
        try (Stream<String> lines = Files.lines(Path.of(this.pathName))) {
            lines.forEach(line -> {
                String[] parts = line.trim().split(" {3}"); // three space separator
                if (parts.length != 2) {
                    throw new RuntimeException("Unexpected input format");
                }
                this.left.add(Integer.valueOf(parts[0]));
                this.right.add(Integer.valueOf(parts[1]));
            });
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        return this;
    }

    private int first() {
        Collections.sort(left);
        Collections.sort(right);

        int sum = 0;
        for (int i = 0; i < left.size(); i++) {
            sum += Math.abs(left.get(i) - right.get(i));
        }
        return sum;
    }

    private int second() {
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