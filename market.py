"""
Market Simulation Engine: Manages stocks, news, and price calculations
"""
import random
import numpy as np
from typing import List, Dict
from datetime import datetime, timedelta

class Market:
    """Market class: Manages stocks and market environment"""
    
    def __init__(self, initial_price: float = 100.0):
        """
        Initialize market
        
        Args:
            initial_price: initial stock price
        """
        self.initial_price = initial_price
        self.current_price = initial_price
        self.price_history = [initial_price]
        self.news_history = []
        self.trades_history = []
        self.sentiment_history = []
        self.timestep = 0
        self.base_value = initial_price  # base value
        
        # news templates
        self.positive_news_templates = [
            "The company released better-than-expected financial results, with net profit rising 30% year-on-year.",
            "The company has been granted a significant patent, further expanding its technological edge.",
            "The company has entered into a strategic cooperation agreement with an industry leader.",
            "The company's new product has garnered an enthusiastic market response, with orders surging significantly.",
            "Analysts raised the company's target price and are optimistic about its future development prospects.",
            "The company announced a large-scale share repurchase plan, demonstrating management confidence",
            "With favorable industry policies, the company is expected to benefit.",
            "The company's overseas business expansion has been smooth and its market share has increased."
        ]
        
        self.negative_news_templates = [
            "The company's financial report fell short of expectations, with net profit dropping by 20% year-on-year.",
            "The company is facing a major lawsuit, which may result in significant compensation claims.",
            "The company's main customers have lost interest and the order volume has decreased significantly.",
            "The industry regulatory policy has tightened and the company's business has been affected.",
            "The company's senior management has left, causing market concerns.",
            "The company's product has quality issues and is facing a recall risk.",
            "Analysts downgraded the company's rating and significantly lowered the target price.",
            "The company's cash flow is tight and the debt repayment pressure is increasing."
        ]
        
        self.neutral_news_templates = [
            "The company released a routine announcement, with no major changes.",
            "The overall market is volatile, and the company's stock price follows the adjustment.",
            "The company participated in the industry conference and shared development experience.",
            "The company completed routine business adjustments and is operating normally."
        ]
    
    def generate_news(self) -> Dict:
        """
        Generate random news
        
        Returns:
            Dict: {'content': str, 'sentiment': 'positive'/'negative'/'neutral', 'timestamp': int}
        """
        # randomly select news type (70% probability of news, 30% probability of no news)
        if random.random() < 0.7:
            sentiment_weights = [0.4, 0.4, 0.2]  # positive, negative, neutral weights
            sentiment_idx = np.random.choice([0, 1, 2], p=sentiment_weights)
            sentiments = ['positive', 'negative', 'neutral']
            sentiment = sentiments[sentiment_idx]
            
            if sentiment == 'positive':
                content = random.choice(self.positive_news_templates)
            elif sentiment == 'negative':
                content = random.choice(self.negative_news_templates)
            else:
                content = random.choice(self.neutral_news_templates)
        else:
            sentiment = 'neutral'
            content = "Today's market is calm, no major news"
        
        news = {
            'content': content,
            'sentiment': sentiment,
            'timestamp': self.timestep
        }
        
        self.news_history.append(news)
        return news
    
    def calculate_price(self, net_order_flow: float, news_impact: float = 0.0) -> float:
        """
        Calculate new stock price (based on supply and demand model)
        
        Args:
            net_order_flow: net order flow (buy is positive, sell is negative)
            news_impact: news impact (positive is positive, negative is negative)
        
        Returns:
            float: new stock price
        """
        # base random walk
        random_walk = np.random.normal(0, 0.01) * self.current_price
        
        # order flow impact (buy more涨，sell more跌）
        order_impact = net_order_flow * 0.1  # order flow impact coefficient
        
        # news impact
        news_impact_value = news_impact * self.current_price * 0.05
        
        # price adjustment
        price_change = random_walk + order_impact + news_impact_value
        
        # update price
        new_price = self.current_price + price_change
        
        # prevent price from being too low
        new_price = max(new_price, self.initial_price * 0.3)
        
        self.current_price = new_price
        self.price_history.append(new_price)
        return new_price
    
    def get_news_impact_score(self, news: Dict) -> float:
        """
        Get news impact score
        
        Returns:
            float: score between -1 and 1, -1 most negative, 1 most positive
        """
        sentiment_scores = {
            'positive': 0.7,
            'negative': -0.7,
            'neutral': 0.0
        }
        return sentiment_scores.get(news['sentiment'], 0.0)
    
    def update(self, trades: List[Dict], news: Dict):
        """
        Update market state
        
        Args:
            trades: trade list
            news: news information
        """
        # calculate net order flow
        net_order_flow = 0
        for trade in trades:
            if trade['action'] == 'buy':
                net_order_flow += trade['quantity']
            elif trade['action'] == 'sell':
                net_order_flow -= trade['quantity']
        
        # calculate news impact
        news_impact = self.get_news_impact_score(news)
        
        # update price
        self.calculate_price(net_order_flow, news_impact)
        
        # record trades
        self.trades_history.append({
            'trades': trades,
            'net_order_flow': net_order_flow,
            'timestamp': self.timestep
        })
        
        self.timestep += 1
    
    def get_market_statistics(self) -> Dict:
        """Get market statistics"""
        if len(self.price_history) < 2:
            return {}
        
        prices = np.array(self.price_history)
        returns = np.diff(prices) / prices[:-1]
        
        return {
            'current_price': self.current_price,
            'price_change': self.current_price - self.initial_price,
            'price_change_pct': (self.current_price - self.initial_price) / self.initial_price * 100,
            'volatility': np.std(returns) if len(returns) > 0 else 0,
            'max_price': np.max(prices),
            'min_price': np.min(prices)
        }

