# ===============================
# Wheel Profit Menu Bar Widget
# ===============================
# Python 3.x, macOS
# Requires: rumps + AppleScript
# Run with: python wheel_profit_widget.py
# ===============================

import rumps
import subprocess


class WheelProfitCalculator(rumps.App):
    """macOS Menu Bar Widget for Wheel Trading Profit Calculations"""
    
    def __init__(self):
        super(WheelProfitCalculator, self).__init__("Wheel Profit")
        self.menu = ["Calculate", "Quit"]

    def get_user_input(self, prompt, default_value, title):
        """Get user input using AppleScript dialog"""
        script = f'''
        tell application "System Events"
            set userInput to text returned of (display dialog "{prompt}" default answer "{default_value}" with title "{title}")
        end tell
        return userInput
        '''
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True)
        return result.stdout.strip()

    def show_result(self, credit_val, fee_val, profit_percent_val, target_profit, debit_to_close):
        """Display calculation results using AppleScript"""
        result_text = f"""Results:

Credit: ${credit_val:.2f}
Fee: ${fee_val:.2f}
Profit Target: {profit_percent_val*100:.0f}%

Target Profit: ${target_profit:.2f}
Debit to Close: ${debit_to_close:.2f}"""
        
        script = f'''
        tell application "System Events"
            display dialog "{result_text}" with title "Wheel Profit Calculator Results"
        end tell
        '''
        subprocess.run(['osascript', '-e', script])

    def show_error(self, error_message):
        """Display error message using AppleScript"""
        script = f'''
        tell application "System Events"
            display dialog "Error: {error_message}\\n\\nPlease enter valid numbers for all fields." with title "Wheel Profit Calculator Error"
        end tell
        '''
        subprocess.run(['osascript', '-e', script])

    @rumps.clicked("Calculate")
    def calculate(self, _):
        """Main calculation method"""
        try:
            # Get user inputs
            credit = self.get_user_input("Enter Credit Amount:", "200", "Wheel Profit Calculator")
            if not credit:
                return
                
            fee = self.get_user_input("Enter Fee Amount:", "2", "Wheel Profit Calculator")
            if not fee:
                return
                
            profit_percent = self.get_user_input("Enter Profit Percentage:", "50", "Wheel Profit Calculator")
            if not profit_percent:
                return

            # Parse inputs
            credit_val = float(credit)
            fee_val = float(fee)
            profit_percent_val = float(profit_percent) / 100

            # Perform calculations
            total_base = credit_val + fee_val
            target_profit = total_base * profit_percent_val
            debit_to_close = total_base - target_profit

            # Show results
            self.show_result(credit_val, fee_val, profit_percent_val, target_profit, debit_to_close)

        except ValueError as e:
            self.show_error("Invalid number format")
        except Exception as e:
            self.show_error(str(e))


if __name__ == "__main__":
    WheelProfitCalculator().run()
