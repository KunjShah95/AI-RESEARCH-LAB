import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Bot, ChevronDown, Loader2, Settings, Check } from 'lucide-react'
import { modelsApi } from '../services/api'

const mockProviders = {
  openai: {
    name: 'OpenAI',
    models: ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo', 'o1', 'o1-mini'],
  },
  anthropic: {
    name: 'Anthropic',
    models: ['claude-3-5-sonnet-20241022', 'claude-3-opus-20240229', 'claude-3-haiku-20240307'],
  },
  google: {
    name: 'Google',
    models: ['gemini-2.0-flash-exp', 'gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.5-flash-8b'],
  },
  groq: {
    name: 'Groq',
    models: ['llama-3.3-70b-versatile', 'llama-3.1-70b-versatile', 'mixtral-8x7b-32768'],
  },
  mistral: {
    name: 'Mistral',
    models: ['mistral-large-latest', 'mistral-small-latest', 'codestral-latest'],
  },
  nvidia: {
    name: 'NVIDIA',
    models: ['nvidia/llama-3.1-nemotron-70b-instruct', 'nvidia/phi-3.5-mini-instruct'],
  },
  openrouter: {
    name: 'OpenRouter',
    models: ['openai/gpt-4o', 'anthropic/claude-3.5-sonnet', 'google/gemini-pro-1.5'],
  },
}

export default function ModelSelector({ onModelChange, defaultProvider = 'openai', defaultModel = 'gpt-4o' }) {
  const [providers, setProviders] = useState({})
  const [loading, setLoading] = useState(true)
  const [selectedProvider, setSelectedProvider] = useState(defaultProvider)
  const [selectedModel, setSelectedModel] = useState(defaultModel)
  const [isOpen, setIsOpen] = useState(false)
  const [showSettings, setShowSettings] = useState(false)

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const response = await modelsApi.getAvailableModels()
        if (response && Object.keys(response).length > 0) {
          setProviders(response)
        } else {
          setProviders(mockProviders)
        }
      } catch (error) {
        console.log('Using mock providers - API not available')
        setProviders(mockProviders)
      } finally {
        setLoading(false)
      }
    }
    fetchModels()
  }, [])

  useEffect(() => {
    if (onModelChange) {
      onModelChange({
        provider: selectedProvider,
        model: selectedModel,
      })
    }
  }, [selectedProvider, selectedModel, onModelChange])

  const currentProvider = providers[selectedProvider]
  const currentModels = currentProvider?.models || []

  const handleProviderChange = (provider) => {
    setSelectedProvider(provider)
    const providerData = providers[provider]
    if (providerData?.models?.length > 0) {
      setSelectedModel(providerData.models[0])
    }
  }

  return (
    <div className="model-selector">
      <div className="model-selector-label">
        <Bot size={16} />
        <span>AI Model</span>
      </div>

      <div className="model-selector-controls">
        <div className="provider-selector">
          <select
            value={selectedProvider}
            onChange={(e) => handleProviderChange(e.target.value)}
            className="model-select"
          >
            {Object.entries(providers).map(([key, value]) => (
              <option key={key} value={key}>
                {value.name || key}
              </option>
            ))}
          </select>
        </div>

        <div className="model-dropdown">
          <button 
            className="model-dropdown-trigger"
            onClick={() => setIsOpen(!isOpen)}
          >
            <span>{selectedModel}</span>
            <ChevronDown size={16} className={isOpen ? 'rotate' : ''} />
          </button>

          <AnimatePresence>
            {isOpen && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="model-dropdown-menu"
              >
                {currentModels.map((model) => (
                  <button
                    key={model}
                    className={`model-option ${selectedModel === model ? 'active' : ''}`}
                    onClick={() => {
                      setSelectedModel(model)
                      setIsOpen(false)
                    }}
                  >
                    <span className="model-name">{model}</span>
                    {selectedModel === model && <Check size={14} />}
                  </button>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        <button 
          className="model-settings-btn"
          onClick={() => setShowSettings(!showSettings)}
          title="Model Settings"
        >
          <Settings size={16} />
        </button>
      </div>

      <AnimatePresence>
        {showSettings && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="model-settings-panel"
          >
            <div className="settings-group">
              <label>Temperature</label>
              <input type="range" min="0" max="1" step="0.1" defaultValue="0.7" />
              <span className="settings-value">0.7</span>
            </div>
            <div className="settings-group">
              <label>Max Tokens</label>
              <input type="number" defaultValue="4096" min="100" max="128000" />
            </div>
            <div className="settings-group">
              <label className="checkbox-label">
                <input type="checkbox" defaultChecked />
                Streaming Response
              </label>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {loading && (
        <div className="model-loading">
          <Loader2 className="spinner" size={16} />
          <span>Loading models...</span>
        </div>
      )}
    </div>
  )
}

export function ModelBadge({ provider, model }) {
  const providerColors = {
    openai: '#10a37f',
    anthropic: '#d97757',
    google: '#4285f4',
    groq: '#ff4d4d',
    mistral: '#ff7000',
    nvidia: '#76b900',
    openrouter: '#000000',
  }

  return (
    <div 
      className="model-badge" 
      style={{ '--provider-color': providerColors[provider] || '#666' }}
    >
      <Bot size={12} />
      <span className="provider-name">{provider}</span>
      <span className="model-name">{model}</span>
    </div>
  )
}