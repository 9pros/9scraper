import { NavLink } from 'react-router-dom'
import { useAppSelector, useAppDispatch } from '@/store'
import { toggleSidebar } from '@/store/slices/uiSlice'
import {
  HomeIcon,
  DocumentTextIcon,
  ChartBarIcon,
  CogIcon,
  Bars3Icon,
  PlusIcon,
} from '@heroicons/react/24/outline'
import {
  HomeIcon as HomeSolidIcon,
  DocumentTextIcon as DocumentSolidIcon,
  ChartBarIcon as ChartSolidIcon,
  CogIcon as CogSolidIcon,
} from '@heroicons/react/24/solid'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon, activeIcon: HomeSolidIcon },
  { name: 'Jobs', href: '/jobs', icon: DocumentTextIcon, activeIcon: DocumentSolidIcon },
  { name: 'Results', href: '/results', icon: ChartBarIcon, activeIcon: ChartSolidIcon },
  { name: 'Settings', href: '/settings', icon: CogIcon, activeIcon: CogSolidIcon },
]

const Sidebar = () => {
  const dispatch = useAppDispatch()
  const sidebarOpen = useAppSelector(state => state.ui.sidebarOpen)

  return (
    <div className={`fixed inset-y-0 left-0 z-50 bg-white border-r border-secondary-200 transition-all duration-300 ${
      sidebarOpen ? 'w-64' : 'w-16'
    }`}>
      <div className="flex flex-col h-full">
        {/* Logo and toggle */}
        <div className="flex items-center justify-between p-4 border-b border-secondary-200">
          {sidebarOpen && (
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">9</span>
              </div>
              <span className="text-xl font-bold text-gradient">Scraper</span>
            </div>
          )}
          
          <button
            onClick={() => dispatch(toggleSidebar())}
            className="p-2 rounded-lg text-secondary-500 hover:text-secondary-700 hover:bg-secondary-100 transition-colors"
          >
            <Bars3Icon className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                `flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 group ${
                  isActive
                    ? 'bg-primary-50 text-primary-700 shadow-sm'
                    : 'text-secondary-700 hover:bg-secondary-100 hover:text-secondary-900'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  {isActive ? (
                    <item.activeIcon className="w-5 h-5 mr-3 flex-shrink-0" />
                  ) : (
                    <item.icon className="w-5 h-5 mr-3 flex-shrink-0" />
                  )}
                  {sidebarOpen && (
                    <span className="truncate">{item.name}</span>
                  )}
                </>
              )}
            </NavLink>
          ))}
        </nav>

        {/* Create Job Button */}
        <div className="p-4 border-t border-secondary-200">
          <NavLink
            to="/jobs/new"
            className="btn-primary w-full justify-center glow-on-hover"
          >
            <PlusIcon className="w-5 h-5 mr-2" />
            {sidebarOpen && 'New Job'}
          </NavLink>
        </div>

        {/* User section */}
        {sidebarOpen && (
          <div className="p-4 border-t border-secondary-200">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-medium">U</span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-secondary-900 truncate">User</p>
                <p className="text-xs text-secondary-500 truncate">Free Plan</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Sidebar
