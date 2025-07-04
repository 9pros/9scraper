import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { Job, JobStatus } from '@/types'

interface JobsState {
  jobs: Job[]
  currentJob: Job | null
  loading: boolean
  error: string | null
  pagination: {
    page: number
    size: number
    total: number
    pages: number
  }
}

const initialState: JobsState = {
  jobs: [],
  currentJob: null,
  loading: false,
  error: null,
  pagination: {
    page: 1,
    size: 20,
    total: 0,
    pages: 0,
  },
}

const jobsSlice = createSlice({
  name: 'jobs',
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload
    },
    setJobs: (state, action: PayloadAction<{ jobs: Job[]; pagination?: Partial<typeof initialState.pagination> }>) => {
      state.jobs = action.payload.jobs
      if (action.payload.pagination) {
        state.pagination = { ...state.pagination, ...action.payload.pagination }
      }
    },
    addJob: (state, action: PayloadAction<Job>) => {
      state.jobs.unshift(action.payload)
      state.pagination.total += 1
    },
    updateJob: (state, action: PayloadAction<Job>) => {
      const index = state.jobs.findIndex(job => job.id === action.payload.id)
      if (index !== -1) {
        state.jobs[index] = action.payload
      }
      if (state.currentJob?.id === action.payload.id) {
        state.currentJob = action.payload
      }
    },
    setCurrentJob: (state, action: PayloadAction<Job | null>) => {
      state.currentJob = action.payload
    },
    updateJobProgress: (state, action: PayloadAction<{ id: string; progress: number; status?: JobStatus }>) => {
      const { id, progress, status } = action.payload
      const job = state.jobs.find(job => job.id === id)
      if (job) {
        job.progress = progress
        if (status) {
          job.status = status
        }
      }
      if (state.currentJob?.id === id) {
        state.currentJob.progress = progress
        if (status) {
          state.currentJob.status = status
        }
      }
    },
    removeJob: (state, action: PayloadAction<string>) => {
      state.jobs = state.jobs.filter(job => job.id !== action.payload)
      if (state.currentJob?.id === action.payload) {
        state.currentJob = null
      }
      state.pagination.total -= 1
    },
    clearJobs: (state) => {
      state.jobs = []
      state.currentJob = null
      state.pagination = initialState.pagination
    },
  },
})

export const {
  setLoading,
  setError,
  setJobs,
  addJob,
  updateJob,
  setCurrentJob,
  updateJobProgress,
  removeJob,
  clearJobs,
} = jobsSlice.actions

export default jobsSlice.reducer
