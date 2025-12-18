"""
Simulator Main Class: Coordinating Agents and Markets
"""
import numpy as np
from typing import List, Dict
from agent import Agent
from market import Market
from config import AGENT_TYPES, AGENT_NAMES

class MarketSimulator:
    """Market simulator"""
    
    def __init__(self, initial_price: float = 100.0):
        """
        Initialize simulator
        
        Args:
            initial_price: initial stock price
        """
        self.market = Market(initial_price)
        self.agents: List[Agent] = []
        self.simulation_history = []
        
        # create agents
        self._create_agents()
    
    def _create_agents(self):
        """create agents"""
        for agent_type in AGENT_TYPES:
            names = AGENT_NAMES.get(agent_type, [])
            for name in names:
                agent = Agent(name, agent_type)
                self.agents.append(agent)
    
    def step(self) -> Dict:
        """
        Execute one step of simulation
        
        Returns:
            Dict: dictionary containing all information for this step
        """
        # 1. generate news
        news = self.market.generate_news()
        
        # 2. calculate current market sentiment
        market_sentiment = self._calculate_market_sentiment()
        
        # 3. agents update beliefs
        for agent in self.agents:
            agent.update_beliefs(news, self.market.current_price, market_sentiment)
        
        # 4. agents form intentions
        intentions = []
        for agent in self.agents:
            intention = agent.form_intention(self.market.current_price)
            intentions.append({
                'agent_name': agent.name,
                'agent_type': agent.agent_type,
                'intention': intention
            })
        
        # 5. agents execute trades
        trades = []
        for agent in self.agents:
            intention = agent.intentions[-1] if agent.intentions else None
            if intention:
                trade = agent.execute_trade(intention, self.market.current_price)
                if trade:
                    trade['agent_name'] = agent.name
                    trade['agent_type'] = agent.agent_type
                    trades.append(trade)
        
        # 6. update market
        self.market.update(trades, news)
        
        # 7. record history
        step_data = {
            'timestep': self.market.timestep,
            'price': self.market.current_price,
            'news': news,
            'market_sentiment': market_sentiment,
            'intentions': intentions,
            'trades': trades,
            'agent_states': self._get_agent_states()
        }
        
        self.simulation_history.append(step_data)
        return step_data
    
    def _calculate_market_sentiment(self) -> Dict:
        """calculate market sentiment distribution"""
        sentiment_scores = {'optimistic': [], 'pessimistic': [], 'calm': []}
        
        for agent in self.agents:
            score = agent.get_sentiment_score()
            sentiment_scores[agent.agent_type].append(score)
        
        # calculate average sentiment
        market_sentiment = {
            'optimistic': np.mean(sentiment_scores['optimistic']) if sentiment_scores['optimistic'] else 0.0,
            'pessimistic': np.mean(sentiment_scores['pessimistic']) if sentiment_scores['pessimistic'] else 0.0,
            'calm': np.mean(sentiment_scores['calm']) if sentiment_scores['calm'] else 0.0
        }
        
        # record sentiment history
        self.market.sentiment_history.append(market_sentiment)
        
        return market_sentiment
    
    def _get_agent_states(self) -> List[Dict]:
        """get all agent states"""
        states = []
        for agent in self.agents:
            states.append({
                'name': agent.name,
                'type': agent.agent_type,
                'cash': agent.cash,
                'shares': agent.shares,
                'portfolio_value': agent.get_portfolio_value(self.market.current_price),
                'sentiment_score': agent.get_sentiment_score(),
                'market_outlook': agent.beliefs.get('market_outlook', 'unknown')
            })
        return states
    
    def reset(self):
        """reset simulator"""
        self.market = Market(self.market.initial_price)
        self.agents = []
        self.simulation_history = []
        self._create_agents()
    
    def get_statistics(self) -> Dict:
        """get simulation statistics"""
        stats = self.market.get_market_statistics()
        
        # add agent statistics - count trades from simulation history (more accurate)
        total_trades = 0
        for step_data in self.simulation_history:
            trades = step_data.get('trades', [])
            total_trades += len(trades)
        
        # Also count from agent trade history as backup
        agent_trade_count = sum(len(agent.trade_history) for agent in self.agents)
        # Use the larger value to ensure accuracy
        stats['total_trades'] = max(total_trades, agent_trade_count)
        stats['num_agents'] = len(self.agents)
        
        return stats

