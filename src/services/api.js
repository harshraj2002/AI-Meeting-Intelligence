const API_BASE_URL = 'http://localhost:8000';

class ApiService {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    if (config.body && config.headers['Content-Type'] === 'application/json') {
      config.body = JSON.stringify(config.body);
    }

    const response = await fetch(url, config);
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'Request failed' }));
      throw new Error(error.detail || error.message || `HTTP ${response.status}`);
    }

    return response.json();
  }

  async uploadMeeting(file) {
    const formData = new FormData();
    formData.append('file', file);

    return this.request('/upload-meeting', {
      method: 'POST',
      headers: {}, // Let browser set Content-Type for FormData
      body: formData,
    });
  }

  async getMeetings() {
    return this.request('/meetings');
  }

  async getMeeting(meetingId) {
    return this.request(`/meetings/${meetingId}`);
  }

  async searchMeetings(query) {
    return this.request(`/search?q=${encodeURIComponent(query)}`);
  }
}

const apiService = new ApiService();

export const uploadMeeting = (file) => apiService.uploadMeeting(file);
export const getMeetings = () => apiService.getMeetings();
export const getMeeting = (id) => apiService.getMeeting(id);
export const searchMeetings = (query) => apiService.searchMeetings(query);