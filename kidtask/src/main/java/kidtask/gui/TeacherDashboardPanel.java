package kidtask.gui;

import kidtask.data.DataManager;
import kidtask.models.Child;
import kidtask.models.Task;
import kidtask.models.Wish;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.time.LocalDate;
import java.util.List;

/**
 * Dashboard panel for Teacher users.
 * Allows teachers to add tasks, approve completed tasks, and manage wishes.
 */
public class TeacherDashboardPanel extends JPanel {
    private MainFrame mainFrame;
    private DataManager dataManager;
    
    // Form components
    private JTextField titleField;
    private JTextField pointsField;
    private JComboBox<String> childComboBox;
    private JButton addTaskButton;
    
    // Table components
    private JTable completedTasksTable;
    private DefaultTableModel tasksTableModel;
    private JTable wishesTable;
    private DefaultTableModel wishesTableModel;
    
    public TeacherDashboardPanel(MainFrame mainFrame) {
        this.mainFrame = mainFrame;
        try {
            this.dataManager = new DataManager();
            try {
                this.dataManager.loadAllData();
            } catch (Exception loadException) {
                System.err.println("Warning: Could not load existing data: " + loadException.getMessage());
            }
            initializePanel();
        } catch (Exception e) {
            System.err.println("Error initializing TeacherDashboardPanel: " + e.getMessage());
            e.printStackTrace();
            setLayout(new BorderLayout());
            add(new JLabel("Error loading dashboard. Please check console."), BorderLayout.CENTER);
        }
    }
    
    /**
     * Refreshes all data when the panel is shown.
     */
    public void refreshData() {
        try {
            if (dataManager != null) {
                dataManager.loadAllData();
                loadChildrenIntoComboBox();
                refreshCompletedTasksTable();
                refreshWishesTable();
            }
        } catch (Exception e) {
            System.err.println("Error refreshing teacher dashboard data: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * Initializes the teacher dashboard panel.
     */
    private void initializePanel() {
        try {
            setLayout(new BorderLayout());
            setBackground(new Color(240, 248, 255));
            
            // Header panel
            JPanel headerPanel = createHeaderPanel();
            
            // Main content with tabbed pane
            JTabbedPane tabbedPane = new JTabbedPane();
            
            // Tab 1: Tasks
            JPanel tasksTab = createTasksTab();
            tabbedPane.addTab("Tasks", tasksTab);
            
            // Tab 2: Wishes
            JPanel wishesTab = createWishesTab();
            tabbedPane.addTab("Wishes", wishesTab);
            
            add(headerPanel, BorderLayout.NORTH);
            add(tabbedPane, BorderLayout.CENTER);
            
            // Initial data load
            refreshData();
        } catch (Exception e) {
            System.err.println("Error in initializePanel: " + e.getMessage());
            e.printStackTrace();
            throw e;
        }
    }
    
    /**
     * Creates the header panel.
     */
    private JPanel createHeaderPanel() {
        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setBackground(new Color(255, 182, 193));
        headerPanel.setBorder(BorderFactory.createEmptyBorder(15, 20, 15, 20));
        
        JLabel titleLabel = new JLabel("Teacher Dashboard", JLabel.LEFT);
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
     * Creates the tasks tab.
     */
    private JPanel createTasksTab() {
        JPanel tasksTab = new JPanel(new BorderLayout());
        tasksTab.setBackground(new Color(240, 248, 255));
        
        // Split pane: Form on left, Table on right
        JSplitPane splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
        splitPane.setDividerLocation(400);
        splitPane.setResizeWeight(0.4);
        splitPane.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        // Left: Add Task Form
        JPanel formPanel = createAddTaskForm();
        
        // Right: Completed Tasks Table
        JPanel tablePanel = createCompletedTasksTable();
        
        splitPane.setLeftComponent(formPanel);
        splitPane.setRightComponent(tablePanel);
        
        tasksTab.add(splitPane, BorderLayout.CENTER);
        
        return tasksTab;
    }
    
    /**
     * Creates the wishes tab.
     */
    private JPanel createWishesTab() {
        JPanel wishesTab = new JPanel(new BorderLayout());
        wishesTab.setBackground(new Color(240, 248, 255));
        wishesTab.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        JPanel wishesTablePanel = createWishesManagementTable();
        wishesTab.add(wishesTablePanel, BorderLayout.CENTER);
        
        return wishesTab;
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
        addTaskButton.setBackground(new Color(255, 182, 193));
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
     * Creates the completed tasks table panel.
     */
    private JPanel createCompletedTasksTable() {
        JPanel tablePanel = new JPanel(new BorderLayout());
        tablePanel.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createEtchedBorder(), "Completed Tasks - Awaiting Approval"));
        tablePanel.setBackground(Color.WHITE);
        
        String[] columnNames = {"ID", "Title", "Points", "Assigned To", "Approve"};
        tasksTableModel = new DefaultTableModel(columnNames, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return column == 4;
            }
        };
        
        completedTasksTable = new JTable(tasksTableModel);
        completedTasksTable.setRowHeight(30);
        completedTasksTable.getColumnModel().getColumn(0).setPreferredWidth(50);
        completedTasksTable.getColumnModel().getColumn(1).setPreferredWidth(200);
        completedTasksTable.getColumnModel().getColumn(2).setPreferredWidth(80);
        completedTasksTable.getColumnModel().getColumn(3).setPreferredWidth(120);
        completedTasksTable.getColumnModel().getColumn(4).setPreferredWidth(100);
        
        // Add button renderer and editor
        completedTasksTable.getColumn("Approve").setCellRenderer(new ButtonRenderer(new Color(255, 182, 193)));
        completedTasksTable.getColumn("Approve").setCellEditor(new TaskButtonEditor(new JCheckBox()));
        
        JScrollPane scrollPane = new JScrollPane(completedTasksTable);
        scrollPane.setPreferredSize(new Dimension(500, 600));
        
        tablePanel.add(scrollPane, BorderLayout.CENTER);
        
        return tablePanel;
    }
    
    /**
     * Creates the wishes management table.
     */
    private JPanel createWishesManagementTable() {
        JPanel tablePanel = new JPanel(new BorderLayout());
        tablePanel.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createEtchedBorder(), "Wishes - Awaiting Approval"));
        tablePanel.setBackground(Color.WHITE);
        
        String[] columnNames = {"ID", "Wish Name", "Required Level", "Requested By", "Status", "Approve", "Reject"};
        wishesTableModel = new DefaultTableModel(columnNames, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return column == 5 || column == 6;
            }
        };
        
