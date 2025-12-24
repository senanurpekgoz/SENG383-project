package kidtask.gui;

import kidtask.data.DataManager;
import kidtask.models.Child;
import kidtask.models.Task;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.time.LocalDate;
import java.util.List;

/**
 * Dashboard panel for Parent users.
 * Allows parents to add new tasks and approve completed tasks.
 */
public class ParentDashboardPanel extends JPanel {
    private MainFrame mainFrame;
    private DataManager dataManager;
    
    // Form components
    private JTextField titleField;
    private JTextField pointsField;
    private JComboBox<String> childComboBox;
    private JButton addTaskButton;
    
    // Table components
    private JTable completedTasksTable;
    private DefaultTableModel tableModel;
    
    public ParentDashboardPanel(MainFrame mainFrame) {
        this.mainFrame = mainFrame;
        try {
            // Initialize DataManager first
            this.dataManager = new DataManager();
            
            // Try to load data, but don't fail if it doesn't exist yet
            try {
                this.dataManager.loadAllData();
            } catch (Exception loadException) {
                System.err.println("Warning: Could not load existing data: " + loadException.getMessage());
                loadException.printStackTrace();
                // Continue anyway - data files might not exist yet
            }
            
            // Initialize the panel UI
            initializePanel();
            
        } catch (Exception e) {
            System.err.println("Error initializing ParentDashboardPanel: " + e.getMessage());
            e.printStackTrace();
            // Initialize with basic panel structure to prevent blocking
            setLayout(new BorderLayout());
            setBackground(new Color(240, 248, 255));
            
            JPanel errorPanel = new JPanel(new BorderLayout());
            errorPanel.setBackground(new Color(240, 248, 255));
            JLabel errorLabel = new JLabel("<html><center>Error loading dashboard.<br>Please check console for details.</center></html>", JLabel.CENTER);
            errorLabel.setFont(new Font("Arial", Font.PLAIN, 14));
            errorPanel.add(errorLabel, BorderLayout.CENTER);
            
            JButton retryButton = new JButton("Retry");
            retryButton.addActionListener(evt -> {
                // Remove error panel and try to reinitialize
                removeAll();
                revalidate();
                repaint();
                // Recreate the panel
                try {
                    this.dataManager = new DataManager();
                    this.dataManager.loadAllData();
                    initializePanel();
                    revalidate();
                    repaint();
                } catch (Exception ex) {
                    System.err.println("Retry failed: " + ex.getMessage());
                    ex.printStackTrace();
                }
            });
            
            JPanel buttonPanel = new JPanel(new FlowLayout());
            buttonPanel.setBackground(new Color(240, 248, 255));
            buttonPanel.add(retryButton);
            errorPanel.add(buttonPanel, BorderLayout.SOUTH);
            
            add(errorPanel, BorderLayout.CENTER);
        }
    }
    
    /**
     * Refreshes all data when the panel is shown.
     * This method can be called when switching to this panel.
     */
    public void refreshData() {
        try {
            if (dataManager != null) {
                dataManager.loadAllData();
                loadChildrenIntoComboBox();
                refreshCompletedTasksTable();
            }
        } catch (Exception e) {
            System.err.println("Error refreshing parent dashboard data: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * Initializes the parent dashboard panel.
     */
    private void initializePanel() {
        try {
            setLayout(new BorderLayout());
            setBackground(new Color(240, 248, 255));
            
            // Header panel
            JPanel headerPanel = createHeaderPanel();
            
            // Split pane for form and table
            JSplitPane splitPane = createSplitPane();
            
            add(headerPanel, BorderLayout.NORTH);
            add(splitPane, BorderLayout.CENTER);
        } catch (Exception e) {
            System.err.println("Error in initializePanel: " + e.getMessage());
            e.printStackTrace();
            throw e; // Re-throw to be caught by constructor
        }
    }
    
    /**
     * Creates the header panel with title and back button.
     */
    private JPanel createHeaderPanel() {
        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setBackground(new Color(144, 238, 144));
        headerPanel.setBorder(BorderFactory.createEmptyBorder(15, 20, 15, 20));
        
        JLabel titleLabel = new JLabel("Parent Dashboard", JLabel.LEFT);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 24));
        titleLabel.setForeground(Color.WHITE);
        
        JButton backButton = new JButton("Back to Login");
        backButton.addActionListener(e -> mainFrame.showLoginPanel());
        
        JButton refreshButton = new JButton("Refresh");
        refreshButton.addActionListener(e -> refreshData());
        
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 5, 0));
        buttonPanel.setOpaque(false);
        buttonPanel.add(refreshButton);
        buttonPanel.add(backButton);
        
