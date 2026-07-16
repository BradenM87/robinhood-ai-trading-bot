# Claude AI Integration Guide

This guide explains how to set up and use the Claude AI integration with the Robinhood trading bot.

## Overview

This fork of the robinhood-ai-trading-bot integrates **Anthropic's Claude API** as an alternative to OpenAI's GPT. Claude can be used for all trading decision-making while maintaining the same robust trading infrastructure (PDT protection, demo mode, etc.).

## What's New

### New Files Created:
- **`src/api/claude.py`** - Claude API client and response parsing

### Modified Files:
- **`config.py.example`** - Added Claude configuration options
- **`requirements.txt`** - Added Anthropic SDK
- **`main.py`** - Added Claude integration with fallback to OpenAI

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/BradenM87/robinhood-ai-trading-bot.git
cd robinhood-ai-trading-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Claude API

Copy the example config and update it:

```bash
cp config.py.example config.py
```

Edit `config.py` and add your Claude API key:

```python
# AI Model Selection
USE_CLAUDE = True                           # Set to True to use Claude
CLAUDE_API_KEY = "sk-ant-..."               # Your Anthropic Claude API key
CLAUDE_MODEL_NAME = "claude-3-5-sonnet-20241022"  # Claude model to use
```

### 4. Add Robinhood Credentials

In the same `config.py`, add your Robinhood credentials:

```python
# Credentials
ROBINHOOD_USERNAME = "your_username@example.com"
ROBINHOOD_PASSWORD = "your_password"
ROBINHOOD_MFA_SECRET = ""  # Optional if MFA is enabled
```

### 5. (Optional) Configure 1Password for MFA

If you want to use 1Password for secure MFA storage:

```python
# 1Password Credentials
OP_SERVICE_ACCOUNT_NAME = "your_service_account_name"
OP_SERVICE_ACCOUNT_TOKEN = "your_token"
OP_VAULT_NAME = "your_vault"
OP_ITEM_NAME = "robinhood"
```

## Configuration Options

### AI Model Selection

**Use Claude (Recommended):**
```python
USE_CLAUDE = True
CLAUDE_API_KEY = "sk-ant-..."
CLAUDE_MODEL_NAME = "claude-3-5-sonnet-20241022"
```

**Use OpenAI (Legacy):**
```python
USE_CLAUDE = False
OPENAI_API_KEY = "sk-..."
OPENAI_MODEL_NAME = "gpt-4o-mini"
```

### Trading Modes

```python
MODE = "demo"      # demo, manual, or auto
```

- **demo**: Simulates trades without executing
- **manual**: Requires user confirmation before each trade
- **auto**: Executes trades automatically

### Trading Parameters

```python
LOG_LEVEL = "INFO"              # DEBUG, INFO, WARNING, ERROR
RUN_INTERVAL_SECONDS = 600      # How often to analyze (in seconds)
PORTFOLIO_LIMIT = 10            # Max stocks to hold
WATCHLIST_OVERVIEW_LIMIT = 10   # Max watchlist stocks to analyze
TRADE_EXCEPTIONS = ["AAPL"]     # Stocks to never trade
MIN_BUYING_AMOUNT_USD = 1.0     # Minimum buy order size
MAX_BUYING_AMOUNT_USD = 10.0    # Maximum buy order size
MIN_SELLING_AMOUNT_USD = 1.0    # Minimum sell order size
MAX_SELLING_AMOUNT_USD = 10.0   # Maximum sell order size
```

## Running the Bot

### Start in Demo Mode (Recommended for Testing)

```bash
python main.py
```

The bot will:
1. Ask for confirmation to run in demo mode
2. Connect to Robinhood
3. Fetch your portfolio and watchlist
4. Analyze stocks using Claude AI
5. Simulate trades (no real money is spent)
6. Continue monitoring every 10 minutes (configurable)

### Sample Output

