"""
Agent module: An agent that realizes three types of investment psychology
Based on the BDI framework (Belief, Desire, Intention)
"""
import random
from typing import Dict, List, Optional
from llm_client import llm_client

class Agent:
    """Basic agent class"""
    
    def __init__(self, name: str, agent_type: str, initial_cash: float = 10000.0):
        """
        Initialize the agent
        
        Args:
            name: agent name
            agent_type: class of agent ('optimistic', 'pessimistic', 'calm')
            initial_cash: initial cash of agent
        """
        self.name = name
        self.agent_type = agent_type
        self.cash = initial_cash
        self.shares = 0
        self.beliefs = {}  # beliefs about the market
        self.desires = {}  # desires: investment goals
        self.intentions = []  # intentions: planned actions
        self.opinions = []  # opinions: published opinions
        self.trade_history = []  # trade history
        
        # initialize beliefs and desires based on agent type
        self._initialize_personality()
    
    def _initialize_personality(self):
        """initialize personality based on agent type"""
        if self.agent_type == 'optimistic':
            self.beliefs['market_outlook'] = 'positive'
            self.beliefs['risk_tolerance'] = 'high'
            self.desires['target_return'] = 0.15  # target return rate: 15%
        elif self.agent_type == 'pessimistic':
            self.beliefs['market_outlook'] = 'negative'
            self.beliefs['risk_tolerance'] = 'low'
            self.desires['target_return'] = 0.05  # target return rate: 5%
        else:  # calm
            self.beliefs['market_outlook'] = 'neutral'
            self.beliefs['risk_tolerance'] = 'medium'
            self.desires['target_return'] = 0.08  # target return rate: 8%
    
    def update_beliefs(self, news: Dict, current_price: float, market_sentiment: Dict):
        """
        update beliefs: based on news, price and market sentiment
        
        Args:
            news: news information {'content': str, 'sentiment': 'positive'/'negative'/'neutral'}
            current_price: current price
            market_sentiment: market sentiment {'optimistic': float, 'pessimistic': float, 'calm': float}
        """
        # update beliefs using LLM
        prompt = self._create_belief_update_prompt(news, current_price, market_sentiment)
        messages = [{"role": "user", "content": prompt}]
        response = llm_client.generate_response(messages, temperature=0.7)
        
        # parse response and update beliefs
        self._parse_belief_response(response, news)
    
    def _create_belief_update_prompt(self, news: Dict, current_price: float, market_sentiment: Dict) -> str:
        """create belief update prompt"""
        prompt = f"""You are a {self._get_type_description()} investor, named {self.name}.

the current market situation:
- price: {current_price:.2f}
- news: {news['content']}
- news sentiment: {news['sentiment']}
- market sentiment distribution: optimistic {market_sentiment.get('optimistic', 0):.2f}, pessimistic {market_sentiment.get('pessimistic', 0):.2f}, calm {market_sentiment.get('calm', 0):.2f}

your current beliefs:
- market outlook: {self.beliefs.get('market_outlook', 'unknown')}
- risk tolerance: {self.beliefs.get('risk_tolerance', 'unknown')}

Please analyze the current situation and briefly state:
1. your opinion on this news (1-2 sentences)
2. your opinion on the price change (up/down/flat)
3. your market outlook changed or not (positive/negative/neutral)

Please answer in simple Chinese words"""
        return prompt
    
    def _get_type_description(self) -> str:
        """get type description"""
        descriptions = {
            'optimistic': 'optimistic,tend to see the positive side,risk tolerance is high',
            'pessimistic': 'pessimistic,tend to see the risk,risk tolerance is low',
            'calm': 'calm,based on data analysis to make decisions'
        }
        return descriptions.get(self.agent_type, '')
    
    def _parse_belief_response(self, response: str, news: Dict):
        """parse LLM response and update beliefs"""
        # simple keyword matching to update beliefs
        response_lower = response.lower()
        
        if 'up' in response or 'positive' in response_lower or 'optimistic' in response:
            if self.agent_type == 'optimistic':
                self.beliefs['market_outlook'] = 'very_positive'
            elif self.agent_type == 'pessimistic':
                self.beliefs['market_outlook'] = 'slightly_positive'
        elif 'down' in response or 'negative' in response_lower or 'pessimistic' in response:
            if self.agent_type == 'pessimistic':
                self.beliefs['market_outlook'] = 'very_negative'
            elif self.agent_type == 'optimistic':
                self.beliefs['market_outlook'] = 'slightly_negative'
        
        # save opinions
        self.opinions.append({
            'news': news['content'],
            'response': response,
            'timestamp': len(self.opinions)
        })
    
    def form_intention(self, current_price: float) -> Dict:
        """
        form investment intention: decide to buy, sell or hold
        
        Returns:
            Dict: {'action': 'buy'/'sell'/'hold', 'quantity': int, 'reason': str}
        """
        # use LLM to form intention
        prompt = self._create_intention_prompt(current_price)
        messages = [{"role": "user", "content": prompt}]
        response = llm_client.generate_response(messages, temperature=0.6)
        
        # parse response
        intention = self._parse_intention_response(response, current_price)
        self.intentions.append(intention)
        return intention
    
    def _create_intention_prompt(self, current_price: float) -> str:
        """create intention formation prompt"""
        prompt = f"""You are{self.name}, a {self._get_type_description()} investor.

the current situation:
- price: {current_price:.2f}
- your cash: {self.cash:.2f}
- your shares: {self.shares}
- your market outlook: {self.beliefs.get('market_outlook', 'unknown')}

Please decide your investment action. You can only choose one of the following:
1. buy (if you think the price will go up)
2. sell (if you think the price will go down or need to sell)
3. hold (if you think you should look on)

Please answer in the following format:
action: [buy/sell/hold]
quantity: [if you buy, the maximum number of shares you can buy based on your cash; if you sell, the maximum number of shares you can sell based on your shares; if you hold, write 0]
reason: [briefly explain the reason, 1-2 sentences]"""
        return prompt
    
    def _parse_intention_response(self, response: str, current_price: float) -> Dict:
        """parse intention response"""
        response_lower = response.lower()
        
        # default hold
        action = 'hold'
        quantity = 0
        reason = "looking on"
        
        # Try to extract quantity from response first
        if 'quantity:' in response_lower:
            try:
                quantity_start = response_lower.find('quantity:')
                if quantity_start != -1:
                    quantity_str = response[quantity_start:].split('\n')[0].replace('quantity:', '').strip()
                    # Extract number from string
                    import re
                    numbers = re.findall(r'\d+', quantity_str)
                    if numbers:
                        parsed_quantity = int(numbers[0])
                        if parsed_quantity > 0:
                            quantity = parsed_quantity
            except:
                pass
        
        # parse action (compatible with replies that do not strictly follow the format)
        if 'action:' in response_lower:
            action_line = response_lower[response_lower.find('action:'):].split('\n')[0]
            if 'buy' in action_line:
                action = 'buy'
            elif 'sell' in action_line:
                action = 'sell'
            else:
                action = 'hold'
        else:
            # fallback: as long as the buy/sell keywords appear, execute
            if 'buy' in response_lower:
                action = 'buy'
            elif 'sell' in response_lower:
                action = 'sell'
            else:
                action = 'hold'
        
        # If quantity was not parsed from response, calculate it based on action and agent type
        if quantity == 0:
            if action == 'buy':
                max_shares = int(self.cash / current_price)
                if max_shares > 0:
                    # decide the buy ratio based on the type
                    if self.agent_type == 'optimistic':
                        quantity = max(1, min(max_shares, int(max_shares * 0.8)))  # optimistic investor buys 80%
                    elif self.agent_type == 'pessimistic':
                        quantity = max(1, min(max_shares, int(max_shares * 0.3)))  # pessimistic investor buys 30%
                    else:
                        quantity = max(1, min(max_shares, int(max_shares * 0.5)))  # calm investor buys 50%
            elif action == 'sell':
                if self.shares > 0:
                    if self.agent_type == 'pessimistic':
                        quantity = max(1, int(self.shares * 0.7))  # pessimistic investor sells 70%
                    elif self.agent_type == 'optimistic':
                        quantity = max(1, int(self.shares * 0.2))  # optimistic investor sells 20%
                    else:
                        quantity = max(1, int(self.shares * 0.4))  # calm investor sells 40%
                    quantity = min(quantity, self.shares)  # not more than the shares
        
        # extract reason
        if 'reason:' in response_lower:
            reason_start = response.find('reason:')
            if reason_start != -1:
                reason = response[reason_start:].split('\n')[0].replace('reason:', '').strip()
        else:
            # Use response as reason if no reason field
            reason = response[:100]  # Limit length
        
        return {
            'action': action,
            'quantity': quantity,
            'reason': reason,
            'response': response
        }
    
    def execute_trade(self, intention: Dict, current_price: float) -> Optional[Dict]:
        """
        execute trade
        
        Returns:
            Dict: trade record {'action': str, 'quantity': int, 'price': float, 'timestamp': int}
        """
        action = intention['action']
        quantity = intention['quantity']
        
        if action == 'buy' and quantity > 0:
            cost = quantity * current_price
            if cost <= self.cash:
                self.cash -= cost
                self.shares += quantity
                trade = {
                    'action': 'buy',
                    'quantity': quantity,
                    'price': current_price,
                    'cost': cost
                }
                self.trade_history.append(trade)
                return trade
        
        elif action == 'sell' and quantity > 0:
            if quantity <= self.shares:
                revenue = quantity * current_price
                self.cash += revenue
                self.shares -= quantity
                trade = {
                    'action': 'sell',
                    'quantity': quantity,
                    'price': current_price,
                    'revenue': revenue
                }
                self.trade_history.append(trade)
                return trade
        
        return None
    
    def get_portfolio_value(self, current_price: float) -> float:
        """calculate the total value of the portfolio"""
        return self.cash + self.shares * current_price
    
    def get_sentiment_score(self) -> float:
        """get sentiment score (-1 to 1, -1 most pessimistic, 1 most optimistic)"""
        outlook = self.beliefs.get('market_outlook', 'neutral')
        scores = {
            'very_positive': 0.9,
            'positive': 0.6,
            'slightly_positive': 0.3,
            'neutral': 0.0,
            'slightly_negative': -0.3,
            'negative': -0.6,
            'very_negative': -0.9
        }
        return scores.get(outlook, 0.0)

