import requests
import pandas as pd
import numpy as np
import sqlite3
import time
import os
from datetime import datetime
import logging
import sys

# Configure logging and immediate print output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
print("🚀 START: Quantum Expert System Starting...")
sys.stdout.flush()

class QuantumExpertSystem:
    def __init__(self):
        print("🔍 DEBUG: Initializing QuantumExpertSystem...")
        sys.stdout.flush()
        
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
        
        print(f"🔍 DEBUG: Token exists: {bool(self.telegram_bot_token)}")
        print(f"🔍 DEBUG: Channel ID exists: {bool(self.telegram_channel_id)}")
        sys.stdout.flush()
        
        self.db_path = "quantum_predictions.db"
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for storing predictions and results"""
        print("🔍 DEBUG: Initializing database...")
        sys.stdout.flush()
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    period INTEGER,
                    prediction TEXT,
                    actual_result TEXT,
                    strategy_used TEXT,
                    confidence REAL
                )
            ''')
            conn.commit()
            conn.close()
            print("✅ DEBUG: Database initialized successfully")
            sys.stdout.flush()
        except Exception as e:
            print(f"❌ DEBUG: Database init error: {e}")
            sys.stdout.flush()

    def get_historical_data(self):
        """Fetch historical WinGo data"""
        print("🔍 DEBUG: Getting historical data...")
        sys.stdout.flush()
        try:
            # For now, use simulated data
            print("🔍 DEBUG: Using simulated data...")
            sys.stdout.flush()
            return self.generate_simulated_data()
        except Exception as e:
            print(f"❌ DEBUG: Historical data error: {e}")
            sys.stdout.flush()
            return self.generate_simulated_data()

    def generate_simulated_data(self):
        """Generate realistic simulated WinGo data"""
        print("🔍 DEBUG: Generating simulated data...")
        sys.stdout.flush()
        periods = []
        results = []
        current_time = int(time.time() * 1000)
        
        for i in range(100):
            period = current_time - (i * 60000)
            if i % 20 == 0:
                result = "B"
            elif i % 15 == 0:
                result = "S"
            else:
                result = np.random.choice(["B", "S"], p=[0.45, 0.55])
            periods.append(period)
            results.append(result)
        
        print(f"✅ DEBUG: Generated {len(results)} data points")
        sys.stdout.flush()
        return {"periods": periods, "results": results}

    def calculate_features(self, data):
        """Advanced feature engineering from original quantum system"""
        print("🔍 DEBUG: Calculating features...")
        sys.stdout.flush()
        results = data["results"]
        
        features = {
            "big_count_5": results[-5:].count("B"),
            "small_count_5": results[-5:].count("S"),
            "big_count_10": results[-10:].count("B"),
            "small_count_10": results[-10:].count("S"),
            "current_streak": self.get_current_streak(results),
            "volatility": self.calculate_volatility(results[-20:]),
            "pattern_score": self.pattern_recognition(results),
            "trend_strength": self.trend_analysis(results)
        }
        
        print(f"✅ DEBUG: Features calculated: {features}")
        sys.stdout.flush()
        return features

    def get_current_streak(self, results):
        """Calculate current streak length"""
        if not results:
            return 0
        last_result = results[-1]
        streak = 0
        for result in reversed(results):
            if result == last_result:
                streak += 1
            else:
                break
        return streak

    def calculate_volatility(self, results):
        """Calculate market volatility"""
        if len(results) < 2:
            return 0
        changes = []
        for i in range(1, len(results)):
            changes.append(1 if results[i] != results[i-1] else 0)
        return sum(changes) / len(changes) if changes else 0

    def pattern_recognition(self, results):
        """Advanced pattern recognition from original system"""
        if len(results) < 10:
            return 0.5
        
        recent = results[-10:]
        pattern_score = 0
        
        alternations = 0
        for i in range(1, len(recent)):
            if recent[i] != recent[i-1]:
                alternations += 1
        pattern_score += alternations / 9 * 0.3
        
        if self.get_current_streak(recent) >= 3:
            pattern_score += 0.4
        
        return min(pattern_score, 1.0)

    def trend_analysis(self, results):
        """Trend strength analysis"""
        if len(results) < 5:
            return 0.5
        
        recent = results[-5:]
        big_count = recent.count("B")
        small_count = recent.count("S")
        
        trend_strength = abs(big_count - small_count) / 5
        return trend_strength

    def neural_lite_prediction(self, features):
        """Lightweight neural network inspired prediction"""
        print("🔍 DEBUG: Running neural lite prediction...")
        sys.stdout.flush()
        
        weights = {
            "big_count_5": 0.15,
            "small_count_5": -0.15,
            "big_count_10": 0.10,
            "small_count_10": -0.10,
            "current_streak": 0.25,
            "volatility": -0.20,
            "pattern_score": 0.30,
            "trend_strength": 0.20
        }
        
        prediction_score = 0
        for feature, value in features.items():
            prediction_score += weights.get(feature, 0) * value
        
        probability = 1 / (1 + np.exp(-prediction_score))
        print(f"✅ DEBUG: Neural prediction: {probability:.3f}")
        sys.stdout.flush()
        return probability

    def statistical_analysis(self, features):
        """Statistical probability calculation"""
        print("🔍 DEBUG: Running statistical analysis...")
        sys.stdout.flush()
        big_prob = features["big_count_5"] / 5 * 0.6 + features["big_count_10"] / 10 * 0.4
        print(f"✅ DEBUG: Statistical prediction: {big_prob:.3f}")
        sys.stdout.flush()
        return big_prob

    def combine_strategies(self, features):
        """Combine multiple AI strategies with adaptive weights"""
        print("🔍 DEBUG: Combining strategies...")
        sys.stdout.flush()
        
        neural_pred = self.neural_lite_prediction(features)
        statistical_pred = self.statistical_analysis(features)
        pattern_pred = features["pattern_score"]
        trend_pred = features["trend_strength"]
        
        weights = {
            "neural": 0.35,
            "statistical": 0.25,
            "pattern": 0.25,
            "trend": 0.15
        }
        
        if features["volatility"] > 0.7:
            weights["pattern"] += 0.1
            weights["trend"] -= 0.1
        elif features["volatility"] < 0.3:
            weights["statistical"] += 0.1
            weights["neural"] -= 0.1
        
        final_prediction = (
            neural_pred * weights["neural"] +
            statistical_pred * weights["statistical"] +
            pattern_pred * weights["pattern"] +
            trend_pred * weights["trend"]
        )
        
        print(f"✅ DEBUG: Final prediction score: {final_prediction:.3f}")
        print(f"✅ DEBUG: Strategy weights: {weights}")
        sys.stdout.flush()
        
        return final_prediction, weights

    def make_prediction(self):
        """Make expert prediction using combined AI strategies"""
        print("🔍 DEBUG: Starting make_prediction...")
        sys.stdout.flush()
        try:
            historical_data = self.get_historical_data()
            features = self.calculate_features(historical_data)
            final_probability, strategy_weights = self.combine_strategies(features)
            
            prediction = "B" if final_probability > 0.5 else "S"
            confidence = final_probability if prediction == "B" else 1 - final_probability
            
            print(f"🎯 DEBUG: Final Prediction: {prediction} (Confidence: {confidence:.2f})")
            sys.stdout.flush()
            
            return {
                "prediction": prediction,
                "confidence": confidence,
                "strategy_weights": strategy_weights,
                "features": features
            }
            
        except Exception as e:
            print(f"❌ DEBUG: Prediction error: {e}")
            sys.stdout.flush()
            return {"prediction": "B", "confidence": 0.5, "error": str(e)}

    def send_telegram_message(self, message):
        """Send message to Telegram channel with debug info"""
        print("🔍 DEBUG: Starting Telegram send...")
        sys.stdout.flush()
        try:
            print(f"🔍 DEBUG: Token: {self.telegram_bot_token[:10]}..." if self.telegram_bot_token else "❌ DEBUG: No token")
            print(f"🔍 DEBUG: Channel ID: {self.telegram_channel_id}")
            sys.stdout.flush()
            
            if not self.telegram_bot_token or not self.telegram_channel_id:
                print("❌ DEBUG: Missing token or channel ID")
                sys.stdout.flush()
                return False
                
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_channel_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            print("🔍 DEBUG: Sending request to Telegram...")
            sys.stdout.flush()
            response = requests.post(url, json=payload, timeout=10)
            print(f"🔍 DEBUG: Response status: {response.status_code}")
            print(f"🔍 DEBUG: Response text: {response.text}")
            sys.stdout.flush()
            
            if response.status_code == 200:
                print("✅ DEBUG: Telegram message sent successfully!")
                sys.stdout.flush()
                return True
            else:
                print(f"❌ DEBUG: Telegram API error: {response.status_code}")
                sys.stdout.flush()
                return False
        except Exception as e:
            print(f"❌ DEBUG: Telegram send error: {e}")
            sys.stdout.flush()
            return False

    def save_prediction(self, prediction_data):
        """Save prediction to database"""
        print("🔍 DEBUG: Saving prediction to database...")
        sys.stdout.flush()
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO predictions (timestamp, period, prediction, strategy_used, confidence)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                int(time.time() * 1000),
                prediction_data["prediction"],
                str(prediction_data["strategy_weights"]),
                prediction_data["confidence"]
            ))
            conn.commit()
            conn.close()
            print("✅ DEBUG: Prediction saved to database")
            sys.stdout.flush()
        except Exception as e:
            print(f"❌ DEBUG: Database save error: {e}")
            sys.stdout.flush()

    def format_prediction_message(self, prediction_data):
        """Format beautiful Telegram message"""
        print("🔍 DEBUG: Formatting Telegram message...")
        sys.stdout.flush()
        
        prediction = prediction_data["prediction"]
        confidence = prediction_data["confidence"]
        features = prediction_data.get("features", {})
        
        emoji = "🔴" if prediction == "B" else "🔵"
        confidence_color = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.6 else "🟠"
        
        message = f"""
{emoji} <b>QUANTUM EXPERT PREDICTION</b> {emoji}

