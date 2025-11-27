package kidtask.models;

/**
 * Represents a Parent user who can create tasks and approve
 * completed tasks and wishes.
 */
public class Parent extends User {
    
    public Parent() {
        super();
        this.role = "Parent";
    }
    
    public Parent(String username, String password) {
        super(username, password, "Parent");
    }
    
    @Override
    public String toString() {
        return "Parent{username='" + username + "'}";
    }
}

