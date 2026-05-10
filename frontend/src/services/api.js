const API_BASE = import.meta.env.VITE_API_URL || '';

class ApiService {
  constructor() {
    this.baseUrl = API_BASE;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    if (options.body && typeof options.body === 'object') {
      config.body = JSON.stringify(options.body);
    }

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${endpoint}?${queryString}` : endpoint;
    return this.request(url, { method: 'GET' });
  }

  post(endpoint, body) {
    return this.request(endpoint, { method: 'POST', body });
  }

  put(endpoint, body) {
    return this.request(endpoint, { method: 'PUT', body });
  }

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

export const api = new ApiService();

export const papersApi = {
  search: (query, filters = {}) => 
    api.post('/papers/search', { query, max_results: filters.max_results || 10, ...filters }),
  
  getPaper: (id, source = 'arxiv') => 
    api.get(`/papers/${id}`, { source }),
  
  summarize: (paperId, source = 'arxiv') => 
    api.post('/papers/summarize', { paper_id: paperId, source }),
  
  export: (paperIds, format) => 
    api.post(`/papers/export/${format}`, { paper_ids: paperIds }),
};

export const compareApi = {
  compare: (paperIds, source = 'arxiv') => 
    api.post('/compare', { paper_ids: paperIds, source }),
};

export const debateApi = {
  start: (thesis, papers = []) => 
    api.post('/debate/start', { thesis, papers }),
  get: (id) => 
    api.get(`/debate/${id}`),
};

export const synthesizeApi = {
  synthesize: (query, papers = []) => 
    api.post('/synthesize', { query, papers }),
};

export const writeApi = {
  generate: (topic, paperType, selectedPapers = []) => 
    api.post('/write', { topic, paper_type: paperType, papers: selectedPapers }),
};

export const projectsApi = {
  list: () => api.get('/projects/'),
  create: (data) => api.post('/projects/', data),
  get: (id) => api.get(`/projects/${id}`),
  update: (id, data) => api.put(`/projects/${id}`, data),
  delete: (id) => api.delete(`/projects/${id}`),
  getPapers: (id) => api.get(`/projects/${id}/papers`),
  addPaper: (projectId, paperId) => api.post(`/projects/${projectId}/papers`, { paper_id: paperId }),
  removePaper: (projectId, paperId) => api.delete(`/projects/${projectId}/papers/${paperId}`),
};

export const collectionsApi = {
  list: () => api.get('/collections/'),
  create: (data) => api.post('/collections/', data),
  get: (id) => api.get(`/collections/${id}`),
  update: (id, data) => api.put(`/collections/${id}`, data),
  delete: (id) => api.delete(`/collections/${id}`),
};

export const clipboardApi = {
  getAll: () => api.get('/clipboard/'),
  add: (paperId, citation) => api.post('/clipboard/', { paper_id: paperId, citation }),
  remove: (id) => api.delete(`/clipboard/${id}`),
  clear: () => api.post('/clipboard/clear'),
};

export const exportApi = {
  bibtex: (paperIds) => api.post('/papers/export/bibtex', { paper_ids: paperIds }),
  ris: (paperIds) => api.post('/papers/export/ris', { paper_ids: paperIds }),
  json: (paperIds) => api.post('/papers/export/json', { paper_ids: paperIds }),
  csv: (paperIds) => api.post('/papers/export/csv', { paper_ids: paperIds }),
};

export const authApi = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (email, password, name) => api.post('/auth/register', { email, password, name }),
  me: () => api.get('/auth/me'),
  logout: () => api.post('/auth/logout'),
};

export const advancedSearchApi = {
  search: (query, searchType = 'hybrid', filters = {}) => 
    api.post('/search/advanced', { query, search_type: searchType, ...filters }),
  suggestions: (query) => 
    api.get('/search/advanced/suggestions', { query }),
};

export const graphApi = {
  buildGraph: (papers) => 
    api.post('/api/graph/build', { papers }),
  
  getMetrics: () => 
    api.get('/api/graph/metrics'),
  
  getInfluential: (metric = 'pagerank', topK = 10) => 
    api.get('/api/graph/influential', { metric, top_k: topK }),
  
  getSubgraph: (paperIds, includeReferences = 1) => 
    api.post('/api/graph/subgraph', { paper_ids: paperIds, include_references: includeReferences }),
  
  getPageRank: () => 
    api.get('/api/graph/pagerank'),
  
  getCycles: (maxLength = 6) => 
    api.get('/api/graph/cycles', { max_length: maxLength }),
  
  getTrends: (paperId) => 
    api.get(`/api/graph/trends/${paperId}`),
  
  getImpact: (paperId, year = null) => 
    api.get(`/api/graph/impact/${paperId}`, { year }),
  
  getNeighbors: (paperId, depth = 1, direction = 'both') => 
    api.get(`/api/graph/neighbors/${paperId}`, { depth, direction }),
  
  getRecommendations: (paperId, topK = 10, method = 'combined') => 
    api.get(`/api/graph/recommendations/${paperId}`, { top_k: topK, method }),
  
  getAnalysis: (paperId) => 
    api.get(`/api/graph/analysis/${paperId}`),
  
  getD3Visualization: (paperIds = null, includeNeighbors = 1) => 
    api.get('/api/graph/visualization/d3', { paper_ids: paperIds, include_neighbors: includeNeighbors }),
  
  getBridges: (topK = 10) => 
    api.get('/api/graph/bridges', { top_k: topK }),
  
  exportGraph: () => 
    api.get('/api/graph/export'),
  
  resetGraph: () => 
    api.post('/api/graph/reset'),
};

export const modelsApi = {
  getAvailableModels: () => 
    api.get('/api/models'),
};

export default api;