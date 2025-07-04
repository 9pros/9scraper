import { Link } from 'react-router-dom'
import { Job, JobStatus } from '@/types'
import { format } from 'date-fns'
import { EyeIcon } from '@heroicons/react/24/outline'
import clsx from 'clsx'

interface RecentJobsProps {
  jobs: Job[]
  isLoading: boolean
}

const RecentJobs = ({ jobs, isLoading }: RecentJobsProps) => {
  if (isLoading) {
    return (
      <div className="space-y-3 p-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="flex items-center space-x-3">
              <div className="w-3 h-3 bg-secondary-200 rounded-full" />
              <div className="flex-1">
                <div className="h-4 bg-secondary-200 rounded w-3/4 mb-1" />
                <div className="h-3 bg-secondary-200 rounded w-1/2" />
              </div>
              <div className="w-16 h-6 bg-secondary-200 rounded" />
            </div>
          </div>
        ))}
      </div>
    )
  }

  if (jobs.length === 0) {
    return (
      <div className="text-center py-8 px-4">
        <p className="text-secondary-500">No jobs yet</p>
      </div>
    )
  }

  return (
    <div className="divide-y divide-secondary-200">
      {jobs.map((job) => (
        <div key={job.id} className="flex items-center justify-between p-4 hover:bg-secondary-50 transition-colors">
          <div className="flex items-center space-x-3 flex-1 min-w-0">
            {/* Status indicator */}
            <div className={clsx('w-3 h-3 rounded-full', {
              'bg-warning-400': job.status === JobStatus.PENDING,
              'bg-primary-500 animate-pulse': job.status === JobStatus.RUNNING,
              'bg-success-500': job.status === JobStatus.COMPLETED,
              'bg-error-500': job.status === JobStatus.FAILED,
              'bg-secondary-400': job.status === JobStatus.CANCELLED,
            })} />
            
            {/* Job info */}
            <div className="flex-1 min-w-0">
              <Link 
                to={`/jobs/${job.id}`}
                className="font-medium text-secondary-900 hover:text-primary-600 transition-colors truncate block"
              >
                {job.keyword}
              </Link>
              <div className="flex items-center space-x-2 text-sm text-secondary-500">
                <span className="truncate">{job.location}</span>
                <span>•</span>
                <span>{format(new Date(job.created_at), 'MMM d')}</span>
                {job.results_count > 0 && (
                  <>
                    <span>•</span>
                    <span>{job.results_count} results</span>
                  </>
                )}
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center space-x-2 ml-4">
            <span className={clsx('status-badge text-xs', {
              'status-pending': job.status === JobStatus.PENDING,
              'status-running': job.status === JobStatus.RUNNING,
              'status-completed': job.status === JobStatus.COMPLETED,
              'status-failed': job.status === JobStatus.FAILED,
              'status-cancelled': job.status === JobStatus.CANCELLED,
            })}>
              {job.status}
            </span>
            
            <Link
              to={`/jobs/${job.id}`}
              className="p-1 text-secondary-400 hover:text-secondary-600 transition-colors"
            >
              <EyeIcon className="w-4 h-4" />
            </Link>
          </div>
        </div>
      ))}
    </div>
  )
}

export default RecentJobs
