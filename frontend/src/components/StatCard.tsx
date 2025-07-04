import { ReactNode } from 'react'
import { ArrowUpIcon, ArrowDownIcon } from '@heroicons/react/24/outline'
import clsx from 'clsx'

interface StatCardProps {
  title: string
  value: number | string
  icon: React.ComponentType<{ className?: string }>
  color: 'primary' | 'secondary' | 'success' | 'warning' | 'error'
  trend?: {
    value: number
    isPositive: boolean
  }
  className?: string
  children?: ReactNode
}

const colorClasses = {
  primary: {
    bg: 'bg-primary-50',
    icon: 'text-primary-600',
    value: 'text-primary-900',
  },
  secondary: {
    bg: 'bg-secondary-50',
    icon: 'text-secondary-600',
    value: 'text-secondary-900',
  },
  success: {
    bg: 'bg-success-50',
    icon: 'text-success-600',
    value: 'text-success-900',
  },
  warning: {
    bg: 'bg-warning-50',
    icon: 'text-warning-600',
    value: 'text-warning-900',
  },
  error: {
    bg: 'bg-error-50',
    icon: 'text-error-600',
    value: 'text-error-900',
  },
}

const StatCard = ({ 
  title, 
  value, 
  icon: Icon, 
  color, 
  trend, 
  className,
  children 
}: StatCardProps) => {
  const colors = colorClasses[color]

  return (
    <div className={clsx('card hover:shadow-lg transition-shadow duration-200', className)}>
      <div className="card-body">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-secondary-600">{title}</p>
            <p className={clsx('text-3xl font-bold mt-2', colors.value)}>
              {typeof value === 'number' ? value.toLocaleString() : value}
            </p>
            
            {trend && (
              <div className="flex items-center mt-2">
                {trend.isPositive ? (
                  <ArrowUpIcon className="w-4 h-4 text-success-500 mr-1" />
                ) : (
                  <ArrowDownIcon className="w-4 h-4 text-error-500 mr-1" />
                )}
                <span className={clsx(
                  'text-sm font-medium',
                  trend.isPositive ? 'text-success-600' : 'text-error-600'
                )}>
                  {trend.value}%
                </span>
                <span className="text-sm text-secondary-500 ml-1">vs last week</span>
              </div>
            )}
            
            {children}
          </div>
          
          <div className={clsx('p-3 rounded-xl', colors.bg)}>
            <Icon className={clsx('w-6 h-6', colors.icon)} />
          </div>
        </div>
      </div>
    </div>
  )
}

export default StatCard
