# Setup Guide: Getting Free AI APIs

This guide helps you quickly set up free or affordable AI API keys to run the Autonomous Paper Analyzer.

## 5-Minute Setup (Free Tier Only)

### 1. Groq (Fastest, Completely Free)
```bash
1. Visit https://console.groq.com/keys
2. Sign up (GitHub or Email)
3. Click "Create API Key"
4. Copy the key
```
**Add to `.env`:**
```
GROQ_API_KEY=your-key-here
```

### 2. Google Gemini (Free Tier)
```bash
1. Visit https://aistudio.google.com/apikey
2. Click "Create API Key in new project"
3. Copy the key
```
**Add to `.env`:**
```
GOOGLE_API_KEY=your-key-here
```

**Done!** You now have 2 free providers. Test with:
```bash
curl http://localhost:8001/api/providers
```

---

## Complete Setup (Free + Premium)

### Add OpenRouter (100+ Models)
```bash
1. Visit https://openrouter.ai/keys
2. Sign up with GitHub or Email
3. Create API Key
4. Add to `.env`:
   OPENROUTER_API_KEY=your-key-here
```

### Add OpenAI (Optional, Paid)
```bash
1. Visit https://platform.openai.com/api/keys
2. Sign up with email
3. Add payment method
4. Create API Key
5. Add to `.env`:
   OPENAI_API_KEY=sk-...
```

### Add Anthropic Claude (Optional, Paid)
```bash
1. Visit https://console.anthropic.com
2. Sign up with email
3. Add payment method
4. Create API Key
5. Add to `.env`:
   ANTHROPIC_API_KEY=sk-ant-...
```

### Add NVIDIA NIM (Free Tier)
```bash
1. Visit https://build.nvidia.com
2. Sign up with email
3. Navigate to API Keys
4. Create API Key
5. Add to `.env`:
   NVIDIA_API_KEY=your-key-here
```

---

## Environment File Setup

Create `.env` file in project root:

```bash
cp .env.example .env
```

Then edit `.env` and add your keys:

```
# Database (optional - uses SQLite by default)
DATABASE_URL=postgresql://localhost:5432/paper_analyzer

# Free providers
GROQ_API_KEY=your-groq-key
GOOGLE_API_KEY=your-google-key
OPENROUTER_API_KEY=your-openrouter-key
NVIDIA_API_KEY=your-nvidia-key

# Premium providers (optional)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
MISTRAL_API_KEY=your-mistral-key
```

---

## Test Your Setup

1. **Start the server:**
   ```bash
   python run.py
   ```

2. **List available providers:**
   ```bash
   curl http://localhost:8001/api/providers
   ```

3. **Test a chat:**
   ```bash
   curl -X POST http://localhost:8001/api/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
       "model": "groq:llama-3.1-70b-versatile",
       "messages": [
         {"role": "user", "content": "What is AI?"}
       ]
     }'
   ```

---

## FAQ

### Can I use completely free?
**Yes!** Groq and Google Gemini free tiers are sufficient for development and light usage.

### What are the free tier limits?
| Provider | Limit | Reset |
|----------|-------|-------|
| Groq | ~30-100 req/min | Daily |
| Google | 60 req/min | Daily |
| OpenRouter | Varies | - |
| NVIDIA | Varies | - |

### Which is fastest?
**Groq** - Often 500+ tokens/second on free tier.

### Which has best quality?
**OpenAI GPT-4o** (paid) or **Claude 3.5** (paid). For free: **Groq Llama 3.1 70B**.

### What if I exceed free limits?
1. Add a paid provider as backup
2. Implement caching
3. Use cheaper models for simple tasks
4. Upgrade to paid tier

### Can I use multiple providers?
**Yes!** The system automatically uses any configured provider. You can:
- Use free tier for development
- Switch to paid for production
- Add multiple providers for fallback

### Do I need all providers?
**No.** Start with just Groq or Google. Add others as needed.

---

## Cost Estimation

| Use Case | Setup | Monthly Cost |
|----------|-------|-------------|
| Personal research | Groq only | $0 |
| Development | Groq + Google | $0-15 |
| Production (small) | Groq + OpenAI | $20-50 |
| Production (large) | Multiple paid | $100+ |

---

## Troubleshooting

### "Provider not found"
- Check API key is in `.env`
- Restart server: `python run.py`
- Verify key format (no extra spaces)

### "Rate limit exceeded"
- Add another free provider
- Implement caching
- Upgrade to paid tier

### "Invalid API key"
- Double-check key spelling
- Re-generate key on provider dashboard
- Check key hasn't been revoked

### "Connection refused"
- Ensure server is running: `python run.py`
- Check port 8001 is available

---

## Next Steps

1. ✅ Set up at least one free API
2. ✅ Test with `curl` commands above
3. ✅ Start using the web interface at http://localhost:5173
4. ✅ Add more providers as needed
5. ✅ See [PROVIDERS.md](../docs/PROVIDERS.md) for advanced setup

---

## Support

- **Groq Docs**: https://console.groq.com/docs
- **Google Docs**: https://ai.google.dev/docs
- **OpenRouter Docs**: https://openrouter.ai/docs
- **OpenAI Docs**: https://platform.openai.com/docs
- **Anthropic Docs**: https://docs.anthropic.com
- **NVIDIA Docs**: https://docs.nvidia.com/nim
