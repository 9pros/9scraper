import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { useAppDispatch } from '@/store'
import { setCurrentPage } from '@/store/slices/uiSlice'
import { apiClient } from '@/services/api'
import { Job, JobStatus } from '@/types'
import {
  PlusIcon,
  DocumentTextIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline'

import StatCard from '@/components/StatCard'
import JobProgress from '@/components/JobProgress'
import RecentJobs from '@/components/RecentJobs'
import QuickActions from '@/components/QuickActions'

const Dashboard = () => {
  const dispatch = useAppDispatch()

  useEffect(() => {
    dispatch(setCurrentPage('dashboard'))
  }, [dispatch])

  // Fetch recent jobs
  const { data: jobsData, isLoading } = useQuery({
    queryKey: ['jobs', 'recent'],
    queryFn: () => apiClient.getJobs({ page: 1, size: 10 }),
    refetchInterval: 30000, // Refetch every 30 seconds
  })

  const jobs = jobsData?.items || []

  // Calculate statistics
  const stats = {
    total: jobs.length,
    running: jobs.filter(job => job.status === JobStatus.RUNNING).length,
    completed: jobs.filter(job => job.status === JobStatus.COMPLETED).length,
    failed: jobs.filter(job => job.status === JobStatus.FAILED).length,
  }

  const runningJobs = jobs.filter(job => 
    job.status === JobStatus.RUNNING || job.status === JobStatus.PENDING
  )

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">Dashboard</h1>
          <p className="text-secondary-600 mt-1">
            Monitor your scraping jobs and business data extraction
          </p>
        </div>
        
        <Link to="/jobs/new" className="btn-primary btn-lg glow-on-hover">
          <PlusIcon className="w-5 h-5 mr-2" />
          Create New Job
        </Link>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Jobs"
          value={stats.total}
          icon={DocumentTextIcon}
          color="primary"
          trend={{ value: 12, isPositive: true }}
        />
        <StatCard
          title="Running"
          value={stats.running}
          icon={ClockIcon}
          color="warning"
          className="animate-pulse-slow"
        />
        <StatCard
          title="Completed"
          value={stats.completed}
          icon={CheckCircleIcon}
          color="success"
          trend={{ value: 8, isPositive: true }}
        />
        <StatCard
          title="Failed"
          value={stats.failed}
          icon={XCircleIcon}
          color="error"
          trend={{ value: 3, isPositive: false }}
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Active Jobs Progress */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="card-header">
              <h2 className="text-xl font-semibold text-secondary-900">Active Jobs</h2>
            </div>
            <div className="card-body">
              {runningJobs.length === 0 ? (
                <div className="text-center py-12">
                  <ClockIcon className="w-12 h-12 text-secondary-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-secondary-900 mb-2">
                    No active jobs
                  </h3>
                  <p className="text-secondary-600 mb-6">
                    Create a new scraping job to get started
                  </p>
                  <Link to="/jobs/new" className="btn-primary">
                    <PlusIcon className="w-4 h-4 mr-2" />
                    Create Job
                  </Link>
                </div>
              ) : (
                <div className="space-y-4">
                  {runningJobs.map((job) => (
                    <JobProgress key={job.id} job={job} />
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Quick Actions & Recent Activity */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <QuickActions />

          {/* Recent Jobs */}
          <div className="card">
            <div className="card-header">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-secondary-900">Recent Jobs</h2>
                <Link to="/jobs" className="text-sm text-primary-600 hover:text-primary-700">
                  View all
                </Link>
              </div>
            </div>
            <div className="card-body p-0">
              <RecentJobs jobs={jobs.slice(0, 5)} isLoading={isLoading} />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
