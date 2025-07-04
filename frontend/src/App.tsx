import { Routes, Route } from 'react-router-dom'
import { useEffect } from 'react'
import { useAppDispatch } from '@/store'
import { setCurrentPage } from '@/store/slices/uiSlice'

import Layout from '@/components/Layout'
import Dashboard from '@/pages/Dashboard'
import Jobs from '@/pages/Jobs'
import JobDetails from '@/pages/JobDetails'
import Results from '@/pages/Results'
import Settings from '@/pages/Settings'
import NotFound from '@/pages/NotFound'

function App() {
  const dispatch = useAppDispatch()

  useEffect(() => {
    // Set initial page based on current route
    const path = window.location.pathname
    const pageName = path.split('/')[1] || 'dashboard'
    dispatch(setCurrentPage(pageName))
  }, [dispatch])

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/jobs" element={<Jobs />} />
        <Route path="/jobs/:id" element={<JobDetails />} />
        <Route path="/results" element={<Results />} />
        <Route path="/results/:jobId" element={<Results />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Layout>
  )
}

export default App
