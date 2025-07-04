import { useEffect } from 'react'
import { useAppDispatch } from '@/store'
import { setCurrentPage } from '@/store/slices/uiSlice'

const Results = () => {
  const dispatch = useAppDispatch()

  useEffect(() => {
    dispatch(setCurrentPage('results'))
  }, [dispatch])

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-secondary-900">Results</h1>
        <p className="text-secondary-600 mt-1">
          Browse and export your scraped business data
        </p>
      </div>

      <div className="card">
        <div className="card-body text-center py-12">
          <h2 className="text-xl font-semibold text-secondary-900 mb-2">Results Page</h2>
          <p className="text-secondary-600">This page will show scraped business data with filtering and export options.</p>
        </div>
      </div>
    </div>
  )
}

export default Results
