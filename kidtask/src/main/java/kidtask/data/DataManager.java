package kidtask.data;

import kidtask.models.*;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

/**
 * Manages all file I/O operations for the KidTask application.
 * Handles reading and writing Users, Tasks, and Wishes to CSV text files.
 */
public class DataManager {
    private static final String DATA_DIR = "data";
    private static final String USERS_FILE = DATA_DIR + "/Users.txt";
    private static final String TASKS_FILE = DATA_DIR + "/Tasks.txt";
    private static final String WISHES_FILE = DATA_DIR + "/Wishes.txt";
    
    private List<User> users;
    private List<Task> tasks;
    private List<Wish> wishes;
    
    public DataManager() {
        this.users = new ArrayList<>();
        this.tasks = new ArrayList<>();
        this.wishes = new ArrayList<>();
        ensureDataDirectoryExists();
    }
    
    /**
     * Ensures the data directory exists, creates it if it doesn't.
     */
    private void ensureDataDirectoryExists() {
        try {
            Path dataPath = Paths.get(DATA_DIR);
            if (!Files.exists(dataPath)) {
                Files.createDirectories(dataPath);
            }
        } catch (IOException e) {
            System.err.println("Error creating data directory: " + e.getMessage());
        }
    }
    
    /**
     * Ensures a file exists, creates it if it doesn't.
     */
    private void ensureFileExists(String filePath) {
        try {
            File file = new File(filePath);
            if (!file.exists()) {
                file.getParentFile().mkdirs(); // Ensure parent directory exists
                file.createNewFile();
            }
        } catch (IOException e) {
            System.err.println("Error creating file " + filePath + ": " + e.getMessage());
        }
    }
    
    /**
     * Loads all data from files on startup.
     */
    public void loadAllData() {
        loadUsers();
        loadTasks();
        loadWishes();
    }
    
    /**
     * Saves all data to files.
     */
    public void saveAllData() {
        saveUsers();
        saveTasks();
        saveWishes();
    }
    
    // ========== User Management ==========
    
    /**
     * Loads users from Users.txt file.
     */
    public void loadUsers() {
        users.clear();
        File file = new File(USERS_FILE);
        if (!file.exists()) {
            return;
        }
        
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty() || line.startsWith("#")) {
                    continue; // Skip empty lines and comments
                }
                
