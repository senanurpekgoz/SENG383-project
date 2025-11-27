package kidtask.models;

/**
 * Represents a Teacher user who can create tasks and approve
 * completed tasks and wishes.
 */
public class Teacher extends User {
    
    public Teacher() {
        super();
        this.role = "Teacher";
    }
    
    public Teacher(String username, String password) {
        super(username, password, "Teacher");
    }
    
    @Override
    public String toString() {
        return "Teacher{username='" + username + "'}";
    }
}

