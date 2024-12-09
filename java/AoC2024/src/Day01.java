import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;


public class Day01 {
    public static class Solver {
        private final List<Integer> left = new ArrayList<>();
        private final List<Integer> right = new ArrayList<>();

        public Solver(String pathName) throws Exception {
            this.read(pathName);
        }


        public int solveFirst() {
            Collections.sort(left);
            Collections.sort(right);

            int output = 0;
            for (int i = 0; i < left.size(); i++) {
                output += Math.abs(left.get(i) - right.get(i));
            }
            return output;
        }

        public int solveSecond() {
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

        private void read(String pathName) throws Exception {
            try {
                File file = new File(pathName);
                Scanner scanner = new Scanner(file);
                while (scanner.hasNextLine()) {
                    String line = scanner.nextLine().trim();
                    String[] parts = line.split(" {3}");
                    if (parts.length == 2) {
                        this.left.add(Integer.valueOf(parts[0]));
                        this.right.add(Integer.valueOf(parts[1]));
                    } else {
                        throw new Exception("Incorrect input parser");
                    }
                }
                scanner.close();
            } catch (FileNotFoundException e) {
                throw new Exception("File not Found");
            }
        }
    }

    public static int solveFirst(String pathName) {
        try {
            return new Solver(pathName).solveFirst();
        }
        catch (Exception ignored) {

        }
        return -1;
    }

    public static int solveSecond(String pathName) {
        try {
            return new Solver(pathName).solveSecond();
        }
        catch (Exception ignored) {

        }
        return -1;
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