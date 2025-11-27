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
import java.util.List;

/**
 * Dashboard panel for Child users.
 * Allows children to view tasks, mark them as completed, and request wishes.
 */
public class ChildDashboardPanel extends JPanel {
    private MainFrame mainFrame;
    private DataManager dataManager;
    private String currentChildUsername = "Child1"; // Default, should be set based on login
    
    // Components
    private JLabel pointsLabel;
    private JLabel levelLabel;
    private JProgressBar pointsProgressBar;
    private JTable tasksTable;
    private DefaultTableModel tasksTableModel;
    private DefaultTableModel wishesTableModel;
    private JTextField wishNameField;
    private JTextField wishLevelField;
    private JComboBox<String> childSelector;
    
    public ChildDashboardPanel(MainFrame mainFrame) {
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
            System.err.println("Error initializing ChildDashboardPanel: " + e.getMessage());
            e.printStackTrace();
            setLayout(new BorderLayout());
            add(new JLabel("Error loading dashboard. Please check console."), BorderLayout.CENTER);
        }
    }
    
    /**
     * Sets the current child username.
     */
    public void setChildUsername(String username) {
        this.currentChildUsername = username;
        refreshData();
    }
    
    /**
     * Refreshes all data when the panel is shown.
     */
    public void refreshData() {
        try {
            if (dataManager != null) {
                dataManager.loadAllData();
                updateProgressDisplay();
                refreshTasksTable();
                refreshWishesTable();
            }
        } catch (Exception e) {
            System.err.println("Error refreshing child dashboard data: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * Initializes the child dashboard panel.
     */
    private void initializePanel() {
        try {
            setLayout(new BorderLayout());
            setBackground(new Color(240, 248, 255));
            
            // Header panel
            JPanel headerPanel = createHeaderPanel();
            
            // Main content with split pane
            JSplitPane mainSplitPane = new JSplitPane(JSplitPane.VERTICAL_SPLIT);
            mainSplitPane.setDividerLocation(400);
            mainSplitPane.setResizeWeight(0.6);
            mainSplitPane.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
            
            // Top: Progress and Tasks
            JPanel topPanel = createTopPanel();
            
            // Bottom: Wishes
            JPanel bottomPanel = createWishesPanel();
            
            mainSplitPane.setTopComponent(topPanel);
            mainSplitPane.setBottomComponent(bottomPanel);
            
            add(headerPanel, BorderLayout.NORTH);
            add(mainSplitPane, BorderLayout.CENTER);
            
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
        headerPanel.setBackground(new Color(135, 206, 250));
        headerPanel.setBorder(BorderFactory.createEmptyBorder(15, 20, 15, 20));
        
        JLabel titleLabel = new JLabel("Child Dashboard", JLabel.LEFT);
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
     * Creates the top panel with progress and tasks.
     */
    private JPanel createTopPanel() {
        JPanel topPanel = new JPanel(new BorderLayout());
        topPanel.setBackground(new Color(240, 248, 255));
        
        // Left: Progress panel
        JPanel progressPanel = createProgressPanel();
        
        // Right: Tasks table
        JPanel tasksPanel = createTasksPanel();
        
        JSplitPane splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
        splitPane.setDividerLocation(300);
        splitPane.setResizeWeight(0.3);
        splitPane.setLeftComponent(progressPanel);
        splitPane.setRightComponent(tasksPanel);
        
        topPanel.add(splitPane, BorderLayout.CENTER);
        
        return topPanel;
    }
    
    /**
     * Creates the progress panel showing points and level.
     */
    private JPanel createProgressPanel() {
        JPanel progressPanel = new JPanel();
        progressPanel.setLayout(new BoxLayout(progressPanel, BoxLayout.Y_AXIS));
        progressPanel.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createEtchedBorder(), "My Progress"));
        progressPanel.setBackground(Color.WHITE);
        progressPanel.setPreferredSize(new Dimension(280, 380));
        
        // Child selector
        JPanel selectorPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        selectorPanel.setBackground(Color.WHITE);
        JLabel selectorLabel = new JLabel("I am:");
        childSelector = new JComboBox<>();
        loadChildrenIntoSelector();
        childSelector.addActionListener(e -> {
            String selected = (String) childSelector.getSelectedItem();
            if (selected != null && !selected.equals("No children available")) {
                setChildUsername(selected);
            }
        });
        selectorPanel.add(selectorLabel);
        selectorPanel.add(childSelector);
        
        // Points display
        pointsLabel = new JLabel("Points: 0", JLabel.CENTER);
        pointsLabel.setFont(new Font("Arial", Font.BOLD, 20));
        pointsLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        // Level display
        levelLabel = new JLabel("Level: 1", JLabel.CENTER);
        levelLabel.setFont(new Font("Arial", Font.BOLD, 18));
        levelLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        // Progress bar
        pointsProgressBar = new JProgressBar(0, 100);
        pointsProgressBar.setStringPainted(true);
        pointsProgressBar.setString("0 / 100 points to next level");
        pointsProgressBar.setPreferredSize(new Dimension(250, 30));
        pointsProgressBar.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        progressPanel.add(Box.createVerticalStrut(20));
        progressPanel.add(selectorPanel);
        progressPanel.add(Box.createVerticalStrut(20));
        progressPanel.add(pointsLabel);
        progressPanel.add(Box.createVerticalStrut(10));
        progressPanel.add(levelLabel);
        progressPanel.add(Box.createVerticalStrut(20));
        progressPanel.add(pointsProgressBar);
        progressPanel.add(Box.createVerticalGlue());
        
        return progressPanel;
    }
    
    /**
     * Creates the tasks panel.
     */
    private JPanel createTasksPanel() {
        JPanel tasksPanel = new JPanel(new BorderLayout());
        tasksPanel.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createEtchedBorder(), "My Tasks"));
        tasksPanel.setBackground(Color.WHITE);
        
        String[] columnNames = {"ID", "Title", "Points", "Status", "Complete"};
        tasksTableModel = new DefaultTableModel(columnNames, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return column == 4; // Only Complete button column
            }
        };
        
        tasksTable = new JTable(tasksTableModel);
        tasksTable.setRowHeight(30);
        tasksTable.getColumnModel().getColumn(0).setPreferredWidth(50);
        tasksTable.getColumnModel().getColumn(1).setPreferredWidth(200);
        tasksTable.getColumnModel().getColumn(2).setPreferredWidth(80);
        tasksTable.getColumnModel().getColumn(3).setPreferredWidth(100);
        tasksTable.getColumnModel().getColumn(4).setPreferredWidth(100);
        
        // Add button renderer and editor
        tasksTable.getColumn("Complete").setCellRenderer(new ButtonRenderer(new Color(135, 206, 250)));
        tasksTable.getColumn("Complete").setCellEditor(new TaskButtonEditor(new JCheckBox()));
        
        JScrollPane scrollPane = new JScrollPane(tasksTable);
        tasksPanel.add(scrollPane, BorderLayout.CENTER);
        
        return tasksPanel;
    }
    
    /**
     * Creates the wishes panel.
     */
    private JPanel createWishesPanel() {
        JPanel wishesPanel = new JPanel(new BorderLayout());
        wishesPanel.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createEtchedBorder(), "My Wishes"));
        wishesPanel.setBackground(Color.WHITE);
        
        // Add Wish form
        JPanel wishFormPanel = new JPanel();
        wishFormPanel.setLayout(new FlowLayout(FlowLayout.LEFT));
        wishFormPanel.setBackground(Color.WHITE);
        wishFormPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        JLabel wishNameLabel = new JLabel("Wish Name:");
        wishNameField = new JTextField(15);
        JLabel wishLevelLabel = new JLabel("Required Level:");
        wishLevelField = new JTextField(5);
        JButton addWishButton = new JButton("Add Wish");
        addWishButton.setBackground(new Color(135, 206, 250));
        addWishButton.setForeground(Color.WHITE);
        addWishButton.addActionListener(new AddWishActionListener());
        
        wishFormPanel.add(wishNameLabel);
        wishFormPanel.add(wishNameField);
        wishFormPanel.add(wishLevelLabel);
        wishFormPanel.add(wishLevelField);
        wishFormPanel.add(addWishButton);
        
        // Wishes table
        JPanel wishesTablePanel = createWishesTable();
        
        wishesPanel.add(wishFormPanel, BorderLayout.NORTH);
        wishesPanel.add(wishesTablePanel, BorderLayout.CENTER);
        
        return wishesPanel;
    }
    
    /**
     * Creates the wishes table.
     */
    private JPanel createWishesTable() {
        JPanel tablePanel = new JPanel(new BorderLayout());
        tablePanel.setBackground(Color.WHITE);
        
        String[] columnNames = {"ID", "Wish Name", "Required Level", "Status"};
        wishesTableModel = new DefaultTableModel(columnNames, 0);
        
        JTable wishesTable = new JTable(wishesTableModel);
        wishesTable.setRowHeight(25);
        
        JScrollPane scrollPane = new JScrollPane(wishesTable);
        tablePanel.add(scrollPane, BorderLayout.CENTER);
        
        return tablePanel;
    }
    
    /**
     * Loads children into the selector.
     */
    private void loadChildrenIntoSelector() {
        if (childSelector == null) return;
        
        try {
            childSelector.removeAllItems();
            if (dataManager != null) {
                List<Child> children = dataManager.getAllChildren();
                for (Child child : children) {
                    if (child != null && child.getUsername() != null) {
                        childSelector.addItem(child.getUsername());
                    }
                }
                if (children.isEmpty()) {
                    childSelector.addItem("No children available");
                } else {
                    childSelector.setSelectedIndex(0);
                    if (children.size() > 0) {
                        setChildUsername(children.get(0).getUsername());
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("Error loading children: " + e.getMessage());
        }
    }
    
    /**
     * Updates the progress display.
     */
    private void updateProgressDisplay() {
        try {
            if (dataManager != null && currentChildUsername != null) {
                Child child = (Child) dataManager.findUser(currentChildUsername);
                if (child != null) {
                    int points = child.getTotalPoints();
                    int level = child.getCurrentLevel();
                    
                    pointsLabel.setText("Points: " + points);
                    levelLabel.setText("Level: " + level);
                    
                    // Calculate progress to next level (points % 100)
                    int progress = points % 100;
                    pointsProgressBar.setValue(progress);
                    pointsProgressBar.setString(progress + " / 100 points to next level");
                }
            }
        } catch (Exception e) {
            System.err.println("Error updating progress: " + e.getMessage());
        }
    }
    
    /**
     * Refreshes the tasks table.
     */
    private void refreshTasksTable() {
        if (tasksTableModel == null) return;
        
        try {
            tasksTableModel.setRowCount(0);
            
            if (dataManager != null && currentChildUsername != null) {
                dataManager.loadTasks();
                List<Task> tasks = dataManager.getTasksForChild(currentChildUsername);
                
                for (Task task : tasks) {
                    if (task != null && !task.getStatus().equals("Approved")) {
                        String buttonText = task.getStatus().equals("Completed") ? "Completed" : "Mark Complete";
                        Object[] rowData = {
                            task.getId(),
                            task.getTitle() != null ? task.getTitle() : "",
                            task.getPoints(),
                            task.getStatus(),
                            buttonText
                        };
                        tasksTableModel.addRow(rowData);
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("Error refreshing tasks table: " + e.getMessage());
        }
    }
    
    /**
     * Refreshes the wishes table.
     */
    private void refreshWishesTable() {
        if (wishesTableModel == null) return;
        
        try {
            wishesTableModel.setRowCount(0);
            
            if (dataManager != null && currentChildUsername != null) {
                dataManager.loadWishes();
                List<Wish> wishes = dataManager.getWishesForChild(currentChildUsername);
                
                for (Wish wish : wishes) {
                    if (wish != null) {
                        Object[] rowData = {
                            wish.getId(),
                            wish.getItemName() != null ? wish.getItemName() : "",
                            wish.getRequiredLevel(),
                            wish.getStatus()
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
     * Marks a task as completed.
     */
    private void markTaskComplete(int taskId) {
        try {
            Task task = dataManager.findTask(taskId);
            if (task != null && task.getStatus().equals("Pending")) {
                task.setStatus("Completed");
                dataManager.updateTask(task);
                refreshTasksTable();
                JOptionPane.showMessageDialog(this,
                    "Task marked as completed! Waiting for approval.", 
                    "Success", JOptionPane.INFORMATION_MESSAGE);
            }
        } catch (Exception e) {
            System.err.println("Error marking task complete: " + e.getMessage());
            JOptionPane.showMessageDialog(this,
                "Error: " + e.getMessage(), 
                "Error", JOptionPane.ERROR_MESSAGE);
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
     * Button editor for task completion.
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
            button.addActionListener(e -> fireEditingStopped());
        }
        
        @Override
        public Component getTableCellEditorComponent(JTable table, Object value,
                boolean isSelected, int row, int column) {
            label = (value == null) ? "" : value.toString();
            button.setText(label);
            button.setBackground(new Color(135, 206, 250));
            button.setForeground(Color.WHITE);
            isPushed = true;
            selectedRow = row;
            return button;
        }
        
        @Override
        public Object getCellEditorValue() {
            if (isPushed) {
                int taskId = (Integer) tasksTableModel.getValueAt(selectedRow, 0);
                String status = (String) tasksTableModel.getValueAt(selectedRow, 3);
                if (status.equals("Pending")) {
                    markTaskComplete(taskId);
                }
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
     * Action listener for Add Wish button.
     */
    private class AddWishActionListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            String wishName = wishNameField.getText().trim();
            String levelText = wishLevelField.getText().trim();
            
            if (wishName.isEmpty()) {
                JOptionPane.showMessageDialog(ChildDashboardPanel.this,
                    "Please enter a wish name.", "Validation Error", JOptionPane.WARNING_MESSAGE);
                return;
            }
            
            if (levelText.isEmpty()) {
                JOptionPane.showMessageDialog(ChildDashboardPanel.this,
                    "Please enter required level.", "Validation Error", JOptionPane.WARNING_MESSAGE);
                return;
            }
            
            int requiredLevel;
            try {
                requiredLevel = Integer.parseInt(levelText);
                if (requiredLevel <= 0) {
                    throw new NumberFormatException();
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(ChildDashboardPanel.this,
                    "Please enter a valid positive number for level.", 
                    "Validation Error", JOptionPane.WARNING_MESSAGE);
                return;
            }
            
            if (currentChildUsername == null) {
                JOptionPane.showMessageDialog(ChildDashboardPanel.this,
                    "Please select a child first.", "Validation Error", JOptionPane.WARNING_MESSAGE);
                return;
            }
            
            try {
                Wish newWish = new Wish(0, wishName, requiredLevel, currentChildUsername);
                dataManager.addWish(newWish);
                
                wishNameField.setText("");
                wishLevelField.setText("");
                
                refreshWishesTable();
                
                JOptionPane.showMessageDialog(ChildDashboardPanel.this,
                    "Wish added successfully!", "Success", JOptionPane.INFORMATION_MESSAGE);
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(ChildDashboardPanel.this,
                    "Error adding wish: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }
}
