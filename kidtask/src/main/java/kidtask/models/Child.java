package kidtask.models;

/**
 * Represents a Child user who can complete tasks to earn points
 * and request wishes (rewards).
 */
public class Child extends User {
    private int totalPoints;
    private int currentLevel;
    
    public Child() {
        super();
        this.role = "Child";
        this.totalPoints = 0;
        this.currentLevel = 1;
    }
    
    public Child(String username, String password) {
        super(username, password, "Child");
        this.totalPoints = 0;
        this.currentLevel = 1;
    }
    
    public Child(String username, String password, int totalPoints, int currentLevel) {
        super(username, password, "Child");
        this.totalPoints = totalPoints;
        this.currentLevel = currentLevel;
    }
    
    public int getTotalPoints() {
        return totalPoints;
    }
    
    public void setTotalPoints(int totalPoints) {
        this.totalPoints = totalPoints;
        // Update level based on points (simple formula: level = points / 100 + 1)
        this.currentLevel = (totalPoints / 100) + 1;
    }
    
    public void addPoints(int points) {
        this.totalPoints += points;
        // Update level based on points
        this.currentLevel = (totalPoints / 100) + 1;
    }
    
    public int getCurrentLevel() {
        return currentLevel;
    }
    
    public void setCurrentLevel(int currentLevel) {
        this.currentLevel = currentLevel;
    }
    
    /**
     * Converts Child to CSV format for file storage.
     * Format: username,password,role,totalPoints,currentLevel
     */
    @Override
    public String toCSV() {
        return username + "," + password + "," + role + "," + totalPoints + "," + currentLevel;
    }
    
    /**
     * Creates a Child from CSV line.
     * Format: username,password,role,totalPoints,currentLevel
     */
    public static Child fromCSV(String csvLine) {
        String[] parts = csvLine.split(",");
        if (parts.length < 3) {
            return null;
        }
        
        String username = parts[0].trim();
        String password = parts[1].trim();
        
        if (parts.length >= 5) {
            try {
                int totalPoints = Integer.parseInt(parts[3].trim());
                int currentLevel = Integer.parseInt(parts[4].trim());
                return new Child(username, password, totalPoints, currentLevel);
            } catch (NumberFormatException e) {
                return new Child(username, password);
            }
        }
        
        return new Child(username, password);
    }
    
    @Override
    public String toString() {
        return "Child{username='" + username + "', totalPoints=" + totalPoints + 
               ", currentLevel=" + currentLevel + "}";
    }
}

