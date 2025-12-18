"""
Streamlit Interactive Interface: Visual Market simulation
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from simulator import MarketSimulator
from config import INITIAL_STOCK_PRICE

# page configuration
st.set_page_config(
    page_title="Stock Market Sentiment Agent Simulator",
    page_icon="📈",
    layout="wide"
)

# compatibility function: handle different Streamlit versions of rerun
def rerun():
    """handle different Streamlit versions of rerun"""
    if hasattr(st, 'rerun'):
        st.rerun()
    elif hasattr(st, 'experimental_rerun'):
        st.experimental_rerun()
    else:
        raise Exception("cannot find rerun function")

def init_session_state():
    """initialize session state"""
    st.session_state.setdefault('simulator', MarketSimulator(INITIAL_STOCK_PRICE))
    st.session_state.setdefault('is_running', False)
    st.session_state.setdefault('auto_step', False)

def get_simulator():
    """get simulator instance, ensure it is initialized"""
    init_session_state()
    # Prioritize dictionary access to avoid attribute access triggering missing errors
    if st.session_state.get('simulator') is None:
        st.session_state['simulator'] = MarketSimulator(INITIAL_STOCK_PRICE)
    return st.session_state['simulator']

def main():
    """main function"""
    # ensure session state is initialized
    init_session_state()
    
    st.title("📈 Stock Market Sentiment Agent Simulator")
    st.markdown("""
    This simulator shows how three different types of investors (optimistic, pessimistic, calm)
    respond to news events and influence stock price,
    whcih visually demonstrates market sentiment, herd behavior, and other behavioral finance phenomena.
    """)
    
    # sidebar control
    with st.sidebar:
        st.header("⚙️ Control Panel")
        
        # reset button
        if st.button("🔄 Reset Simulation"):
            sim = get_simulator()
            sim.reset()
            st.session_state.is_running = False
            st.session_state.auto_step = False
            rerun()
        
        st.markdown("---")
        
        # single step execution
        if st.button("▶️ Execute one step"):
            sim = get_simulator()
            step_data = sim.step()
            st.session_state.is_running = True
            rerun()

        # automatic running feature is disabled to avoid blocking
        st.info("Click once to 'Execute one step' to simulate one transaction.")
        
        st.markdown("---")
        
        # display current state
        st.subheader("📊 Current State")
        sim = get_simulator()
        stats = sim.get_statistics()
        if stats:
            st.metric("current stock price", f"¥{stats.get('current_price', 0):.2f}")
            price_change_pct = stats.get('price_change_pct', 0)
            st.metric("price change percentage", f"{price_change_pct:.2f}%")
            st.metric("total trades", stats.get('total_trades', 0))
            st.metric("time step", len(sim.simulation_history))
    
    # main content area
    sim = get_simulator()
    if len(sim.simulation_history) == 0:
        st.info("👆 Click the 'Execute one step' button in the sidebar to start the simulation.")
    
    # display latest news
    if sim.simulation_history:
        latest_step = sim.simulation_history[-1]
        news = latest_step.get('news', {})
        
        # news card
        sentiment_emoji = {
            'positive': '📰',
            'negative': '⚠️',
            'neutral': '📄'
        }
        sentiment_color = {
            'positive': 'green',
            'negative': 'red',
            'neutral': 'gray'
        }
        
        st.markdown(f"""
        <div style="padding: 15px; border-left: 4px solid {sentiment_color.get(news.get('sentiment', 'neutral'), 'gray')}; 
                    background-color: #f0f0f0; border-radius: 5px; margin-bottom: 20px;">
            <h3>{sentiment_emoji.get(news.get('sentiment', 'neutral'), '📄')} Latest News</h3>
            <p style="font-size: 16px;">{news.get('content', 'No news')}</p>
            <p style="color: {sentiment_color.get(news.get('sentiment', 'neutral'), 'gray')}; 
                      font-weight: bold;">sentiment: {news.get('sentiment', 'neutral')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # chart display
    if len(sim.simulation_history) > 0:
        # use radio button to create tabs (compatible with old version Streamlit)
        tab_options = [
            "📈 Price and Sentiment", 
            "💹 Trading Analysis", 
            "👥 Agent States", 
            "📊 Market Statistics"
        ]
        selected_tab = st.radio(
            "Select Content to View:",
            tab_options,
            horizontal=True
        )
        
        st.markdown("---")
        
        if selected_tab == tab_options[0]:
            show_price_sentiment_chart()
        elif selected_tab == tab_options[1]:
            show_trading_analysis()
        elif selected_tab == tab_options[2]:
            show_agent_states()
        elif selected_tab == tab_options[3]:
            show_market_statistics()

