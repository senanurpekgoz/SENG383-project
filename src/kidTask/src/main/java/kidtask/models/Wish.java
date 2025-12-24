package kidtask.models;

/**
 * Represents a Wish (reward) that a child can request.
 * Wishes have a required level and can be in different statuses:
 * Requested, Approved, or Rejected.
 */
public class Wish {
    private int id;
    private String itemName;
    private int requiredLevel;
    private String status; // "Requested", "Approved", "Rejected"
    private String requestedBy; // Username of Child who requested the wish
    
    public Wish() {
        this.status = "Requested";
    }
    
    public Wish(int id, String itemName, int requiredLevel, String requestedBy) {
        this.id = id;
        this.itemName = itemName;
        this.requiredLevel = requiredLevel;
        this.status = "Requested";
        this.requestedBy = requestedBy;
    }
    
    public int getId() {
        return id;
    }
    
    public void setId(int id) {
        this.id = id;
    }
    
    public String getItemName() {
        return itemName;
    }
    
    public void setItemName(String itemName) {
        this.itemName = itemName;
    }
    
    public int getRequiredLevel() {
        return requiredLevel;
    }
    
    public void setRequiredLevel(int requiredLevel) {
        this.requiredLevel = requiredLevel;
    }
    
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
    
    public String getRequestedBy() {
        return requestedBy;
    }
    
    public void setRequestedBy(String requestedBy) {
        this.requestedBy = requestedBy;
    }
    
    /**
     * Converts Wish to CSV format for file storage.
     * Format: id,itemName,requiredLevel,status,requestedBy
     */
    public String toCSV() {
        return id + "," + escapeCSV(itemName) + "," + requiredLevel + "," + 
               status + "," + requestedBy;
    }
    
    /**
     * Creates a Wish from CSV line.
     * Format: id,itemName,requiredLevel,status,requestedBy
     */
    public static Wish fromCSV(String csvLine) {
        String[] parts = parseCSVLine(csvLine);
        if (parts.length < 5) {
            return null;
        }
        
        try {
            int id = Integer.parseInt(parts[0].trim());
            String itemName = parts[1].trim();
            int requiredLevel = Integer.parseInt(parts[2].trim());
            String status = parts[3].trim();
            String requestedBy = parts[4].trim();
            
            Wish wish = new Wish(id, itemName, requiredLevel, requestedBy);
            wish.setStatus(status);
            return wish;
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
        return "Wish{id=" + id + ", itemName='" + itemName + "', requiredLevel=" + 
               requiredLevel + ", status='" + status + "', requestedBy='" + requestedBy + "'}";
    }
}

