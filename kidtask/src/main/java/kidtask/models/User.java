package kidtask.models;

/**
 * Base class for all users in the KidTask application.
 * Supports different roles: Child, Parent, and Teacher.
 */
public class User {
    protected String username;
    protected String password;
    protected String role; // "Child", "Parent", or "Teacher"
    
    public User() {
    }
    
    public User(String username, String password, String role) {
        this.username = username;
        this.password = password;
        this.role = role;
    }
    
    public String getUsername() {
        return username;
    }
    
    public void setUsername(String username) {
        this.username = username;
    }
    
    public String getPassword() {
        return password;
    }
    
    public void setPassword(String password) {
        this.password = password;
    }
    
    public String getRole() {
        return role;
    }
    
    public void setRole(String role) {
        this.role = role;
    }
    
    /**
     * Converts User to CSV format for file storage.
     * Format: username,password,role
     */
    public String toCSV() {
        return username + "," + password + "," + role;
    }
    
    /**
     * Creates a User from CSV line.
     * Format: username,password,role
     */
    public static User fromCSV(String csvLine) {
        String[] parts = csvLine.split(",");
        if (parts.length < 3) {
            return null;
        }
        
        String username = parts[0].trim();
        String password = parts[1].trim();
        String role = parts[2].trim();
        
        switch (role) {
            case "Child":
                return new Child(username, password);
            case "Parent":
                return new Parent(username, password);
            case "Teacher":
                return new Teacher(username, password);
            default:
                return new User(username, password, role);
        }
    }
    
    @Override
    public String toString() {
        return "User{username='" + username + "', role='" + role + "'}";
    }
}

