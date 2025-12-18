# Stock Market Sentiment Agent Simulator

A LLM-based stock market sentiment simulator that demonstrates how three different types of investors (optimistic, pessimistic, and calm) respond to news events and influence stock prices.

## Features

- 🤖 **Three Agent Types**: Optimistic, pessimistic, and calm investors
- 📰 **Dynamic News Generation**: Positive, negative, and neutral news events
- 💹 **Real-time Price Calculation**: Based on supply-demand model and news impact
- 📊 **Interactive Visualization**: Price trends, sentiment indices, trading analysis
- 🧠 **LLM Decision Making**: Intelligent decisions based on Baidu Wenxin API

---

## How to Run the Code

### Method 1: Using Streamlit Command (Recommended)

1. **Install dependencies** (see Dependencies section below)
2. **Run the application**:
   ```bash
   streamlit run app.py
   ```
   Or using Python module:
   ```bash
   py -m streamlit run app.py
   ```

3. **Access the application**:
   - The application will automatically open in your browser at `http://localhost:8501`
   - If it doesn't open automatically, manually navigate to the URL above

### Method 2: Using Batch Scripts (Windows)

- **Quick start**: Double-click `start_app.bat`
- **Install and start**: Double-click `run.bat` (installs dependencies first, then starts the app)

### Method 3: Using Python Directly

```bash
python app.py
```

**Note**: The application uses Streamlit, so it must be run via `streamlit run` command for proper functionality.

---

## Dependencies and Environment Requirements

### Python Version
- **Python 3.8 or higher** is required

### Required Packages

All dependencies are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

#### Core Dependencies:

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | >=1.28.0 | Web application framework for the interactive UI |
| `pandas` | >=2.0.0 | Data manipulation and analysis |
| `numpy` | >=1.24.0 | Numerical computations |
| `plotly` | >=5.14.0 | Interactive data visualization |
| `qianfan` | >=0.3.0 | Baidu Qianfan API client (optional, for real LLM) |
| `python-dotenv` | >=1.0.0 | Environment variable management |

#### Optional Dependencies:

- `qianfan`: If not installed, the system will use mock responses (fully functional for testing)
- `matplotlib`: Listed in requirements but not actively used in current version

### API Configuration

The system uses **Baidu Wenxin API** for LLM-based decision making:

- **API Key**: Configured in `config.py` (already includes a default key)
- **Fallback Mode**: If API is unavailable or `qianfan` package is not installed, the system automatically uses mock responses
- **To use real API**: 
  1. Install `qianfan`: `pip install qianfan`
  2. Update API credentials in `config.py` if needed

