package kidtask.models;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

/**
 * Represents a Task that can be assigned to children.
 * Tasks can be in different statuses: Pending, Completed, or Approved.
 */
public class Task {
    private int id;
    private String title;
    private String description;
    private LocalDate dueDate;
    private int points;
    private String status; // "Pending", "Completed", "Approved"
    private String assignedBy; // Username of Parent/Teacher who created the task
    private String assignedTo; // Username of Child assigned to this task
    
    private static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ISO_LOCAL_DATE;
    
    public Task() {
        this.status = "Pending";
    }
    
    public Task(int id, String title, String description, LocalDate dueDate, 
                int points, String assignedBy, String assignedTo) {
        this.id = id;
        this.title = title;
        this.description = description;
        this.dueDate = dueDate;
        this.points = points;
        this.status = "Pending";
        this.assignedBy = assignedBy;
        this.assignedTo = assignedTo;
    }
    
    public int getId() {
        return id;
    }
    
    public void setId(int id) {
        this.id = id;
    }
    
    public String getTitle() {
        return title;
    }
    
    public void setTitle(String title) {
        this.title = title;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    public LocalDate getDueDate() {
        return dueDate;
    }
    
    public void setDueDate(LocalDate dueDate) {
        this.dueDate = dueDate;
    }
    
    public int getPoints() {
        return points;
    }
    
    public void setPoints(int points) {
        this.points = points;
    }
    
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
    
    public String getAssignedBy() {
        return assignedBy;
    }
    
    public void setAssignedBy(String assignedBy) {
        this.assignedBy = assignedBy;
    }
    
    public String getAssignedTo() {
        return assignedTo;
    }
    
    public void setAssignedTo(String assignedTo) {
        this.assignedTo = assignedTo;
    }
    
    /**
     * Converts Task to CSV format for file storage.
     * Format: id,title,description,dueDate,points,status,assignedBy,assignedTo
     */
    public String toCSV() {
        String dueDateStr = dueDate != null ? dueDate.format(DATE_FORMATTER) : "";
        return id + "," + escapeCSV(title) + "," + escapeCSV(description) + "," + 
               dueDateStr + "," + points + "," + status + "," + assignedBy + "," + assignedTo;
    }
    
    /**
     * Creates a Task from CSV line.
     * Format: id,title,description,dueDate,points,status,assignedBy,assignedTo
     */
    public static Task fromCSV(String csvLine) {
        String[] parts = parseCSVLine(csvLine);
        if (parts.length < 8) {
            return null;
        }
        
        try {
            int id = Integer.parseInt(parts[0].trim());
            String title = parts[1].trim();
            String description = parts[2].trim();
            LocalDate dueDate = parts[3].trim().isEmpty() ? null : 
                               LocalDate.parse(parts[3].trim(), DATE_FORMATTER);
            int points = Integer.parseInt(parts[4].trim());
            String status = parts[5].trim();
            String assignedBy = parts[6].trim();
            String assignedTo = parts[7].trim();
            
            Task task = new Task(id, title, description, dueDate, points, assignedBy, assignedTo);
            task.setStatus(status);
            return task;
        } catch (Exception e) {
            return null;
        }
    }
    
    /**
     * Escapes commas in CSV fields by wrapping in quotes if necessary.
     */
    private static String escapeCSV(String field) {
        if (field == null) {
            return "";
        }
        if (field.contains(",") || field.contains("\"") || field.contains("\n")) {
            return "\"" + field.replace("\"", "\"\"") + "\"";
        }
        return field;
    }
    
    /**
     * Parses a CSV line handling quoted fields.
     */
    private static String[] parseCSVLine(String line) {
        java.util.List<String> result = new java.util.ArrayList<>();
        boolean inQuotes = false;
        StringBuilder current = new StringBuilder();
        
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (c == '"') {
                if (inQuotes && i + 1 < line.length() && line.charAt(i + 1) == '"') {
                    current.append('"');
                    i++;
                } else {
                    inQuotes = !inQuotes;
                }
            } else if (c == ',' && !inQuotes) {
                result.add(current.toString());
                current = new StringBuilder();
            } else {
                current.append(c);
            }
        }
        result.add(current.toString());
        return result.toArray(new String[0]);
    }
    
    @Override
    public String toString() {
        return "Task{id=" + id + ", title='" + title + "', points=" + points + 
               ", status='" + status + "', assignedTo='" + assignedTo + "'}";
    }
}