                User user = User.fromCSV(line);
                if (user != null) {
                    // If it's a Child, try to load with points and level
                    if (user instanceof Child) {
                        user = Child.fromCSV(line);
                    }
                    users.add(user);
                }
            }
        } catch (IOException e) {
            System.err.println("Error loading users: " + e.getMessage());
        }
    }
    
    /**
     * Saves users to Users.txt file.
     * Creates the file if it doesn't exist.
     */
    public void saveUsers() {
        ensureFileExists(USERS_FILE);
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(USERS_FILE))) {
            for (User user : users) {
                writer.write(user.toCSV());
                writer.newLine();
            }
        } catch (IOException e) {
            System.err.println("Error saving users: " + e.getMessage());
        }
    }
    
    /**
     * Adds a new user and saves to file.
     */
    public void addUser(User user) {
        users.add(user);
        saveUsers();
    }
    
    /**
     * Updates an existing user and saves to file.
     */
    public void updateUser(User user) {
        for (int i = 0; i < users.size(); i++) {
            if (users.get(i).getUsername().equals(user.getUsername())) {
                users.set(i, user);
                saveUsers();
                return;
            }
        }
    }
    
    /**
     * Finds a user by username.
     */
    public User findUser(String username) {
        for (User user : users) {
            if (user.getUsername().equals(username)) {
                return user;
            }
        }
        return null;
    }
    
    /**
     * Gets all users.
     */
    public List<User> getAllUsers() {
        return new ArrayList<>(users);
    }
    
    /**
     * Gets all children.
     */
    public List<Child> getAllChildren() {
        List<Child> children = new ArrayList<>();
        for (User user : users) {
            if (user instanceof Child) {
                children.add((Child) user);
            }
        }
        return children;
    }
    
    // ========== Task Management ==========
    
    /**
     * Loads tasks from Tasks.txt file.
     */
    public void loadTasks() {
        tasks.clear();
        File file = new File(TASKS_FILE);
        if (!file.exists()) {
            return;
        }
        
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty() || line.startsWith("#")) {
                    continue; // Skip empty lines and comments
                }
                
                Task task = Task.fromCSV(line);
                if (task != null) {
                    tasks.add(task);
                }
            }
        } catch (IOException e) {
            System.err.println("Error loading tasks: " + e.getMessage());
        }
    }
    
    /**
     * Saves tasks to Tasks.txt file.
     * Creates the file if it doesn't exist.
     */
    public void saveTasks() {
        ensureFileExists(TASKS_FILE);
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(TASKS_FILE))) {
            for (Task task : tasks) {
                writer.write(task.toCSV());
                writer.newLine();
            }
        } catch (IOException e) {
            System.err.println("Error saving tasks: " + e.getMessage());
        }
    }
    
    /**
     * Adds a new task and saves to file.
     */
    public void addTask(Task task) {
        // Auto-generate ID if not set
        if (task.getId() == 0) {
            int maxId = tasks.stream()
                    .mapToInt(Task::getId)
                    .max()
                    .orElse(0);
            task.setId(maxId + 1);
        }
        tasks.add(task);
        saveTasks();
    }
    
    /**
     * Updates an existing task and saves to file.
     */
    public void updateTask(Task task) {
        for (int i = 0; i < tasks.size(); i++) {
            if (tasks.get(i).getId() == task.getId()) {
                tasks.set(i, task);
                saveTasks();
                return;
            }
        }
    }
    
    /**
     * Finds a task by ID.
     */
    public Task findTask(int taskId) {
        for (Task task : tasks) {
            if (task.getId() == taskId) {
                return task;
            }
        }
        return null;
    }
    
    /**
     * Gets all tasks.
     */
    public List<Task> getAllTasks() {
        return new ArrayList<>(tasks);
    }
    
    /**
     * Gets tasks assigned to a specific child.
     */
    public List<Task> getTasksForChild(String childUsername) {
        List<Task> childTasks = new ArrayList<>();
        for (Task task : tasks) {
            if (task.getAssignedTo().equals(childUsername)) {
                childTasks.add(task);
            }
        }
        return childTasks;
    }
    
    /**
     * Gets tasks with a specific status.
     */
    public List<Task> getTasksByStatus(String status) {
        List<Task> filteredTasks = new ArrayList<>();
        for (Task task : tasks) {
            if (task.getStatus().equals(status)) {
                filteredTasks.add(task);
            }
        }
        return filteredTasks;
    }
    
    // ========== Wish Management ==========
    
    /**
     * Loads wishes from Wishes.txt file.
     */
    public void loadWishes() {
        wishes.clear();
        File file = new File(WISHES_FILE);
        if (!file.exists()) {
            return;
        }
        
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty() || line.startsWith("#")) {
                    continue; // Skip empty lines and comments
                }
                
                Wish wish = Wish.fromCSV(line);
                if (wish != null) {
                    wishes.add(wish);
                }
            }
        } catch (IOException e) {
            System.err.println("Error loading wishes: " + e.getMessage());
        }
    }
    
    /**
     * Saves wishes to Wishes.txt file.
     * Creates the file if it doesn't exist.
     */
    public void saveWishes() {
        ensureFileExists(WISHES_FILE);
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(WISHES_FILE))) {
            for (Wish wish : wishes) {
                writer.write(wish.toCSV());
                writer.newLine();
            }
        } catch (IOException e) {
            System.err.println("Error saving wishes: " + e.getMessage());
        }
    }
    
    /**
     * Adds a new wish and saves to file.
     */
    public void addWish(Wish wish) {
        // Auto-generate ID if not set
        if (wish.getId() == 0) {
            int maxId = wishes.stream()
                    .mapToInt(Wish::getId)
                    .max()
                    .orElse(0);
            wish.setId(maxId + 1);
        }
        wishes.add(wish);
        saveWishes();
    }
    
    /**
     * Updates an existing wish and saves to file.
     */
    public void updateWish(Wish wish) {
        for (int i = 0; i < wishes.size(); i++) {
            if (wishes.get(i).getId() == wish.getId()) {
                wishes.set(i, wish);
                saveWishes();
                return;
            }
        }
    }
    
    /**
     * Finds a wish by ID.
     */
    public Wish findWish(int wishId) {
        for (Wish wish : wishes) {
            if (wish.getId() == wishId) {
                return wish;
            }
        }
        return null;
    }
    
    /**
     * Gets all wishes.
     */
    public List<Wish> getAllWishes() {
        return new ArrayList<>(wishes);
    }
    
    /**
     * Gets wishes requested by a specific child.
     */
    public List<Wish> getWishesForChild(String childUsername) {
        List<Wish> childWishes = new ArrayList<>();
        for (Wish wish : wishes) {
            if (wish.getRequestedBy().equals(childUsername)) {
                childWishes.add(wish);
            }
        }
        return childWishes;
    }
    
    /**
     * Gets wishes with a specific status.
     */
    public List<Wish> getWishesByStatus(String status) {
        List<Wish> filteredWishes = new ArrayList<>();
        for (Wish wish : wishes) {
            if (wish.getStatus().equals(status)) {
                filteredWishes.add(wish);
            }
        }
        return filteredWishes;
    }
}