🎯 <b>Prediction:</b> <code>{prediction}</code>
📊 <b>Confidence:</b> <code>{confidence:.2%}</code> {confidence_color}

<b>Advanced Analysis:</b>
📈 Big Count (5): <code>{features.get('big_count_5', 0)}</code>
📉 Small Count (5): <code>{features.get('small_count_5', 0)}</code>
🔥 Current Streak: <code>{features.get('current_streak', 0)}</code>
⚡ Volatility: <code>{features.get('volatility', 0):.2f}</code>

<b>AI Strategies:</b>
🧠 Neural Lite: <code>{prediction_data['strategy_weights'].get('neural', 0):.2%}</code>
📊 Statistical: <code>{prediction_data['strategy_weights'].get('statistical', 0):.2%}</code>
🎯 Pattern Rec: <code>{prediction_data['strategy_weights'].get('pattern', 0):.2%}</code>
📈 Trend Analysis: <code>{prediction_data['strategy_weights'].get('trend', 0):.2%}</code>

⏰ <i>Generated: {datetime.now().strftime('%H:%M:%S')}</i>
        """
        print("✅ DEBUG: Message formatted")
        sys.stdout.flush()
        return message.strip()

    def run(self):
        """Main execution function"""
        print("🔍 DEBUG: Entering run method")
        sys.stdout.flush()
        try:
            print("🎯 START: Quantum Expert System Running...")
            sys.stdout.flush()
            
            # Make expert prediction
            print("🔍 DEBUG: Before make_prediction")
            sys.stdout.flush()
            prediction_data = self.make_prediction()
            print(f"🔍 DEBUG: Prediction data: {prediction_data}")
            sys.stdout.flush()
            
            # Format and send message
            print("🔍 DEBUG: Before format_prediction_message")
            sys.stdout.flush()
            message = self.format_prediction_message(prediction_data)
            print("🔍 DEBUG: Before send_telegram_message")
            sys.stdout.flush()
            
            telegram_success = self.send_telegram_message(message)
            print(f"🔍 DEBUG: Telegram success: {telegram_success}")
            sys.stdout.flush()
            
            # Save to database
            print("🔍 DEBUG: Before save_prediction")
            sys.stdout.flush()
            self.save_prediction(prediction_data)
            
            print("✅ SUCCESS: Quantum Expert System completed successfully")
            sys.stdout.flush()
            
        except Exception as e:
            print(f"❌ ERROR: System error: {e}")
            sys.stdout.flush()
            try:
                self.send_telegram_message(f"❌ System Error: {str(e)}")
            except:
                print("❌ DEBUG: Could not send error message to Telegram")
                sys.stdout.flush()

if __name__ == "__main__":
    print("🎯 MAIN: Starting Quantum Expert System")
    sys.stdout.flush()
    expert_system = QuantumExpertSystem()
    expert_system.run()
    print("🏁 MAIN: Script completed")
    sys.stdout.flush()