        wishesTable = new JTable(wishesTableModel);
        wishesTable.setRowHeight(30);
        wishesTable.getColumnModel().getColumn(0).setPreferredWidth(50);
        wishesTable.getColumnModel().getColumn(1).setPreferredWidth(200);
        wishesTable.getColumnModel().getColumn(2).setPreferredWidth(100);
        wishesTable.getColumnModel().getColumn(3).setPreferredWidth(120);
        wishesTable.getColumnModel().getColumn(4).setPreferredWidth(100);
        wishesTable.getColumnModel().getColumn(5).setPreferredWidth(80);
        wishesTable.getColumnModel().getColumn(6).setPreferredWidth(80);
        
        // Add button renderers and editors
        wishesTable.getColumn("Approve").setCellRenderer(new ButtonRenderer(new Color(144, 238, 144)));
        wishesTable.getColumn("Approve").setCellEditor(new WishApproveEditor(new JCheckBox()));
        
        wishesTable.getColumn("Reject").setCellRenderer(new ButtonRenderer(new Color(255, 99, 71)));
        wishesTable.getColumn("Reject").setCellEditor(new WishRejectEditor(new JCheckBox()));
        
        JScrollPane scrollPane = new JScrollPane(wishesTable);
        tablePanel.add(scrollPane, BorderLayout.CENTER);
        
