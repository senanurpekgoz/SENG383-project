package kidtask.gui;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/**
 * Login panel that allows users to select their role (Child, Parent, or Teacher)
 * and navigate to the appropriate dashboard.
 */
public class LoginPanel extends JPanel {
    private MainFrame mainFrame;
    
    public LoginPanel(MainFrame mainFrame) {
        this.mainFrame = mainFrame;
        initializePanel();
    }
    
    /**
     * Initializes the login panel with role selection buttons.
     */
    private void initializePanel() {
        setLayout(new BorderLayout());
        setBackground(new Color(240, 248, 255)); // Light blue background
        
        // Create title panel
        JPanel titlePanel = createTitlePanel();
        
        // Create button panel
        JPanel buttonPanel = createButtonPanel();
        
        // Add components
        add(titlePanel, BorderLayout.NORTH);
        add(buttonPanel, BorderLayout.CENTER);
    }
    
    /**
     * Creates the title panel with application name.
     */
    private JPanel createTitlePanel() {
        JPanel titlePanel = new JPanel();
        titlePanel.setBackground(new Color(240, 248, 255));
        titlePanel.setBorder(BorderFactory.createEmptyBorder(50, 20, 30, 20));
        
        JLabel titleLabel = new JLabel("KidTask", JLabel.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 48));
        titleLabel.setForeground(new Color(70, 130, 180));
        
        JLabel subtitleLabel = new JLabel("Task and Wish Management System", JLabel.CENTER);
        subtitleLabel.setFont(new Font("Arial", Font.PLAIN, 18));
        subtitleLabel.setForeground(new Color(100, 100, 100));
        
        titlePanel.setLayout(new BoxLayout(titlePanel, BoxLayout.Y_AXIS));
        titlePanel.add(titleLabel);
        titlePanel.add(Box.createVerticalStrut(10));
        titlePanel.add(subtitleLabel);
        
        return titlePanel;
    }
    
    /**
     * Creates the button panel with role selection buttons.
     */
    private JPanel createButtonPanel() {
        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(new GridBagLayout());
        buttonPanel.setBackground(new Color(240, 248, 255));
        buttonPanel.setBorder(BorderFactory.createEmptyBorder(20, 50, 50, 50));
        
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(15, 15, 15, 15);
        gbc.fill = GridBagConstraints.BOTH; // Fill both horizontally and vertically
        gbc.weightx = 1.0;
        gbc.weighty = 1.0;
        gbc.gridwidth = GridBagConstraints.REMAINDER; // Each button takes full width
        
        // Child button
        JButton childButton = createRoleButton("Child", new Color(135, 206, 250), 
                                               "Complete tasks and earn points!");
        gbc.gridx = 0;
        gbc.gridy = 0;
        buttonPanel.add(childButton, gbc);
        childButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                mainFrame.showChildDashboard();
            }
        });
        
        // Parent button
        JButton parentButton = createRoleButton("Parent", new Color(144, 238, 144),
                                                "Manage tasks and approve wishes!");
        gbc.gridx = 0;
        gbc.gridy = 1;
        buttonPanel.add(parentButton, gbc);
        parentButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                mainFrame.showParentDashboard();
            }
        });
        
        // Teacher button
        JButton teacherButton = createRoleButton("Teacher", new Color(255, 182, 193),
                                                 "Create tasks and manage rewards!");
        gbc.gridx = 0;
        gbc.gridy = 2;
        buttonPanel.add(teacherButton, gbc);
        teacherButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                mainFrame.showTeacherDashboard();
            }
        });
        
        return buttonPanel;
    }
    
    /**
     * Creates a styled role selection button.
     */
    private JButton createRoleButton(String role, Color color, String tooltip) {
        JButton button = new JButton(role);
        button.setFont(new Font("Arial", Font.BOLD, 24));
        button.setPreferredSize(new Dimension(300, 80));
        button.setMinimumSize(new Dimension(300, 80));
        button.setMaximumSize(new Dimension(300, 80));
        
        // Ensure button is fully colored
        button.setBackground(color);
        button.setForeground(Color.WHITE);
        button.setOpaque(true);
        button.setContentAreaFilled(true);
        button.setBorderPainted(true);
        button.setFocusPainted(false);
        button.setBorder(BorderFactory.createRaisedBevelBorder());
        button.setToolTipText(tooltip);
        
        // Add hover effect
        button.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseEntered(java.awt.event.MouseEvent evt) {
                button.setBackground(color.darker());
            }
            public void mouseExited(java.awt.event.MouseEvent evt) {
                button.setBackground(color);
            }
        });
        
        return button;
    }
}

