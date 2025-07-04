import { Link } from 'react-router-dom'
import { Job, JobStatus } from '@/types'
import { 
  PlayIcon, 
  PauseIcon, 
  StopIcon,
  ClockIcon,
  ExclamationTriangleIcon 
} from '@heroicons/react/24/outline'
import { format } from 'date-fns'
import clsx from 'clsx'

interface JobProgressProps {
  job: Job
  showActions?: boolean
}

const JobProgress = ({ job, showActions = true }: JobProgressProps) => {
  const getStatusColor = (status: JobStatus) => {
    switch (status) {
      case JobStatus.RUNNING:
        return 'text-primary-600'
      case JobStatus.COMPLETED:
        return 'text-success-600'
      case JobStatus.FAILED:
        return 'text-error-600'
      case JobStatus.CANCELLED:
        return 'text-secondary-600'
      case JobStatus.PENDING:
        return 'text-warning-600'
      default:
        return 'text-secondary-600'
    }
  }

  const getProgressColor = (status: JobStatus) => {
    switch (status) {
      case JobStatus.RUNNING:
        return 'from-primary-500 to-primary-600'
      case JobStatus.COMPLETED:
        return 'from-success-500 to-success-600'
      case JobStatus.FAILED:
        return 'from-error-500 to-error-600'
      default:
        return 'from-secondary-400 to-secondary-500'
    }
  }

  const formatDuration = (startedAt?: string) => {
    if (!startedAt) return null
    const start = new Date(startedAt)
    const now = new Date()
    const diff = now.getTime() - start.getTime()
    const minutes = Math.floor(diff / 60000)
    const seconds = Math.floor((diff % 60000) / 1000)
    
    if (minutes > 0) {
      return `${minutes}m ${seconds}s`
    }
    return `${seconds}s`
  }

  return (
    <div className="bg-white border border-secondary-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-3">
        <div className="flex-1 min-w-0">
          <Link 
            to={`/jobs/${job.id}`}
            className="text-lg font-semibold text-secondary-900 hover:text-primary-600 transition-colors truncate block"
          >
            {job.keyword}
          </Link>
          <p className="text-sm text-secondary-600 truncate">
            {job.location} • {job.radius_miles} miles
          </p>
        </div>
        
        <div className="flex items-center space-x-2 ml-4">
          <span className={clsx('status-badge', {
            'status-pending': job.status === JobStatus.PENDING,
            'status-running': job.status === JobStatus.RUNNING,
            'status-completed': job.status === JobStatus.COMPLETED,
            'status-failed': job.status === JobStatus.FAILED,
            'status-cancelled': job.status === JobStatus.CANCELLED,
          })}>
            {job.status}
          </span>
          
          {job.status === JobStatus.RUNNING && (
            <div className="loading-spinner" />
          )}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-3">
        <div className="flex items-center justify-between text-sm text-secondary-600 mb-2">
          <span>Progress: {job.progress}%</span>
          <span>{job.results_count} results found</span>
        </div>
        
        <div className="progress-bar">
          <div 
            className={clsx('progress-fill bg-gradient-to-r', getProgressColor(job.status))}
            style={{ width: `${job.progress}%` }}
          />
        </div>
      </div>

      {/* Job Details */}
      <div className="flex items-center justify-between text-sm text-secondary-500">
        <div className="flex items-center space-x-4">
          <span className="flex items-center">
            <ClockIcon className="w-4 h-4 mr-1" />
            {job.started_at ? formatDuration(job.started_at) : 'Not started'}
          </span>
          
          <span>
            Sources: {job.sources.join(', ')}
          </span>
        </div>

        {showActions && (
          <div className="flex items-center space-x-2">
            {job.status === JobStatus.RUNNING && (
              <>
                <button className="btn-sm btn-secondary">
                  <PauseIcon className="w-4 h-4" />
                </button>
                <button className="btn-sm btn-danger">
                  <StopIcon className="w-4 h-4" />
                </button>
              </>
            )}
            
            {job.status === JobStatus.FAILED && (
              <button className="btn-sm btn-primary">
                <PlayIcon className="w-4 h-4 mr-1" />
                Retry
              </button>
            )}
          </div>
        )}
      </div>

      {/* Error Message */}
      {job.error_message && (
        <div className="mt-3 p-3 bg-error-50 border border-error-200 rounded-lg">
          <div className="flex items-start">
            <ExclamationTriangleIcon className="w-5 h-5 text-error-500 mr-2 mt-0.5 flex-shrink-0" />
            <p className="text-sm text-error-700">{job.error_message}</p>
          </div>
        </div>
      )}

      {/* Timing Info */}
      <div className="mt-3 pt-3 border-t border-secondary-200 text-xs text-secondary-400">
        Created {format(new Date(job.created_at), 'MMM d, yyyy HH:mm')}
        {job.completed_at && (
          <> • Completed {format(new Date(job.completed_at), 'MMM d, yyyy HH:mm')}</>
        )}
      </div>
    </div>
  )
}

export default JobProgress
