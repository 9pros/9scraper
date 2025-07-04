import { 
  Job, 
  Business, 
  CreateJobRequest, 
  UpdateJobRequest, 
  PaginatedResponse, 
  JobResultsResponse,
  ExportRequest,
  ExportResponse,
  SuccessResponse 
} from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

class ApiError extends Error {
  constructor(public status: number, message: string, public code?: string) {
    super(message)
    this.name = 'ApiError'
  }
}

class ApiClient {
  private baseURL: string

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
  }

  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        let errorMessage = `HTTP ${response.status}`
        let errorCode: string | undefined
        
        try {
          const errorData = await response.json()
          errorMessage = errorData.detail || errorMessage
          errorCode = errorData.code
        } catch {
          // If JSON parsing fails, use the status text
          errorMessage = response.statusText || errorMessage
        }
        
        throw new ApiError(response.status, errorMessage, errorCode)
      }

      const contentType = response.headers.get('Content-Type')
      if (contentType && contentType.includes('application/json')) {
        return await response.json()
      }
      
      return response as unknown as T
    } catch (error) {
      if (error instanceof ApiError) {
        throw error
      }
      
      // Network or other errors
      throw new ApiError(0, error instanceof Error ? error.message : 'Network error')
    }
  }

  // Job endpoints
  async createJob(jobData: CreateJobRequest): Promise<Job> {
    return this.request<Job>('/jobs/', {
      method: 'POST',
      body: JSON.stringify(jobData),
    })
  }

  async getJobs(params: {
    page?: number
    size?: number
    status?: string
  } = {}): Promise<PaginatedResponse<Job>> {
    const searchParams = new URLSearchParams()
    
    if (params.page) searchParams.append('page', params.page.toString())
    if (params.size) searchParams.append('size', params.size.toString())
    if (params.status) searchParams.append('status', params.status)
    
    const query = searchParams.toString()
    const endpoint = query ? `/jobs/?${query}` : '/jobs/'
    
    return this.request<PaginatedResponse<Job>>(endpoint)
  }

  async getJob(jobId: string): Promise<Job> {
    return this.request<Job>(`/jobs/${jobId}`)
  }

  async updateJob(jobId: string, updates: UpdateJobRequest): Promise<Job> {
    return this.request<Job>(`/jobs/${jobId}`, {
      method: 'PATCH',
      body: JSON.stringify(updates),
    })
  }

  async cancelJob(jobId: string): Promise<SuccessResponse> {
    return this.request<SuccessResponse>(`/jobs/${jobId}`, {
      method: 'DELETE',
    })
  }

  async restartJob(jobId: string): Promise<Job> {
    return this.request<Job>(`/jobs/${jobId}/restart`, {
      method: 'POST',
    })
  }

  async getJobResults(
    jobId: string, 
    params: { page?: number; size?: number } = {}
  ): Promise<JobResultsResponse> {
    const searchParams = new URLSearchParams()
    
    if (params.page) searchParams.append('page', params.page.toString())
    if (params.size) searchParams.append('size', params.size.toString())
    
    const query = searchParams.toString()
    const endpoint = query ? `/jobs/${jobId}/results?${query}` : `/jobs/${jobId}/results`
    
    return this.request<JobResultsResponse>(endpoint)
  }

  // Export endpoints
  async exportJobResults(
    jobId: string, 
    exportData: ExportRequest
  ): Promise<ExportResponse> {
    return this.request<ExportResponse>(`/exports/${jobId}`, {
      method: 'POST',
      body: JSON.stringify(exportData),
    })
  }

  // Health check
  async healthCheck(): Promise<{ status: string; version: string }> {
    return this.request<{ status: string; version: string }>('/health')
  }
}

// Create singleton instance
export const apiClient = new ApiClient()
export { ApiError }