        headerPanel.add(titleLabel, BorderLayout.WEST);
        headerPanel.add(buttonPanel, BorderLayout.EAST);
        
        return headerPanel;
    }
    
    /**
     * Creates the split pane with form on left and table on right.
     */
    private JSplitPane createSplitPane() {
        JSplitPane splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
        splitPane.setDividerLocation(400);
        splitPane.setResizeWeight(0.4);
        splitPane.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        // Left side: Add Task Form
        JPanel formPanel = createAddTaskForm();
        
        // Right side: Completed Tasks Table
        JPanel tablePanel = createCompletedTasksTable();
        
        splitPane.setLeftComponent(formPanel);
        splitPane.setRightComponent(tablePanel);
        
        return splitPane;
    }
    
    /**
     * Creates the form panel for adding new tasks.
     */
    private JPanel createAddTaskForm() {
        JPanel formPanel = new JPanel();
        formPanel.setLayout(new BoxLayout(formPanel, BoxLayout.Y_AXIS));
        formPanel.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createEtchedBorder(), "Add New Task"));
        formPanel.setBackground(Color.WHITE);
        formPanel.setPreferredSize(new Dimension(380, 600));
        
        // Title field
        JPanel titlePanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        titlePanel.setBackground(Color.WHITE);
        JLabel titleLabel = new JLabel("Title:");
        titleLabel.setPreferredSize(new Dimension(80, 25));
        titleField = new JTextField(20);
        titlePanel.add(titleLabel);
        titlePanel.add(titleField);
        
        // Points field
        JPanel pointsPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        pointsPanel.setBackground(Color.WHITE);
        JLabel pointsLabel = new JLabel("Points:");
        pointsLabel.setPreferredSize(new Dimension(80, 25));
        pointsField = new JTextField(20);
        pointsPanel.add(pointsLabel);
        pointsPanel.add(pointsField);
        
        // Child selection
        JPanel childPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        childPanel.setBackground(Color.WHITE);
        JLabel childLabel = new JLabel("Assign To:");
        childLabel.setPreferredSize(new Dimension(80, 25));
        childComboBox = new JComboBox<>();
        loadChildrenIntoComboBox();
        childPanel.add(childLabel);
        childPanel.add(childComboBox);
        
        // Add Task button
        addTaskButton = new JButton("Add Task");
        addTaskButton.setFont(new Font("Arial", Font.BOLD, 14));
        addTaskButton.setBackground(new Color(144, 238, 144));
        addTaskButton.setForeground(Color.WHITE);
        addTaskButton.setPreferredSize(new Dimension(150, 35));
        addTaskButton.addActionListener(new AddTaskActionListener());
        
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));
        buttonPanel.setBackground(Color.WHITE);
        buttonPanel.add(addTaskButton);
        
        // Add components to form panel
        formPanel.add(Box.createVerticalStrut(20));
        formPanel.add(titlePanel);
        formPanel.add(Box.createVerticalStrut(15));
        formPanel.add(pointsPanel);
        formPanel.add(Box.createVerticalStrut(15));
        formPanel.add(childPanel);
        formPanel.add(Box.createVerticalStrut(30));
        formPanel.add(buttonPanel);
        formPanel.add(Box.createVerticalGlue());
        
        return formPanel;
    }
    
    /**
     * Loads children into the combo box.
     */
    private void loadChildrenIntoComboBox() {
        if (childComboBox == null) {
            return; // Component not initialized yet
        }
        
        try {
            childComboBox.removeAllItems();
            if (dataManager != null) {
                List<Child> children = dataManager.getAllChildren();
                for (Child child : children) {
                    if (child != null && child.getUsername() != null) {
                        childComboBox.addItem(child.getUsername());
                    }
                }
                if (children.isEmpty()) {
                    childComboBox.addItem("No children available");
                    if (addTaskButton != null) {
                        addTaskButton.setEnabled(false);
                    }
                } else {
                    if (addTaskButton != null) {
                        addTaskButton.setEnabled(true);
                    }
                }
            } else {
                childComboBox.addItem("No children available");
                if (addTaskButton != null) {
                    addTaskButton.setEnabled(false);
                }
            }
        } catch (Exception e) {
            System.err.println("Error loading children into combo box: " + e.getMessage());
            e.printStackTrace();
            if (childComboBox != null) {
                childComboBox.addItem("Error loading children");
            }
        }
    }
    
    /**
     * Creates the completed tasks table panel.
     */
    private JPanel createCompletedTasksTable() {
        JPanel tablePanel = new JPanel(new BorderLayout());
        tablePanel.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createEtchedBorder(), "Completed Tasks - Awaiting Approval"));
        tablePanel.setBackground(Color.WHITE);
        
        // Create table model
        String[] columnNames = {"ID", "Title", "Points", "Assigned To", "Approve"};
        tableModel = new DefaultTableModel(columnNames, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return column == 4; // Only Approve button column is "editable"
            }
        };
        
        completedTasksTable = new JTable(tableModel);
        completedTasksTable.setRowHeight(30);
        completedTasksTable.getColumnModel().getColumn(0).setPreferredWidth(50);
        completedTasksTable.getColumnModel().getColumn(1).setPreferredWidth(200);
        completedTasksTable.getColumnModel().getColumn(2).setPreferredWidth(80);
        completedTasksTable.getColumnModel().getColumn(3).setPreferredWidth(120);
        completedTasksTable.getColumnModel().getColumn(4).setPreferredWidth(100);
        
        // Add button renderer and editor for Approve column
        completedTasksTable.getColumn("Approve").setCellRenderer(new ButtonRenderer());
        completedTasksTable.getColumn("Approve").setCellEditor(new ButtonEditor(new JCheckBox()));
        
        JScrollPane scrollPane = new JScrollPane(completedTasksTable);
        scrollPane.setPreferredSize(new Dimension(500, 600));
        
        tablePanel.add(scrollPane, BorderLayout.CENTER);
        
        // Load initial data
        refreshCompletedTasksTable();
        
        return tablePanel;
    }
    
    /**
     * Refreshes the completed tasks table with current data.
     */
    private void refreshCompletedTasksTable() {
        if (tableModel == null) {
            return; // Component not initialized yet
        }
        
        try {
            // Clear existing rows
            tableModel.setRowCount(0);
            
            if (dataManager != null) {
                // Load completed tasks
                dataManager.loadTasks();
                List<Task> completedTasks = dataManager.getTasksByStatus("Completed");
                
                // Add tasks to table
                for (Task task : completedTasks) {
                    if (task != null) {
                        Object[] rowData = {
                            task.getId(),
                            task.getTitle() != null ? task.getTitle() : "",
                            task.getPoints(),
                            task.getAssignedTo() != null ? task.getAssignedTo() : "",
                            "Approve"
                        };
                        tableModel.addRow(rowData);
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("Error refreshing completed tasks table: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * Action listener for Add Task button.
     */
    private class AddTaskActionListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            String title = titleField.getText().trim();
            String pointsText = pointsField.getText().trim();
            String assignedTo = (String) childComboBox.getSelectedItem();
            
            // Validation
            if (title.isEmpty()) {
                JOptionPane.showMessageDialog(ParentDashboardPanel.this,
                    "Please enter a task title.", "Validation Error", JOptionPane.WARNING_MESSAGE);
                return;
            }
            
            if (pointsText.isEmpty()) {
                JOptionPane.showMessageDialog(ParentDashboardPanel.this,
                    "Please enter points for the task.", "Validation Error", JOptionPane.WARNING_MESSAGE);
                return;
            }
            
            int points;
            try {
                points = Integer.parseInt(pointsText);
                if (points <= 0) {
                    throw new NumberFormatException();
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(ParentDashboardPanel.this,
                    "Please enter a valid positive number for points.", 
                    "Validation Error", JOptionPane.WARNING_MESSAGE);
                return;
            }
            
            if (assignedTo == null || assignedTo.equals("No children available")) {
                JOptionPane.showMessageDialog(ParentDashboardPanel.this,
                    "Please select a child to assign the task to.", 
                    "Validation Error", JOptionPane.WARNING_MESSAGE);
                return;
            }
            
            // Create new task
            Task newTask = new Task(0, title, "", LocalDate.now().plusDays(7), 
                                   points, "Parent", assignedTo);
            
            // Add task to data manager
            dataManager.addTask(newTask);
            
            // Clear form
            titleField.setText("");
            pointsField.setText("");
            
            // Show success message
            JOptionPane.showMessageDialog(ParentDashboardPanel.this,
                "Task added successfully!", "Success", JOptionPane.INFORMATION_MESSAGE);
        }
    }
    
    /**
     * Button renderer for the table.
     */
    private class ButtonRenderer extends JButton implements javax.swing.table.TableCellRenderer {
        public ButtonRenderer() {
            setOpaque(true);
        }
        
        @Override
        public Component getTableCellRendererComponent(JTable table, Object value,
                boolean isSelected, boolean hasFocus, int row, int column) {
            setText((value == null) ? "" : value.toString());
            setBackground(new Color(144, 238, 144));
            setForeground(Color.WHITE);
            setFont(new Font("Arial", Font.BOLD, 12));
            return this;
        }
    }
    
    /**
     * Button editor for the table.
     */
    private class ButtonEditor extends javax.swing.DefaultCellEditor {
        protected JButton button;
        private String label;
        private boolean isPushed;
        private int selectedRow;
        
        public ButtonEditor(JCheckBox checkBox) {
            super(checkBox);
            button = new JButton();
            button.setOpaque(true);
            button.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    fireEditingStopped();
                }
            });
        }
        
        @Override
        public Component getTableCellEditorComponent(JTable table, Object value,
                boolean isSelected, int row, int column) {
            label = (value == null) ? "" : value.toString();
            button.setText(label);
            button.setBackground(new Color(144, 238, 144));
            button.setForeground(Color.WHITE);
            isPushed = true;
            selectedRow = row;
            return button;
        }
        
        @Override
        public Object getCellEditorValue() {
            if (isPushed) {
                // Handle approve action
                int taskId = (Integer) tableModel.getValueAt(selectedRow, 0);
                approveTask(taskId);
            }
            isPushed = false;
            return label;
        }
        
        @Override
        public boolean stopCellEditing() {
            isPushed = false;
            return super.stopCellEditing();
        }
    }
    
    /**
     * Approves a completed task and updates the child's points.
     */
    private void approveTask(int taskId) {
        Task task = dataManager.findTask(taskId);
        if (task == null) {
            JOptionPane.showMessageDialog(this,
                "Task not found.", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }
        
        if (!task.getStatus().equals("Completed")) {
            JOptionPane.showMessageDialog(this,
                "This task is not in Completed status.", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }
        
        // Update task status
        task.setStatus("Approved");
        dataManager.updateTask(task);
        
        // Update child's points
        kidtask.models.User user = dataManager.findUser(task.getAssignedTo());
        if (user instanceof kidtask.models.Child) {
            kidtask.models.Child child = (kidtask.models.Child) user;
            child.addPoints(task.getPoints());
            dataManager.updateUser(child);
        }
        
        // Refresh table
        refreshCompletedTasksTable();
        
        JOptionPane.showMessageDialog(this,
            "Task approved! Points have been added to " + task.getAssignedTo() + ".", 
            "Success", JOptionPane.INFORMATION_MESSAGE);
    }
}

