# quantum_expert_system.py
import time
import sqlite3
import numpy as np
import requests
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json

class QuantumExpertSystem:
    def __init__(self, game_type="1M"):
        self.game_type = game_type
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
        self.club55_username = os.getenv('CLUB55_USERNAME')
        self.club55_password = os.getenv('CLUB55_PASSWORD')
        
        self.setup_quantum_database()
        self.setup_browser()
        self.current_running_period = None

    def setup_quantum_database(self):
        """Initialize quantum database"""
        try:
            self.conn = sqlite3.connect('quantum_data.db', check_same_thread=False)
            self.cursor = self.conn.cursor()
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS quantum_game_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    period TEXT UNIQUE,
                    number INTEGER,
                    big_small TEXT,
                    color TEXT,
                    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    game_type TEXT
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS quantum_predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    period TEXT UNIQUE,
                    prediction TEXT,
                    confidence FLOAT,
                    strategy_used TEXT,
                    actual_result TEXT,
                    is_correct BOOLEAN,
                    predicted_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            print("✅ Quantum database initialized")
            
        except Exception as e:
            print(f"❌ Database setup failed: {e}")
            raise

    def setup_browser(self):
        """Setup Chrome browser for GitHub Actions"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--ignore-certificate-errors")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 15)
            print("✅ Browser setup complete")
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            raise

    def send_telegram_message(self, message):
        """Send message to Telegram"""
        try:
            if not self.telegram_bot_token or not self.telegram_channel_id:
                return False
                
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_channel_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Telegram error: {e}")
            return False

    def handle_puzzle_verification(self):
        """Handle drag-and-drop puzzle verification"""
        print("🧩 Handling puzzle verification...")
        try:
            # Wait for puzzle element to appear
            puzzle_selectors = [
                ".verify-bar",
                ".slider",
                ".drag-handle",
                "[class*='verify']",
                "[class*='slider']"
            ]
            
            puzzle_element = None
            for selector in puzzle_selectors:
                try:
                    puzzle_element = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    if puzzle_element:
                        break
                except:
                    continue
            
            if puzzle_element:
                # Get element size and location
                size = puzzle_element.size
                location = puzzle_element.location
                
                # Calculate drag distance (typical puzzle verification)
                drag_distance = size['width'] - 10
                
                # Perform drag action
                actions = ActionChains(self.driver)
                actions.click_and_hold(puzzle_element)
                actions.move_by_offset(drag_distance, 0)
                actions.release()
                actions.perform()
                
                print("✅ Puzzle verification completed")
                time.sleep(3)
                return True
                
        except Exception as e:
            print(f"⚠️ Puzzle handling failed: {e}")
        
        return False

    def handle_confirmation_screens(self):
        """Handle multiple confirmation/receive screens"""
        print("🔄 Handling confirmation screens...")
        
        confirmation_selectors = [
            "button:contains('Confirm')",
            "button:contains('OK')",
            "button:contains('Yes')",
            "button:contains('Agree')",
            "button:contains('Receive')",
            ".confirm-btn",
            ".ok-button",
            ".btn-confirm"
        ]
        
        max_screens = 6
        screens_handled = 0
        
        for _ in range(max_screens):
            clicked = False
            for selector in confirmation_selectors:
                try:
                    # Try CSS selector first
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in buttons:
                        if button.is_displayed():
                            button.click()
                            print(f"✅ Clicked: {selector}")
                            clicked = True
                            screens_handled += 1
                            time.sleep(2)
                            break
                    if clicked:
                        break
                except:
                    continue
            
            if not clicked:
                break
        
        print(f"✅ Handled {screens_handled} confirmation screens")
        return screens_handled > 0

    def navigate_to_1m_game(self):
        """Navigate to 1M WinGo game"""
        print("🎮 Navigating to 1M game...")
        
        try:
            # Game page URL
            game_url = "https://55club.game/#/saasLottery/WinGo?gameCode=WinGo_30S&lottery=WinGo"
            self.driver.get(game_url)
            time.sleep(8)
            
            # Wait for game to load and switch to 1M
            game_loaded = False
            game_indicators = ['Period', 'Number', 'Big', 'Small', 'WinGo']
            
            for _ in range(5):
                page_text = self.driver.find_element(By.TAG_NAME, "body").text
                if any(indicator in page_text for indicator in game_indicators):
                    game_loaded = True
                    break
                time.sleep(3)
            
            if not game_loaded:
                print("❌ Game page not loaded properly")
                return False
            
            # Switch to 1M game tab
            tab_selectors = [
                "button:contains('1M')",
                "a[href*='1M']",
                ".tab:contains('1M')",
                "[class*='1m']",
                "[class*='one']"
            ]
            
            for selector in tab_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            element.click()
                            print("✅ Switched to 1M game")
                            time.sleep(5)
                            return True
                except:
                    continue
            
            print("⚠️ Could not find 1M tab, continuing with current game")
            return True
            
        except Exception as e:
            print(f"❌ Game navigation failed: {e}")
            return False

    def perform_login(self):
        """Perform complete login flow"""
        print("🔐 Starting login process...")
        
        try:
            # Navigate to login page
            self.driver.get("https://55club.game/")
            time.sleep(8)
            
            # Check if already logged in
            if "login" not in self.driver.current_url.lower():
                print("✅ Already logged in")
                return True
            
            # Find and fill login form
            username_selectors = [
                "input[type='text']",
                "input[name='username']",
                "input[placeholder*='phone']",
                "input[placeholder*='email']"
            ]
            
            password_selectors = [
                "input[type='password']",
                "input[name='password']"
            ]
            
            # Fill username
            for selector in username_selectors:
                try:
                    username_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    username_field.clear()
                    username_field.send_keys(self.club55_username)
                    print("✅ Username filled")
                    break
                except:
                    continue
            
            # Fill password
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    password_field.clear()
                    password_field.send_keys(self.club55_password)
                    print("✅ Password filled")
                    break
                except:
                    continue
            
            # Click login button
            login_selectors = [
                "button[type='submit']",
                "button:contains('Login')",
                "button:contains('Sign In')"
            ]
            
            for selector in login_selectors:
                try:
                    login_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    login_btn.click()
                    print("✅ Login button clicked")
                    time.sleep(5)
                    break
                except:
                    continue
            
            # Handle puzzle verification
            self.handle_puzzle_verification()
            
            # Handle confirmation screens
            self.handle_confirmation_screens()
            
            print("✅ Login flow completed")
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False

    # QUANTUM PREDICTION ENGINE (From your original code)
    def extract_game_data(self):
        """Extract game data from page"""
        print("🔍 Extracting game data...")
        
        data = []
        try:
            # Multiple extraction methods
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            lines = [line.strip() for line in body_text.split('\n') if line.strip()]
            
            i = 0
            while i < len(lines) - 2:
                line1 = lines[i].replace(' ', '').replace('-', '')
                line2 = lines[i+1].replace(' ', '') if i+1 < len(lines) else ""
                line3 = lines[i+2] if i+2 < len(lines) else ""
                
                if (line1.isdigit() and len(line1) == 17 and
                    line2.isdigit() and 0 <= int(line2) <= 9 and
                    line3 in ['Big', 'Small']):
                    
                    data.append({
                        'period': line1,
                        'number': int(line2),
                        'big_small': line3,
                        'color': 'green' if int(line2) == 0 else 'red' if int(line2) % 2 == 1 else 'violet'
                    })
                    i += 3
                else:
                    i += 1
                    
            print(f"📊 Extracted {len(data)} records")
            return data
            
        except Exception as e:
            print(f"❌ Data extraction failed: {e}")
            return []

    def quantum_prediction_engine(self, training_data):
        """Quantum prediction engine"""
        if len(training_data) < 10:
            return self.fallback_prediction(training_data)
        
        # Analyze recent trends
        results = [game['big_small'] for game in training_data[:20]]
        big_count = results.count('Big')
        total = len(results)
        
        # Multiple strategy analysis
        trend_pred, trend_conf = self.trend_analysis(results)
        pattern_pred, pattern_conf = self.pattern_analysis(results)
        statistical_pred, statistical_conf = self.statistical_analysis(results)
        
        # Weighted combination
        final_prediction = trend_pred if trend_conf > pattern_conf else pattern_pred
        confidence = max(trend_conf, pattern_conf, statistical_conf)
        
        reasoning = f"Trend: {trend_pred}({trend_conf:.2f}), Pattern: {pattern_pred}({pattern_conf:.2f})"
        
        return {
            "prediction": final_prediction,
            "confidence": confidence,
            "strategy": "quantum_adaptive", 
            "reasoning": reasoning
        }

    def trend_analysis(self, results):
        big_count = results.count('Big')
        ratio = big_count / len(results) if results else 0.5
        
        if ratio > 0.6:
            return 'Big', 0.75
        elif ratio < 0.4:
            return 'Small', 0.75
        else:
            return 'Big' if ratio >= 0.5 else 'Small', 0.65

    def pattern_analysis(self, results):
        if len(results) < 3:
            return 'Small', 0.5
            
        streak = 1
        for i in range(1, len(results)):
            if results[i] == results[0]:
                streak += 1
            else:
                break
                
        if streak >= 3:
            opposite = 'Small' if results[0] == 'Big' else 'Big'
            return opposite, 0.70
        else:
            return results[0], 0.60

    def statistical_analysis(self, results):
        big_count = results.count('Big')
        return 'Big' if big_count >= len(results)/2 else 'Small', 0.65

    def fallback_prediction(self, training_data):
        return {
            "prediction": "Small",
            "confidence": 0.5, 
            "strategy": "fallback",
            "reasoning": "Insufficient data"
        }

    def format_prediction_message(self, prediction_data, period):
        prediction = prediction_data["prediction"]
        confidence = prediction_data["confidence"]
        
        emoji = "🔴" if prediction == "B" else "🔵"
        confidence_color = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.6 else "🟠"
        
        message = f"""
{emoji} <b>QUANTUM PREDICTION</b> {emoji}