def show_price_sentiment_chart():
    """show price and sentiment chart"""
    sim = get_simulator()
    history = sim.simulation_history
    market = sim.market
    
    if len(history) < 2:
        st.info("At least 2 time steps are required to display the chart")
        return
    
    # prepare data
    timesteps = [h['timestep'] for h in history]
    prices = [h['price'] for h in history]
    
    # calculate sentiment index
    optimistic_scores = []
    pessimistic_scores = []
    calm_scores = []
    
    for h in history:
        sentiment = h.get('market_sentiment', {})
        optimistic_scores.append(sentiment.get('optimistic', 0))
        pessimistic_scores.append(sentiment.get('pessimistic', 0))
        calm_scores.append(sentiment.get('calm', 0))
    
    # create subplots
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Stock Price Change', 'Market Sentiment Index'),
        vertical_spacing=0.1,
        row_heights=[0.6, 0.4]
    )
    
    # price chart
    fig.add_trace(
        go.Scatter(
            x=timesteps,
            y=prices,
            mode='lines+markers',
            name='Stock Price',
            line=dict(color='blue', width=2),
            marker=dict(size=4)
        ),
        row=1, col=1
    )
    
    # add base value line
    fig.add_hline(
        y=market.initial_price,
        line_dash="dash",
        line_color="gray",
        annotation_text="Initial Price",
        row=1, col=1
    )
    
    # sentiment chart
    fig.add_trace(
        go.Scatter(
            x=timesteps,
            y=optimistic_scores,
            mode='lines',
            name='Optimistic Sentiment',
            line=dict(color='green', width=2)
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=timesteps,
            y=pessimistic_scores,
            mode='lines',
            name='Pessimistic Sentiment',
            line=dict(color='red', width=2)
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=timesteps,
            y=calm_scores,
            mode='lines',
            name='Calm Sentiment',
            line=dict(color='gray', width=2)
        ),
        row=2, col=1
    )
    
    # update layout
    fig.update_xaxes(title_text="Time Step", row=2, col=1)
    fig.update_yaxes(title_text="Price (¥)", row=1, col=1)
    fig.update_yaxes(title_text="Sentiment Score", row=2, col=1)
    fig.update_layout(height=700, showlegend=True)
    
    st.plotly_chart(fig)
    
    # display key information
    col1, col2, col3 = st.columns(3)
    with col1:
        current_price = prices[-1]
        initial_price = market.initial_price
        change_pct = (current_price - initial_price) / initial_price * 100
        st.metric("current price", f"¥{current_price:.2f}", f"{change_pct:.2f}%")
    
    with col2:
        latest_sentiment = history[-1].get('market_sentiment', {})
        avg_sentiment = (latest_sentiment.get('optimistic', 0) - latest_sentiment.get('pessimistic', 0)) / 2
        st.metric("market sentiment", f"{avg_sentiment:.2f}", 
                 "optimistic" if avg_sentiment > 0 else "pessimistic" if avg_sentiment < 0 else "neutral")
    
    with col3:
        volatility = np.std(np.diff(prices) / prices[:-1]) if len(prices) > 1 else 0
        st.metric("volatility", f"{volatility:.4f}")

def show_trading_analysis():
    """show trading analysis"""
    sim = get_simulator()
    history = sim.simulation_history
    
    if len(history) == 0:
        st.info("No trading data")
        return
    
    # collect all trades
    all_trades = []
    for h in history:
        trades = h.get('trades', [])
        for trade in trades:
            all_trades.append({
                'timestep': h['timestep'],
                'agent_name': trade.get('agent_name', ''),
                'agent_type': trade.get('agent_type', ''),
                'action': trade.get('action', ''),
                'quantity': trade.get('quantity', 0),
                'price': trade.get('price', 0)
            })
    
    if not all_trades:
        st.info("No trading record")
        return
    
    df_trades = pd.DataFrame(all_trades)
    
    # trading volume statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Trading Type Distribution")
        action_counts = df_trades['action'].value_counts()
        fig_pie = px.pie(
            values=action_counts.values,
            names=action_counts.index,
            color_discrete_map={'buy': 'green', 'sell': 'red', 'hold': 'gray'}
        )
        st.plotly_chart(fig_pie)
    
    with col2:
        st.subheader("Trading Volume by Agent Type")
        type_action = df_trades.groupby(['agent_type', 'action']).size().reset_index(name='count')
        fig_bar = px.bar(
            type_action,
            x='agent_type',
            y='count',
            color='action',
            color_discrete_map={'buy': 'green', 'sell': 'red'},
            labels={'agent_type': 'Agent Type', 'count': 'Trading Count'}
        )
        st.plotly_chart(fig_bar)
    
    # trading time series
    st.subheader("Trading Volume Time Series")
    trade_volume = df_trades.groupby('timestep').agg({
        'quantity': 'sum',
        'action': lambda x: (x == 'buy').sum() - (x == 'sell').sum()  # net buy
    }).reset_index()
    trade_volume.columns = ['timestep', 'total_volume', 'net_buy']
    
    fig_volume = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Total Trading Volume', 'Net Buy Volume'),
        vertical_spacing=0.1
    )
    
    fig_volume.add_trace(
        go.Bar(x=trade_volume['timestep'], y=trade_volume['total_volume'], name='Total Trading Volume'),
        row=1, col=1
    )
    
    fig_volume.add_trace(
        go.Bar(
            x=trade_volume['timestep'], 
            y=trade_volume['net_buy'],
            name='Net Buy Volume',
            marker_color=['green' if x > 0 else 'red' for x in trade_volume['net_buy']]
        ),
        row=2, col=1
    )
    
    fig_volume.update_xaxes(title_text="Time Step", row=2, col=1)
    fig_volume.update_yaxes(title_text="Trading Volume", row=1, col=1)
    fig_volume.update_yaxes(title_text="Net Buy Volume", row=2, col=1)
    fig_volume.update_layout(height=600, showlegend=False)
    
    st.plotly_chart(fig_volume)
    
    # trading detail table
    st.subheader("Trading Detail")
    st.dataframe(df_trades)

