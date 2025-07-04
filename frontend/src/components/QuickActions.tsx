import { Link } from 'react-router-dom'
import {
  PlusIcon,
  DocumentArrowDownIcon,
  ChartBarIcon,
  CogIcon,
  BookOpenIcon,
  QuestionMarkCircleIcon,
} from '@heroicons/react/24/outline'

const quickActions = [
  {
    name: 'New Job',
    description: 'Start scraping',
    href: '/jobs/new',
    icon: PlusIcon,
    color: 'primary',
  },
  {
    name: 'View Results',
    description: 'Browse data',
    href: '/results',
    icon: ChartBarIcon,
    color: 'success',
  },
  {
    name: 'Export Data',
    description: 'Download CSV',
    href: '/exports',
    icon: DocumentArrowDownIcon,
    color: 'secondary',
  },
  {
    name: 'Settings',
    description: 'Configure',
    href: '/settings',
    icon: CogIcon,
    color: 'secondary',
  },
]

const resources = [
  {
    name: 'Documentation',
    description: 'Learn how to use 9Scraper',
    href: '/docs',
    icon: BookOpenIcon,
  },
  {
    name: 'Support',
    description: 'Get help when you need it',
    href: '/support',
    icon: QuestionMarkCircleIcon,
  },
]

const QuickActions = () => {
  const getColorClasses = (color: string) => {
    switch (color) {
      case 'primary':
        return 'bg-primary-50 text-primary-700 hover:bg-primary-100'
      case 'success':
        return 'bg-success-50 text-success-700 hover:bg-success-100'
      case 'secondary':
        return 'bg-secondary-50 text-secondary-700 hover:bg-secondary-100'
      default:
        return 'bg-secondary-50 text-secondary-700 hover:bg-secondary-100'
    }
  }

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="text-lg font-semibold text-secondary-900">Quick Actions</h2>
      </div>
      <div className="card-body">
        <div className="grid grid-cols-2 gap-3 mb-6">
          {quickActions.map((action) => (
            <Link
              key={action.name}
              to={action.href}
              className={`${getColorClasses(action.color)} p-4 rounded-lg transition-colors group`}
            >
              <action.icon className="w-6 h-6 mb-2 group-hover:scale-110 transition-transform" />
              <h3 className="font-medium text-sm">{action.name}</h3>
              <p className="text-xs opacity-75">{action.description}</p>
            </Link>
          ))}
        </div>

        {/* Resources */}
        <div className="border-t border-secondary-200 pt-4">
          <h3 className="text-sm font-medium text-secondary-900 mb-3">Resources</h3>
          <div className="space-y-2">
            {resources.map((resource) => (
              <Link
                key={resource.name}
                to={resource.href}
                className="flex items-center space-x-3 p-2 rounded-lg hover:bg-secondary-50 transition-colors group"
              >
                <resource.icon className="w-5 h-5 text-secondary-500 group-hover:text-secondary-700" />
                <div>
                  <p className="text-sm font-medium text-secondary-900">{resource.name}</p>
                  <p className="text-xs text-secondary-500">{resource.description}</p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default QuickActions
