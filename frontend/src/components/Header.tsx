import { useState } from 'react'
import { useAppSelector } from '@/store'
import {
  MagnifyingGlassIcon,
  BellIcon,
  UserCircleIcon,
  SunIcon,
  MoonIcon,
} from '@heroicons/react/24/outline'
import { BellIcon as BellSolidIcon } from '@heroicons/react/24/solid'

const Header = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [notificationsOpen, setNotificationsOpen] = useState(false)
  const theme = useAppSelector(state => state.ui.theme)
  const notifications = useAppSelector(state => state.ui.notifications)
  const unreadCount = notifications.filter(n => !n.read).length

  return (
    <header className="bg-white border-b border-secondary-200 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Search */}
        <div className="flex-1 max-w-lg">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MagnifyingGlassIcon className="h-5 w-5 text-secondary-400" />
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="form-input pl-10 pr-4 py-2 w-full"
              placeholder="Search jobs, businesses..."
            />
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center space-x-4">
          {/* Theme toggle */}
          <button
            onClick={() => {/* TODO: Implement theme toggle */}}
            className="p-2 text-secondary-500 hover:text-secondary-700 hover:bg-secondary-100 rounded-lg transition-colors"
          >
            {theme === 'light' ? (
              <MoonIcon className="w-5 h-5" />
            ) : (
              <SunIcon className="w-5 h-5" />
            )}
          </button>

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => setNotificationsOpen(!notificationsOpen)}
              className="p-2 text-secondary-500 hover:text-secondary-700 hover:bg-secondary-100 rounded-lg transition-colors relative"
            >
              {unreadCount > 0 ? (
                <BellSolidIcon className="w-5 h-5 text-primary-600" />
              ) : (
                <BellIcon className="w-5 h-5" />
              )}
              {unreadCount > 0 && (
                <span className="absolute -top-1 -right-1 w-5 h-5 bg-error-500 text-white text-xs font-medium rounded-full flex items-center justify-center">
                  {unreadCount > 9 ? '9+' : unreadCount}
                </span>
              )}
            </button>

            {/* Notifications dropdown */}
            {notificationsOpen && (
              <>
                <div
                  className="fixed inset-0 z-10"
                  onClick={() => setNotificationsOpen(false)}
                />
                <div className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-lg border border-secondary-200 z-20 max-h-96 overflow-y-auto">
                  <div className="p-4 border-b border-secondary-200">
                    <h3 className="text-lg font-semibold text-secondary-900">Notifications</h3>
                  </div>
                  
                  {notifications.length === 0 ? (
                    <div className="p-4 text-center text-secondary-500">
                      No notifications yet
                    </div>
                  ) : (
                    <div className="divide-y divide-secondary-200">
                      {notifications.slice(0, 10).map((notification) => (
                        <div
                          key={notification.id}
                          className={`p-4 hover:bg-secondary-50 transition-colors ${
                            !notification.read ? 'bg-primary-50' : ''
                          }`}
                        >
                          <div className="flex items-start space-x-3">
                            <div className={`w-2 h-2 rounded-full mt-2 ${
                              notification.type === 'success' ? 'bg-success-500' :
                              notification.type === 'error' ? 'bg-error-500' :
                              notification.type === 'warning' ? 'bg-warning-500' :
                              'bg-primary-500'
                            }`} />
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-medium text-secondary-900">
                                {notification.title}
                              </p>
                              <p className="text-sm text-secondary-500 mt-1">
                                {notification.message}
                              </p>
                              <p className="text-xs text-secondary-400 mt-2">
                                {new Date(notification.timestamp).toLocaleString()}
                              </p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </>
            )}
          </div>

          {/* User menu */}
          <button className="p-2 text-secondary-500 hover:text-secondary-700 hover:bg-secondary-100 rounded-lg transition-colors">
            <UserCircleIcon className="w-6 h-6" />
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header