```
Are you sure you want to run the bot in demo mode? (yes/no): yes
[2024-11-01 11:06:58] [INFO]    Market is open, running trading bot in demo mode...
[2024-11-01 11:06:58] [INFO]    Getting account info...
[2024-11-01 11:07:02] [INFO]    Getting portfolio stocks...
[2024-11-01 11:07:02] [INFO]    Portfolio stocks to proceed: NVDA (1.07%), MSFT (0.12%)
[2024-11-01 11:07:02] [INFO]    Using Claude AI for trading decisions...
[2024-11-01 11:07:15] [INFO]    Executing decisions...
[2024-11-01 11:07:15] [INFO]    NVDA > Decision: sell of 2.012
[2024-11-01 11:07:15] [INFO]    NVDA > Demo > Sold 2.012 stocks
[2024-11-01 11:07:16] [INFO]    Waiting for 600 seconds...
```

## How Claude Makes Trading Decisions

Claude analyzes the following for each stock:

1. **RSI (Relative Strength Index)** - Momentum indicator (0-100 scale)
   - Above 70: Overbought (sell signal)
   - Below 30: Oversold (buy signal)

2. **VWAP (Volume-Weighted Average Price)** - Fair value indicator
   - Above VWAP: Potentially overvalued (sell signal)
   - Below VWAP: Potentially undervalued (buy signal)

3. **Moving Averages** - Trend indicators
   - 50-day vs 200-day moving averages
   - Golden Cross (bullish), Death Cross (bearish)

4. **Analyst Ratings** - Expert consensus
   - Buy, hold, and sell recommendations aggregated

5. **PDT Restrictions** - Pattern Day Trading protection
   - Prevents day trading violations automatically

## Claude API Costs

Claude 3.5 Sonnet pricing (as of 2024):
- **Input**: $3 per million tokens
- **Output**: $15 per million tokens

Typical trading analysis: ~2,000-5,000 tokens per decision
Expected cost: **$0.01-$0.05 per trading analysis**

## Switching Between Claude and OpenAI

To quickly switch AI providers, just update `config.py`:

```python
# Use Claude
USE_CLAUDE = True

# Or use OpenAI
USE_CLAUDE = False
```

No code changes needed!

## Troubleshooting

### "Invalid API key provided"
- Verify your `CLAUDE_API_KEY` is correct
- Ensure it starts with `sk-ant-`
- Check it has access to claude-3-5-sonnet model

### "No stocks to analyze"
- Ensure you have stocks in your Robinhood portfolio or watchlist
- Check that `WATCHLIST_NAMES` is properly configured

### "Market is closed"
- The bot only runs during market hours (9:30 AM - 4:00 PM ET)
- Check your timezone settings

### Authentication errors
- Verify Robinhood credentials in `config.py`
- Check if 2FA is enabled on your account
- Ensure MFA secret is correct if using 1Password

## Safety Features

✅ **PDT Protection** - Prevents day trading violations  
✅ **Demo Mode** - Test without real money  
✅ **Manual Mode** - Require approval for each trade  
✅ **Trade Exceptions** - Exclude specific stocks  
✅ **Amount Limits** - Set min/max buy/sell amounts  
✅ **Portfolio Limits** - Cap max holdings  
✅ **Comprehensive Logging** - Track all decisions  

## Disclaimer

⚠️ **This bot is for educational purposes only.**

Trading stocks involves significant financial risk. You should only invest money you can afford to lose. The authors are not responsible for any financial losses incurred through the use of this bot.

**Always:**
- Start in demo mode
- Test thoroughly before enabling auto mode
- Monitor logs regularly
- Keep your API keys secure
- Review all trades before they execute

## Support & Contribution

For issues, questions, or improvements:
- Open a GitHub issue
- Submit a pull request
- Contact: goodbotty@proton.me

## License

MIT License - See LICENSE file for details

## Resources

- [Anthropic Claude API Docs](https://docs.anthropic.com)
- [Robinhood Python Documentation](https://github.com/jmfernandes/robin_stocks)
- [Technical Analysis Indicators](https://www.investopedia.com/terms/t/technicalanalysis.asp)

---

**Happy trading! 🚀**
