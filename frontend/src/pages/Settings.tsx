import { useEffect } from 'react'
import { useAppDispatch } from '@/store'
import { setCurrentPage } from '@/store/slices/uiSlice'

const Settings = () => {
  const dispatch = useAppDispatch()

  useEffect(() => {
    dispatch(setCurrentPage('settings'))
  }, [dispatch])

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-secondary-900">Settings</h1>
        <p className="text-secondary-600 mt-1">
          Configure your account and scraping preferences
        </p>
      </div>

      <div className="card">
        <div className="card-body text-center py-12">
          <h2 className="text-xl font-semibold text-secondary-900 mb-2">Settings Page</h2>
          <p className="text-secondary-600">This page will contain user settings and configuration options.</p>
        </div>
      </div>
    </div>
  )
}

export default Settings