        return tablePanel;
    }
    
    /**
     * Loads children into the combo box.
     */
    private void loadChildrenIntoComboBox() {
        if (childComboBox == null) return;
        
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
            }
        } catch (Exception e) {
            System.err.println("Error loading children: " + e.getMessage());
        }
    }
    
    /**
     * Refreshes the completed tasks table.
     */
    private void refreshCompletedTasksTable() {
        if (tasksTableModel == null) return;
        
        try {
            tasksTableModel.setRowCount(0);
            
            if (dataManager != null) {
                dataManager.loadTasks();
                List<Task> completedTasks = dataManager.getTasksByStatus("Completed");
                
                for (Task task : completedTasks) {
                    if (task != null) {
                        Object[] rowData = {
                            task.getId(),
                            task.getTitle() != null ? task.getTitle() : "",
                            task.getPoints(),
                            task.getAssignedTo() != null ? task.getAssignedTo() : "",
                            "Approve"
                        };
                        tasksTableModel.addRow(rowData);
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("Error refreshing completed tasks table: " + e.getMessage());
        }
    }
    
    /**
     * Refreshes the wishes table.
     */
    private void refreshWishesTable() {
        if (wishesTableModel == null) return;
        
        try {
            wishesTableModel.setRowCount(0);
            
            if (dataManager != null) {
                dataManager.loadWishes();
                List<Wish> wishes = dataManager.getWishesByStatus("Requested");
                
                for (Wish wish : wishes) {
                    if (wish != null) {
                        Object[] rowData = {
                            wish.getId(),
                            wish.getItemName() != null ? wish.getItemName() : "",
                            wish.getRequiredLevel(),
                            wish.getRequestedBy() != null ? wish.getRequestedBy() : "",
                            wish.getStatus(),
                            "Approve",
                            "Reject"
                        };
                        wishesTableModel.addRow(rowData);
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("Error refreshing wishes table: " + e.getMessage());
        }
    }
    
    /**
     * Approves a completed task.
     */
    private void approveTask(int taskId) {
        try {
            Task task = dataManager.findTask(taskId);
            if (task == null || !task.getStatus().equals("Completed")) {
                return;
            }
            
            task.setStatus("Approved");
            dataManager.updateTask(task);
            
            // Update child's points
            kidtask.models.User user = dataManager.findUser(task.getAssignedTo());
            if (user instanceof Child) {
                Child child = (Child) user;
                child.addPoints(task.getPoints());
                dataManager.updateUser(child);
            }
            
            refreshCompletedTasksTable();
            
            JOptionPane.showMessageDialog(this,
                "Task approved! Points added to " + task.getAssignedTo() + ".", 
                "Success", JOptionPane.INFORMATION_MESSAGE);
        } catch (Exception e) {
            System.err.println("Error approving task: " + e.getMessage());
            JOptionPane.showMessageDialog(this,
                "Error: " + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
    
    /**
     * Approves a wish.
     */
    private void approveWish(int wishId) {
        try {
            Wish wish = dataManager.findWish(wishId);
            if (wish == null || !wish.getStatus().equals("Requested")) {
                return;
            }
            
            wish.setStatus("Approved");
            dataManager.updateWish(wish);
            
            refreshWishesTable();
            
            JOptionPane.showMessageDialog(this,
                "Wish approved!", "Success", JOptionPane.INFORMATION_MESSAGE);
        } catch (Exception e) {
            System.err.println("Error approving wish: " + e.getMessage());
            JOptionPane.showMessageDialog(this,
                "Error: " + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
    
    /**
     * Rejects a wish.
     */
    private void rejectWish(int wishId) {
        try {
            Wish wish = dataManager.findWish(wishId);
            if (wish == null || !wish.getStatus().equals("Requested")) {
                return;
            }
            
            wish.setStatus("Rejected");
            dataManager.updateWish(wish);
            
            refreshWishesTable();
            
            JOptionPane.showMessageDialog(this,
                "Wish rejected.", "Info", JOptionPane.INFORMATION_MESSAGE);
        } catch (Exception e) {
            System.err.println("Error rejecting wish: " + e.getMessage());
            JOptionPane.showMessageDialog(this,
                "Error: " + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
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
            
            if (title.isEmpty()) {
                JOptionPane.showMessageDialog(TeacherDashboardPanel.this,
                    "Please enter a task title.", "Validation Error", JOptionPane.WARNING_MESSAGE);
                return;
            }
            
            if (pointsText.isEmpty()) {
                JOptionPane.showMessageDialog(TeacherDashboardPanel.this,
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
                JOptionPane.showMessageDialog(TeacherDashboardPanel.this,
                    "Please enter a valid positive number for points.", 
                    "Validation Error", JOptionPane.WARNING_MESSAGE);
                return;
            }
            
            if (assignedTo == null || assignedTo.equals("No children available")) {
                JOptionPane.showMessageDialog(TeacherDashboardPanel.this,
                    "Please select a child to assign the task to.", 
                    "Validation Error", JOptionPane.WARNING_MESSAGE);
                return;
            }
            
            try {
                Task newTask = new Task(0, title, "", LocalDate.now().plusDays(7), 
                                       points, "Teacher", assignedTo);
                dataManager.addTask(newTask);
                
                titleField.setText("");
                pointsField.setText("");
                
                JOptionPane.showMessageDialog(TeacherDashboardPanel.this,
                    "Task added successfully!", "Success", JOptionPane.INFORMATION_MESSAGE);
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(TeacherDashboardPanel.this,
                    "Error adding task: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }
    
    /**
     * Button renderer for tables.
     */
    private class ButtonRenderer extends JButton implements javax.swing.table.TableCellRenderer {
        private Color buttonColor;
        
        public ButtonRenderer(Color color) {
            this.buttonColor = color;
            setOpaque(true);
        }
        
        @Override
        public Component getTableCellRendererComponent(JTable table, Object value,
                boolean isSelected, boolean hasFocus, int row, int column) {
            setText((value == null) ? "" : value.toString());
            setBackground(buttonColor);
            setForeground(Color.WHITE);
            setFont(new Font("Arial", Font.BOLD, 12));
            return this;
        }
    }
    
    /**
     * Button editor for task approval.
     */
    private class TaskButtonEditor extends javax.swing.DefaultCellEditor {
        protected JButton button;
        private String label;
        private boolean isPushed;
        private int selectedRow;
        
        public TaskButtonEditor(JCheckBox checkBox) {
            super(checkBox);
            button = new JButton();
            button.setOpaque(true);
            button.addActionListener(evt -> fireEditingStopped());
        }
        
        @Override
        public Component getTableCellEditorComponent(JTable table, Object value,
                boolean isSelected, int row, int column) {
            label = (value == null) ? "" : value.toString();
            button.setText(label);
            button.setBackground(new Color(255, 182, 193));
            button.setForeground(Color.WHITE);
            isPushed = true;
            selectedRow = row;
            return button;
        }
        
        @Override
        public Object getCellEditorValue() {
            if (isPushed) {
                int taskId = (Integer) tasksTableModel.getValueAt(selectedRow, 0);
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
     * Button editor for wish approval.
     */
    private class WishApproveEditor extends javax.swing.DefaultCellEditor {
        protected JButton button;
        private String label;
        private boolean isPushed;
        private int selectedRow;
        
        public WishApproveEditor(JCheckBox checkBox) {
            super(checkBox);
            button = new JButton();
            button.setOpaque(true);
            button.addActionListener(evt -> fireEditingStopped());
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
                int wishId = (Integer) wishesTableModel.getValueAt(selectedRow, 0);
                approveWish(wishId);
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
     * Button editor for wish rejection.
     */
    private class WishRejectEditor extends javax.swing.DefaultCellEditor {
        protected JButton button;
        private String label;
        private boolean isPushed;
        private int selectedRow;
        
        public WishRejectEditor(JCheckBox checkBox) {
            super(checkBox);
            button = new JButton();
            button.setOpaque(true);
            button.addActionListener(evt -> fireEditingStopped());
        }
        
        @Override
        public Component getTableCellEditorComponent(JTable table, Object value,
                boolean isSelected, int row, int column) {
            label = (value == null) ? "" : value.toString();
            button.setText(label);
            button.setBackground(new Color(255, 99, 71));
            button.setForeground(Color.WHITE);
            isPushed = true;
            selectedRow = row;
            return button;
        }
        
        @Override
        public Object getCellEditorValue() {
            if (isPushed) {
                int wishId = (Integer) wishesTableModel.getValueAt(selectedRow, 0);
                rejectWish(wishId);
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
}
