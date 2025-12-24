package kidtask.gui;

import javax.swing.*;
import java.awt.*;

/**
 * Main application window that manages different screens using CardLayout.
 * Handles navigation between Login, Child Dashboard, Parent Dashboard, and Teacher Dashboard.
 */
public class MainFrame extends JFrame {
    private static final String LOGIN_PANEL = "LOGIN";
    private static final String CHILD_DASHBOARD = "CHILD_DASHBOARD";
    private static final String PARENT_DASHBOARD = "PARENT_DASHBOARD";
    private static final String TEACHER_DASHBOARD = "TEACHER_DASHBOARD";
    
    private CardLayout cardLayout;
    private JPanel cardPanel;
    private LoginPanel loginPanel;
    private ChildDashboardPanel childDashboardPanel;
    private ParentDashboardPanel parentDashboardPanel;
    private TeacherDashboardPanel teacherDashboardPanel;
    
    public MainFrame() {
        try {
            initializeFrame();
            setupCardLayout();
            showLoginPanel();
        } catch (Exception e) {
            System.err.println("Error initializing MainFrame: " + e.getMessage());
            e.printStackTrace();
            JOptionPane.showMessageDialog(null, 
                "Error initializing application: " + e.getMessage(), 
                "Initialization Error", 
                JOptionPane.ERROR_MESSAGE);
        }
    }
    
    /**
     * Initializes the main frame properties.
     */
    private void initializeFrame() {
        setTitle("KidTask - Task and Wish Management");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(900, 700);
        setLocationRelativeTo(null); // Center the window
        setResizable(true);
    }
    
    /**
     * Sets up the CardLayout and all panels.
     */
    private void setupCardLayout() {
        cardLayout = new CardLayout();
        cardPanel = new JPanel(cardLayout);
        
        // Create all panels
        loginPanel = new LoginPanel(this);
        childDashboardPanel = new ChildDashboardPanel(this);
        parentDashboardPanel = new ParentDashboardPanel(this);
        teacherDashboardPanel = new TeacherDashboardPanel(this);
        
        // Add panels to card layout
        cardPanel.add(loginPanel, LOGIN_PANEL);
        cardPanel.add(childDashboardPanel, CHILD_DASHBOARD);
        cardPanel.add(parentDashboardPanel, PARENT_DASHBOARD);
        cardPanel.add(teacherDashboardPanel, TEACHER_DASHBOARD);
        
        add(cardPanel);
    }
    
    /**
     * Shows the login panel.
     */
    public void showLoginPanel() {
        cardLayout.show(cardPanel, LOGIN_PANEL);
    }
    
    /**
     * Shows the child dashboard panel.
     */
    public void showChildDashboard() {
        try {
            if (childDashboardPanel != null) {
                childDashboardPanel.refreshData();
                cardLayout.show(cardPanel, CHILD_DASHBOARD);
            }
        } catch (Exception e) {
            System.err.println("Error showing child dashboard: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * Shows the parent dashboard panel.
     */
    public void showParentDashboard() {
        try {
            if (parentDashboardPanel != null) {
                parentDashboardPanel.refreshData();
                cardLayout.show(cardPanel, PARENT_DASHBOARD);
            } else {
                System.err.println("ParentDashboardPanel is null!");
                JOptionPane.showMessageDialog(this, 
                    "Error: Parent dashboard not initialized.", 
                    "Navigation Error", 
                    JOptionPane.ERROR_MESSAGE);
            }
        } catch (Exception e) {
            System.err.println("Error showing parent dashboard: " + e.getMessage());
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, 
                "Error loading parent dashboard: " + e.getMessage(), 
                "Navigation Error", 
                JOptionPane.ERROR_MESSAGE);
        }
    }
    
    /**
     * Shows the teacher dashboard panel.
     */
    public void showTeacherDashboard() {
        try {
            if (teacherDashboardPanel != null) {
                teacherDashboardPanel.refreshData();
                cardLayout.show(cardPanel, TEACHER_DASHBOARD);
            } else {
                System.err.println("TeacherDashboardPanel is null!");
            }
        } catch (Exception e) {
            System.err.println("Error showing teacher dashboard: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * Gets the child dashboard panel (for updates).
     */
    public ChildDashboardPanel getChildDashboardPanel() {
        return childDashboardPanel;
    }
    
    /**
     * Gets the parent dashboard panel (for updates).
     */
    public ParentDashboardPanel getParentDashboardPanel() {
        return parentDashboardPanel;
    }
    
    /**
     * Gets the teacher dashboard panel (for updates).
     */
    public TeacherDashboardPanel getTeacherDashboardPanel() {
        return teacherDashboardPanel;
    }
}

