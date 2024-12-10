import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;


public class Day01 {
    private final String pathName;
    private final List<Integer> left = new ArrayList<>();
    private final List<Integer> right = new ArrayList<>();

    public Day01(String pathName) {
        this.pathName = pathName;
    }

    private Day01 read() {
        try {
            File file = new File(this.pathName);
            Scanner scanner = new Scanner(file);
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine().trim();
                String[] parts = line.split(" {3}");
                if (parts.length == 2) {
                    this.left.add(Integer.valueOf(parts[0]));
                    this.right.add(Integer.valueOf(parts[1]));
                } else {
                    throw new Error("Unexpected input format");
                }
            }
            scanner.close();
        }
        catch (FileNotFoundException ignored) {
            throw new Error(String.format("File not found %s", this.pathName));
        }
        return this;
    }

    private int first() {
        Collections.sort(left);
        Collections.sort(right);

        int output = 0;
        for (int i = 0; i < left.size(); i++) {
            output += Math.abs(left.get(i) - right.get(i));
        }
        return output;
    }

    private int second() {
        HashMap<Integer, Integer> counts = new HashMap<>();
        for (Integer i : right) {
            counts.put(i, counts.getOrDefault(i, 0) + 1);
        }
        int output = 0;
        for (Integer i : left) {
            output += i * counts.getOrDefault(i, 0);
        }
        return output;
    }

    // TEST CODE BELOW

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
}