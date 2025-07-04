import { useEffect } from 'react'
import { useAppDispatch } from '@/store'
import { setCurrentPage } from '@/store/slices/uiSlice'

const Jobs = () => {
  const dispatch = useAppDispatch()

  useEffect(() => {
    dispatch(setCurrentPage('jobs'))
  }, [dispatch])

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">Jobs</h1>
          <p className="text-secondary-600 mt-1">
            Manage your scraping jobs and monitor their progress
          </p>
        </div>
      </div>

      <div className="card">
        <div className="card-body text-center py-12">
          <h2 className="text-xl font-semibold text-secondary-900 mb-2">Jobs Page</h2>
          <p className="text-secondary-600">This page will show a detailed list of all scraping jobs.</p>
        </div>
      </div>
    </div>
  )
}

export default Jobs
