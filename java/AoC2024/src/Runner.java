import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

public class Runner<V extends Comparable<V>> {
    public static final String INPUT_FILE_NAME = "input.txt";

    private final Function<String, Solver<V>> creator;
    private final String folderPathName;

    private final Map<String, V> firstTests = new HashMap<>();
    private final Map<String, V> secondTests = new HashMap<>();

    public Runner(Function<String, Solver<V>> creator, String folderPathName) {
        this.creator = creator;
        this.folderPathName = folderPathName;
    }

    public Runner<V> addFirstTest(String filename, V value) {
        firstTests.put(filename, value);
        return this;
    }

    public Runner<V> addSecondTest(String filename, V value) {
        secondTests.put(filename, value);
        return this;
    }

    private String fileNameToPathName(String filename) {
        return String.format("%s/%s", folderPathName, filename);
    }

    private V first(String fileName) {
        return creator.apply(fileNameToPathName(fileName)).first();
    }

    private V second(String fileName) {
        return creator.apply(fileNameToPathName(fileName)).second();
    }

    public void run() {
        System.out.printf("Running data from folder: %s\n\n", folderPathName);

        for (Map.Entry<String, V> entry : firstTests.entrySet()) {
            V solution = first(entry.getKey());
            System.out.printf("First %s: %s\n", entry.getKey(), solution);
            if (!solution.equals(entry.getValue())) {
                System.out.println("Failed test");
                return;
            }
        }
        System.out.printf("First %s: %s\n\n", INPUT_FILE_NAME, first(INPUT_FILE_NAME));

        for (Map.Entry<String, V> entry : secondTests.entrySet()) {
            V solution = second(entry.getKey());
            System.out.printf("Second %s: %s\n", entry.getKey(), solution);
            if (!solution.equals(entry.getValue())) {
                System.out.println("Failed test");
                return;
            }
        }
        System.out.printf("Second %s: %s\n", INPUT_FILE_NAME, second(INPUT_FILE_NAME));

    }
}
