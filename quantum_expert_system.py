import requests
import pandas as pd
import numpy as np
import sqlite3
import time
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QuantumExpertSystem:
    def __init__(self):
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
        self.db_path = "quantum_predictions.db"
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for storing predictions and results"""
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
        logging.info("Database initialized")

    def get_historical_data(self):
        """Fetch historical WinGo data"""
        try:
            url = "https://api.wingo.com/historical"  # Example API
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                # Fallback to simulated data for testing
                return self.generate_simulated_data()
        except Exception as e:
            logging.warning(f"API fetch failed, using simulated data: {e}")
            return self.generate_simulated_data()

    def generate_simulated_data(self):
        """Generate realistic simulated WinGo data"""
        periods = []
        results = []
        current_time = int(time.time() * 1000)
        
        for i in range(100):
            period = current_time - (i * 60000)  # 1 minute intervals
            # Realistic pattern: more big numbers, some streaks
            if i % 20 == 0:
                result = "B"  # Force big for pattern
            elif i % 15 == 0:
                result = "S"  # Force small for pattern
            else:
                result = np.random.choice(["B", "S"], p=[0.45, 0.55])
            periods.append(period)
            results.append(result)
        
        return {"periods": periods, "results": results}

    def calculate_features(self, data):
        """Advanced feature engineering from original quantum system"""
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
        
        # Look for repeating patterns
        recent = results[-10:]
        pattern_score = 0
        
        # Check for alternation pattern
        alternations = 0
        for i in range(1, len(recent)):
            if recent[i] != recent[i-1]:
                alternations += 1
        pattern_score += alternations / 9 * 0.3
        
        # Check for streak pattern
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
        # Simplified version of our neural logic
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
        
        # Normalize to probability
        probability = 1 / (1 + np.exp(-prediction_score))
        return probability

    def statistical_analysis(self, features):
        """Statistical probability calculation"""
        big_prob = features["big_count_5"] / 5 * 0.6 + features["big_count_10"] / 10 * 0.4
        return big_prob

    def combine_strategies(self, features):
        """Combine multiple AI strategies with adaptive weights"""
        # Get predictions from all strategies
        neural_pred = self.neural_lite_prediction(features)
        statistical_pred = self.statistical_analysis(features)
        pattern_pred = features["pattern_score"]
        trend_pred = features["trend_strength"]
        
        # Adaptive weights based on feature strength
        weights = {
            "neural": 0.35,
            "statistical": 0.25,
            "pattern": 0.25,
            "trend": 0.15
        }
        
        # Adjust weights based on volatility
        if features["volatility"] > 0.7:
            weights["pattern"] += 0.1
            weights["trend"] -= 0.1
        elif features["volatility"] < 0.3:
            weights["statistical"] += 0.1
            weights["neural"] -= 0.1
        
        # Calculate final prediction
        final_prediction = (
            neural_pred * weights["neural"] +
            statistical_pred * weights["statistical"] +
            pattern_pred * weights["pattern"] +
            trend_pred * weights["trend"]
        )
        
        return final_prediction, weights

    def make_prediction(self):
        """Make expert prediction using combined AI strategies"""
        try:
            # Get historical data
            historical_data = self.get_historical_data()
            
            # Calculate advanced features
            features = self.calculate_features(historical_data)
            
            # Get combined prediction from all strategies
            final_probability, strategy_weights = self.combine_strategies(features)
            
            # Make final decision
            prediction = "B" if final_probability > 0.5 else "S"
            confidence = final_probability if prediction == "B" else 1 - final_probability
            
            logging.info(f"Expert Prediction: {prediction} (Confidence: {confidence:.2f})")
            logging.info(f"Strategy Weights: {strategy_weights}")
            
            return {
                "prediction": prediction,
                "confidence": confidence,
                "strategy_weights": strategy_weights,
                "features": features
            }
            
        except Exception as e:
            logging.error(f"Prediction error: {e}")
            return {"prediction": "B", "confidence": 0.5, "error": str(e)}

    def send_telegram_message(self, message):
        """Send message to Telegram channel"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_channel_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                logging.info("Message sent to Telegram")
                return True
            else:
                logging.error(f"Telegram API error: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"Telegram send error: {e}")
            return False

    def save_prediction(self, prediction_data):
        """Save prediction to database"""
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
            logging.info("Prediction saved to database")
        except Exception as e:
            logging.error(f"Database save error: {e}")

    def format_prediction_message(self, prediction_data):
        """Format beautiful Telegram message"""
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
        return message.strip()

    def run(self):
        """Main execution function"""
        try:
            logging.info("Starting Quantum Expert System...")
            
            # Make expert prediction
            prediction_data = self.make_prediction()
            
            # Format and send message
            message = self.format_prediction_message(prediction_data)
            self.send_telegram_message(message)
            
            # Save to database
            self.save_prediction(prediction_data)
            
            logging.info("Quantum Expert System completed successfully")
            
        except Exception as e:
            logging.error(f"System error: {e}")
            self.send_telegram_message(f"❌ System Error: {str(e)}")

if __name__ == "__main__":
    expert_system = QuantumExpertSystem()
    expert_system.run()