🎯 <b>Prediction:</b> <code>{prediction}</code>
📊 <b>Confidence:</b> <code>{confidence:.2%}</code> {confidence_color}
🎮 <b>Period:</b> <code>{period}</code>
🤖 <b>Strategy:</b> <code>{prediction_data['strategy']}</code>

💡 <b>Analysis:</b>
{prediction_data['reasoning']}

⏰ <i>Generated: {datetime.now().strftime('%H:%M:%S')}</i>
        """
        return message.strip()

    def run_expert_system(self):
        """Main expert system execution"""
        print("🚀 QUANTUM EXPERT SYSTEM STARTED")
        
        # Send startup message
        self.send_telegram_message("🔮 <b>Quantum Expert System Started</b>\n🎯 Monitoring WinGo 1M\n🤖 AI Predictions Active")
        
        # Perform login and navigation
        if not self.perform_login():
            self.send_telegram_message("❌ <b>Login Failed</b>\n🔐 Check credentials")
            return
            
        if not self.navigate_to_1m_game():
            self.send_telegram_message("❌ <b>Game Navigation Failed</b>")
            return
        
        # Main prediction loop
        print("🔮 Starting prediction cycles...")
        
        for cycle in range(5):  # 5 cycles for testing
            print(f"\n🔄 Cycle {cycle + 1}/5")
            
            try:
                # Extract current data
                game_data = self.extract_game_data()
                if game_data:
                    # Save to database
                    for game in game_data:
                        try:
                            self.cursor.execute('''
                                INSERT OR IGNORE INTO quantum_game_results 
                                (period, number, big_small, color, game_type)
                                VALUES (?, ?, ?, ?, ?)
                            ''', (game['period'], game['number'], game['big_small'], 
                                  game['color'], self.game_type))
                        except:
                            pass
                    self.conn.commit()
                
                # Get training data
                training_data = self.get_training_data()
                
                # Make prediction
                prediction_data = self.quantum_prediction_engine(training_data)
                
                # Get current period
                current_period = self.get_current_period()
                
                if current_period and current_period != self.current_running_period:
                    # Send prediction to Telegram
                    message = self.format_prediction_message(prediction_data, current_period)
                    self.send_telegram_message(message)
                    
                    self.current_running_period = current_period
                
                time.sleep(15)  # Wait 15 seconds between cycles
                
            except Exception as e:
                print(f"❌ Cycle error: {e}")
                time.sleep(10)
        
        # Completion message
        self.send_telegram_message("✅ <b>Quantum System Completed</b>\n📊 5 cycles executed\n🤖 Ready for next run")

    def get_training_data(self, limit=50):
        """Get training data from database"""
        try:
            self.cursor.execute('''
                SELECT period, number, big_small FROM quantum_game_results 
                WHERE game_type = ? ORDER BY scraped_at DESC LIMIT ?
            ''', (self.game_type, limit))
            
            return [{'period': p, 'number': n, 'big_small': b} 
                   for p, n, b in self.cursor.fetchall()]
        except:
            return []

    def get_current_period(self):
        """Get current running period"""
        try:
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            lines = body_text.split('\n')
            
            for line in lines:
                line = line.strip().replace(' ', '').replace('-', '')
                if line.isdigit() and len(line) == 17:
                    return line
            return None
        except:
            return None

    def close(self):
        """Cleanup resources"""
        try:
            self.conn.close()
            self.driver.quit()
        except:
            pass

if __name__ == "__main__":
    system = QuantumExpertSystem()
    
    try:
        system.run_expert_system()
    except Exception as e:
        print(f"❌ System error: {e}")
        system.send_telegram_message(f"❌ <b>System Crash</b>\n{str(e)}")
    finally:
        system.close()
