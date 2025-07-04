export interface Job {
  id: string
  keyword: string
  location: string
  radius_miles: number
  sources: string[]
  options: JobOptions
  status: JobStatus
  progress: number
  results_count: number
  error_message?: string
  retry_count: number
  started_at?: string
  completed_at?: string
  created_at: string
  updated_at: string
  estimated_completion?: string
}

export interface JobOptions {
  include_emails: boolean
  include_social: boolean
  include_reviews: boolean
  max_results?: number
  min_rating?: number
}

export enum JobStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  PAUSED = 'paused',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled',
}

export interface Business {
  id: string
  name: string
  address?: string
  phone?: string
  email?: string
  website?: string
  rating?: string
  review_count?: number
  data?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface JobResult {
  id: string
  job_id: string
  business_id: string
  source: string
  confidence_score: number
  search_term?: string
  search_position?: string
  created_at: string
  updated_at: string
  business?: Business
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}

export interface JobResultsResponse {
  job: Job
  businesses: Business[]
  total_results: number
  page: number
  size: number
  pages: number
}

export interface CreateJobRequest {
  keyword: string
  location: string
  radius_miles?: number
  sources?: string[]
  options?: Partial<JobOptions>
}

export interface UpdateJobRequest {
  status?: JobStatus
  progress?: number
  results_count?: number
  error_message?: string
}

export interface ExportRequest {
  format: 'csv' | 'json' | 'excel'
  fields?: string[]
  filters?: Record<string, any>
}

export interface ExportResponse {
  download_url: string
  expires_at: string
  file_size: number
  record_count: number
}

export interface ApiError {
  detail: string
  code?: string
}

export interface SuccessResponse {
  message: string
  data?: Record<string, any>
}

// WebSocket message types
export interface WebSocketMessage {
  type: 'job_progress' | 'job_completed' | 'job_failed' | 'result_update'
  data: any
}

export interface JobProgressMessage {
  job_id: string
  progress: number
  status: JobStatus
  message?: string
  results_count?: number
}

// Form types
export interface CreateJobFormData {
  keyword: string
  location: string
  radius_miles: number
  sources: string[]
  include_emails: boolean
  include_social: boolean
  include_reviews: boolean
  max_results?: number
  min_rating?: number
}

// Chart data types
export interface ChartData {
  name: string
  value: number
  color?: string
}

export interface TimeSeriesData {
  timestamp: string
  value: number
  label?: string
}

// Filter types
export interface BusinessFilters {
  search?: string
  has_email?: boolean
  has_website?: boolean
  has_phone?: boolean
  min_rating?: number
  sources?: string[]
}

export interface JobFilters {
  status?: JobStatus[]
  keyword?: string
  location?: string
  date_range?: {
    start: string
    end: string
  }
}