### Environment Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python test_imports.py
   ```
   This will test if all modules can be imported successfully.

---

## Descriptions of Key Files and Folders

### Core Application Files

#### `app.py`
- **Purpose**: Main Streamlit application interface
- **Functionality**: 
  - Creates the web UI with interactive controls
  - Displays price charts, sentiment indices, trading analysis
  - Manages simulation state and user interactions
- **Key Components**: 
  - Price & Sentiment visualization
  - Trading Analysis dashboard
  - Agent States panel
  - Market Statistics view

#### `simulator.py`
- **Purpose**: Core simulation engine that coordinates agents and market
- **Functionality**:
  - Manages simulation steps and history
  - Coordinates agent decision-making
  - Calculates market sentiment
  - Records simulation data
- **Key Class**: `MarketSimulator`

#### `agent.py`
- **Purpose**: Defines the agent class with BDI (Belief, Desire, Intention) framework
- **Functionality**:
  - Implements three agent types: optimistic, pessimistic, calm
  - Updates beliefs based on news and market conditions
  - Forms investment intentions using LLM
  - Executes trades based on intentions
- **Key Class**: `Agent`

#### `market.py`
- **Purpose**: Market environment that manages stock prices and news generation
- **Functionality**:
  - Generates random news events (positive/negative/neutral)
  - Calculates stock prices based on order flow and news impact
  - Maintains price history and market statistics
- **Key Class**: `Market`

#### `llm_client.py`
- **Purpose**: LLM API client for agent decision-making
- **Functionality**:
  - Integrates with Baidu Wenxin API (qianfan)
  - Provides mock responses when API is unavailable
  - Handles API calls and error management
- **Key Class**: `LLMClient`

#### `config.py`
- **Purpose**: Configuration file for API keys and system parameters
- **Contents**:
  - Baidu Wenxin API credentials
  - Market configuration (initial price, volatility, etc.)
  - Agent configuration (types and names)
- **Note**: Contains default API key, can be modified as needed

### Supporting Files

#### `requirements.txt`
- **Purpose**: Lists all Python package dependencies with version requirements
- **Usage**: `pip install -r requirements.txt`

#### `test_imports.py`
- **Purpose**: Test script to verify all modules can be imported correctly
- **Usage**: `python test_imports.py`
- **Functionality**: Tests imports of all core modules and reports any errors

#### `start_app.bat` (Windows)
- **Purpose**: Quick start script for Windows users
- **Functionality**: Starts the Streamlit application directly

#### `run.bat` (Windows)
- **Purpose**: Installation and start script for Windows
- **Functionality**: Installs dependencies first, then starts the application

### Documentation Files

#### `README.md`
- **Purpose**: This file - project documentation and setup instructions

#### `操作指南.md` (Chinese User Guide)
- **Purpose**: Detailed Chinese user guide with operation instructions
- **Content**: Step-by-step usage guide, experiment suggestions, key concepts

### Generated/System Files

#### `__pycache__/`
- **Purpose**: Python bytecode cache directory (auto-generated)
- **Note**: Can be ignored, regenerated automatically

---

## Project Structure

```
agent_simulator_market/
│
├── app.py                    # Main Streamlit application
├── simulator.py              # Simulation engine
├── agent.py                  # Agent class definition
├── market.py                 # Market environment
├── llm_client.py             # LLM API client
├── config.py                 # Configuration file
│
├── requirements.txt          # Python dependencies
├── test_imports.py           # Import test script
├── start_app.bat             # Windows quick start script
├── run.bat                   # Windows install & start script
│
├── README.md                 # This file (English documentation)
├── 操作指南.md               # Chinese user guide
│
└── __pycache__/              # Python cache (auto-generated)
```

---

## Quick Start Guide

1. **Clone or download the project**
2. **Install Python 3.8+** if not already installed
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application**:
   ```bash
   streamlit run app.py
   ```
5. **Open browser** to `http://localhost:8501`
6. **Click "Execute one step"** in the sidebar to start simulation

---

## Usage

### Starting a Simulation

1. Click **"▶️ Execute one step"** in the sidebar to simulate one time step
2. The system will:
   - Generate a random news event
   - Update all agents' beliefs
   - Form investment intentions
   - Execute trades
   - Update stock price

### Viewing Results

Use the radio buttons at the top to switch between views:

- **📈 Price and Sentiment**: Stock price trends and market sentiment indices
- **💹 Trading Analysis**: Trading volume, type distribution, and trade details
- **👥 Agent States**: Individual agent portfolios, sentiment scores, and opinions
- **📊 Market Statistics**: Price distribution, return analysis, and key metrics

### Resetting Simulation

Click **"🔄 Reset Simulation"** in the sidebar to restart from the beginning.

---

## Core Mechanisms

### Agent Decision Process

1. **Receive News** → Agents get latest market news
2. **Update Beliefs** → LLM analyzes news and updates market outlook
3. **Form Intention** → Decide to buy, sell, or hold
4. **Execute Trade** → Execute trading action based on intention

### Price Calculation

- **Random Walk**: Base market volatility
- **Order Flow Impact**: More buys → price up, more sells → price down
- **News Impact**: Positive news → price up, negative news → price down

### Market Sentiment

- Calculates average sentiment scores across all agents
- Sentiment range: -1 (most pessimistic) to 1 (most optimistic)
- Three sentiment types: optimistic, pessimistic, calm

---

## Troubleshooting

### Application won't start
- Check Python version: `python --version` (should be 3.8+)
- Verify dependencies: `pip list` or run `python test_imports.py`
- Check if port 8501 is available

### No trades appearing
- This is normal for the first few steps
- Agents need to form intentions and have sufficient cash/shares
- Try executing multiple steps

### API errors
- System automatically falls back to mock responses
- To use real API: install `qianfan` and configure credentials in `config.py`

### Browser doesn't open automatically
- Manually navigate to `http://localhost:8501`
- Check terminal output for the exact URL (may use port 8502, 8503, etc.)

---

## Notes

1. **API Calls**: First run may require API configuration. If unavailable, mock responses are used.
2. **Performance**: LLM API calls may take a few seconds, please be patient.
3. **Data Persistence**: Current version doesn't save historical data; refreshing the page resets the simulation.
4. **Mock Mode**: System works fully in mock mode without API access.

---

## License

This project is for educational and research purposes only.

---

## Future Improvements

- [ ] Support for more agent types
- [ ] Real market data calibration
- [ ] Data persistence functionality
- [ ] Custom parameter configuration
- [ ] Additional visualization charts
