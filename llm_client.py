"""
LLM Client: Integrates Baidu Wenxin API
"""
import os
try:
    import qianfan
    QIANFAN_AVAILABLE = True
except ImportError:
    QIANFAN_AVAILABLE = False
    print("Warning: qianfan package not installed, using mock response. To use real API, run: pip install qianfan")

from config import ACCESS_KEY, SECRET_KEY

class LLMClient:
    """Baidu Wenxin LLM Client"""
    
    def __init__(self):
        """Initialize client"""
        # Allow using mock mode through environment variables to avoid network/timeout blocking
        self.force_mock = os.getenv("USE_MOCK_LLM", "0") == "1"

        # Use environment variables first, then use configuration file
        ak = os.getenv('QIANFAN_ACCESS_KEY', ACCESS_KEY)
        sk = os.getenv('QIANFAN_SECRET_KEY', SECRET_KEY)
        
        if not self.force_mock and QIANFAN_AVAILABLE and ak and sk:
            try:
                self.chat_comp = qianfan.ChatCompletion(
                    ak=ak,
                    sk=sk
                )
                print("✓ Baidu Wenxin API initialized")
            except Exception as e:
                print(f"Warning: API initialization failed: {e}, using mock response")
                self.chat_comp = None
        else:
            self.chat_comp = None
            if self.force_mock:
                print("Hint: USE_MOCK_LLM=1 is enabled, using mock response mode")
            elif not QIANFAN_AVAILABLE:
                print("Hint: using mock response mode (qianfan package not installed)")
            elif not (ak and sk):
                print("Warning: API key not correctly configured, using mock response")
    
    def generate_response(self, messages, temperature=0.7):
        """
        Generate LLM response
        
        Args:
            messages: message list, format: [{"role": "user", "content": "..."}]
            temperature: temperature parameter, controls randomness
        
        Returns:
            str: LLM generated response text
        """
        if self.force_mock or self.chat_comp is None:
            # mock response (for testing)
            return self._mock_response(messages)
        
        try:
            # call Baidu Wenxin API
            response = self.chat_comp.do(
                model="ERNIE-Bot-turbo",
                messages=messages,
                temperature=temperature,
                timeout=8  # set timeout to prevent blocking
            )
            # handle response format
            if isinstance(response, dict):
                return response.get('result', '')
            elif isinstance(response, str):
                return response
            else:
                return str(response)
        except Exception as e:
            print(f"LLM API call error: {e}, using mock response")
            return self._mock_response(messages)
    
    def _mock_response(self, messages):
        """mock response (when API is not available)"""
        import random
        last_message = messages[-1]['content'] if messages else ""
        
        # For intention formation prompts, return formatted response
        if "action:" in last_message.lower() or "decide your investment action" in last_message.lower():
            # Extract agent type and market outlook from prompt
            if "optimistic" in last_message.lower():
                # Optimistic investors are more likely to buy
                if random.random() < 0.7:  # 70% chance to buy
                    return "action: buy\nquantity: 50\nreason: I am optimistic about the market and believe the price will rise."
                else:
                    return "action: hold\nquantity: 0\nreason: I will wait for a better entry point."
            elif "pessimistic" in last_message.lower():
                # Pessimistic investors are more likely to sell or hold
                if "shares: 0" in last_message or "shares:0" in last_message:
                    # No shares to sell, so hold
                    return "action: hold\nquantity: 0\nreason: I am cautious about the market but have no shares to sell."
                elif random.random() < 0.6:  # 60% chance to sell if has shares
                    return "action: sell\nquantity: 30\nreason: I am pessimistic about the market and want to reduce risk."
                else:
                    return "action: hold\nquantity: 0\nreason: I will wait and see."
            else:  # calm investor
                # Calm investors make balanced decisions
                if random.random() < 0.5:
                    return "action: buy\nquantity: 30\nreason: Based on analysis, this seems like a reasonable entry point."
                elif "shares: 0" not in last_message and "shares:0" not in last_message and random.random() < 0.3:
                    return "action: sell\nquantity: 20\nreason: Taking some profits based on current valuation."
                else:
                    return "action: hold\nquantity: 0\nreason: Waiting for more clarity before making a decision."
        
        # For belief update prompts
        if "买入" in last_message or "乐观" in last_message or "optimistic" in last_message.lower():
            return "Based on current information, I think this is a good time to buy. The market outlook is positive."
        elif "卖出" in last_message or "悲观" in last_message or "pessimistic" in last_message.lower():
            return "Based on current information, I think you should be cautious and consider selling. The market outlook is negative."
        else:
            return "I need more information to make a decision. The market outlook is neutral."

# global LLM client instance
llm_client = LLMClient()

