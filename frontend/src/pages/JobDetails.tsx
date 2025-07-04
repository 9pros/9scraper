import { useParams } from 'react-router-dom'

const JobDetails = () => {
  const { id } = useParams<{ id: string }>()

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-secondary-900">Job Details</h1>
        <p className="text-secondary-600 mt-1">
          View detailed information about job {id}
        </p>
      </div>

      <div className="card">
        <div className="card-body text-center py-12">
          <h2 className="text-xl font-semibold text-secondary-900 mb-2">Job Details Page</h2>
          <p className="text-secondary-600">This page will show detailed job information and real-time progress.</p>
        </div>
      </div>
    </div>
  )
}

export default JobDetails
