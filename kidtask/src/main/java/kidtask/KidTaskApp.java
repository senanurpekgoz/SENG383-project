package kidtask;

import kidtask.gui.MainFrame;
import javax.swing.SwingUtilities;
import javax.swing.UIManager;
import javax.swing.JOptionPane;

/**
 * Main application entry point for KidTask.
 * Initializes and displays the main application window.
 */
public class KidTaskApp {
    
    public static void main(String[] args) {
        // Use SwingUtilities.invokeLater to ensure thread safety
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                try {
                    // Set system look and feel for better appearance
                    UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
                } catch (Exception e) {
                    // If setting look and feel fails, use default
                    System.err.println("Could not set system look and feel: " + e.getMessage());
                    e.printStackTrace();
                }
                
                try {
                    // Create and show the main frame
                    MainFrame mainFrame = new MainFrame();
                    mainFrame.pack(); // Ensure proper sizing before showing
                    mainFrame.setVisible(true);
                    System.out.println("KidTask application started successfully!");
                } catch (Exception e) {
                    System.err.println("Error starting application: " + e.getMessage());
                    e.printStackTrace();
                    JOptionPane.showMessageDialog(null, 
                        "Error starting application: " + e.getMessage(), 
                        "Startup Error", 
                        JOptionPane.ERROR_MESSAGE);
                }
            }
        });
    }
}