def show_agent_states():
    """show agent states"""
    sim = get_simulator()
    if not sim.simulation_history:
        st.info("No data")
        return
    
    latest_step = sim.simulation_history[-1]
    agent_states = latest_step.get('agent_states', [])
    
    if not agent_states:
        st.info("No agent states data")
        return
    
    df_agents = pd.DataFrame(agent_states)
    
    # agent states table
    st.subheader("Agent Current States")
    st.dataframe(df_agents)
    
    # portfolio value comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Portfolio Value")
        fig_portfolio = px.bar(
            df_agents,
            x='name',
            y='portfolio_value',
            color='type',
            labels={'name': 'Agent Name', 'portfolio_value': 'Portfolio Value (¥)', 'type': 'Type'},
            color_discrete_map={'optimistic': 'green', 'pessimistic': 'red', 'calm': 'blue'}
        )
        st.plotly_chart(fig_portfolio)
    
    with col2:
        st.subheader("Sentiment Score")
        fig_sentiment = px.bar(
            df_agents,
            x='name',
            y='sentiment_score',
            color='type',
            labels={'name': 'Agent Name', 'sentiment_score': 'Sentiment Score', 'type': 'Type'},
            color_discrete_map={'optimistic': 'green', 'pessimistic': 'red', 'calm': 'blue'}
        )
        fig_sentiment.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_sentiment)
    
    # display agent opinions
    st.subheader("Agent Latest Opinions")
    for agent in sim.agents:
        if agent.opinions:
            latest_opinion = agent.opinions[-1]
            with st.expander(f"{agent.name} ({agent.agent_type})"):
                st.write(f"**news:** {latest_opinion.get('news', '')}")
                st.write(f"**opinion:** {latest_opinion.get('response', '')}")

def show_market_statistics():
    """show market statistics"""
    sim = get_simulator()
    stats = sim.get_statistics()
    market = sim.market
    
    if not stats:
        st.info("No statistics data")
        return
    
    # key indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("current price", f"¥{stats.get('current_price', 0):.2f}")
    
    with col2:
        price_change = stats.get('price_change', 0)
        price_change_pct = stats.get('price_change_pct', 0)
        st.metric("price change", f"¥{price_change:.2f}", f"{price_change_pct:.2f}%")
    
    with col3:
        st.metric("highest price", f"¥{stats.get('max_price', 0):.2f}")
    
    with col4:
        st.metric("lowest price", f"¥{stats.get('min_price', 0):.2f}")
    
    st.markdown("---")
    
    # price distribution
    if len(market.price_history) > 1:
        st.subheader("Price Distribution")
        fig_dist = px.histogram(
            x=market.price_history,
            nbins=20,
            labels={'x': 'Price (¥)', 'count': 'Frequency'},
            title='Price Distribution Histogram'
        )
        st.plotly_chart(fig_dist)
    
    # return analysis
    if len(market.price_history) > 2:
        st.subheader("Return Analysis")
        returns = np.diff(market.price_history) / market.price_history[:-1]
        
        # indicators on top to avoid overlapping with chart
        met_col1, met_col2, met_col3, met_col4 = st.columns(4)
        with met_col1:
            st.metric("average return", f"{np.mean(returns):.4f}")
        with met_col2:
            st.metric("return volatility", f"{np.std(returns):.4f}")
        with met_col3:
            st.metric("maximum daily increase", f"{np.max(returns):.4%}")
        with met_col4:
            st.metric("maximum daily decrease", f"{np.min(returns):.4%}")

        # chart occupies one row to avoid text being blocked
        fig_returns = px.line(
            x=list(range(len(returns))),
            y=returns,
            labels={'x': 'Time Step', 'y': 'Return'},
            title='Return Time Series'
        )
        fig_returns.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_returns.update_layout(margin=dict(t=60, l=60, r=20, b=60), height=500)
        st.plotly_chart(fig_returns)

if __name__ == "__main__":
    main()

