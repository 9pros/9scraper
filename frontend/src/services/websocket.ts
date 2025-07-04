import { io, Socket } from 'socket.io-client'
import { WebSocketMessage, JobProgressMessage } from '@/types'

type EventCallback = (data: any) => void

class WebSocketService {
  private socket: Socket | null = null
  private url: string
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000

  constructor(url?: string) {
    this.url = url || import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.socket = io(this.url, {
          transports: ['websocket'],
          timeout: 10000,
        })

        this.socket.on('connect', () => {
          console.log('WebSocket connected')
          this.reconnectAttempts = 0
          resolve()
        })

        this.socket.on('disconnect', (reason) => {
          console.log('WebSocket disconnected:', reason)
          this.handleReconnect()
        })

        this.socket.on('connect_error', (error) => {
          console.error('WebSocket connection error:', error)
          reject(error)
        })

        this.socket.on('message', (message: WebSocketMessage) => {
          this.handleMessage(message)
        })

      } catch (error) {
        reject(error)
      }
    })
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }

  isConnected(): boolean {
    return this.socket?.connected || false
  }

  private handleMessage(message: WebSocketMessage): void {
    // Handle different message types
    switch (message.type) {
      case 'job_progress':
        this.emit('jobProgress', message.data)
        break
      case 'job_completed':
        this.emit('jobCompleted', message.data)
        break
      case 'job_failed':
        this.emit('jobFailed', message.data)
        break
      case 'result_update':
        this.emit('resultUpdate', message.data)
        break
      default:
        console.log('Unknown message type:', message.type)
    }
  }

  private handleReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1)
      
      console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`)
      
      setTimeout(() => {
        this.connect().catch(console.error)
      }, delay)
    } else {
      console.error('Max reconnection attempts reached')
    }
  }

  // Event handling
  on(event: string, callback: EventCallback): void {
    if (this.socket) {
      this.socket.on(event, callback)
    }
  }

  off(event: string, callback?: EventCallback): void {
    if (this.socket) {
      this.socket.off(event, callback)
    }
  }

  emit(event: string, data: any): void {
    if (this.socket) {
      this.socket.emit(event, data)
    }
  }

  // Specific methods for job tracking
  subscribeToJob(jobId: string): void {
    this.emit('subscribe_job', { job_id: jobId })
  }

  unsubscribeFromJob(jobId: string): void {
    this.emit('unsubscribe_job', { job_id: jobId })
  }

  onJobProgress(callback: (data: JobProgressMessage) => void): void {
    this.on('jobProgress', callback)
  }

  onJobCompleted(callback: (data: any) => void): void {
    this.on('jobCompleted', callback)
  }

  onJobFailed(callback: (data: any) => void): void {
    this.on('jobFailed', callback)
  }

  onResultUpdate(callback: (data: any) => void): void {
    this.on('resultUpdate', callback)
  }
}

// Create singleton instance
export const wsService = new WebSocketService()

// Hook for React components
export const useWebSocket = () => {
  return {
    connect: () => wsService.connect(),
    disconnect: () => wsService.disconnect(),
    isConnected: () => wsService.isConnected(),
    subscribeToJob: (jobId: string) => wsService.subscribeToJob(jobId),
    unsubscribeFromJob: (jobId: string) => wsService.unsubscribeFromJob(jobId),
    onJobProgress: (callback: (data: JobProgressMessage) => void) => wsService.onJobProgress(callback),
    onJobCompleted: (callback: (data: any) => void) => wsService.onJobCompleted(callback),
    onJobFailed: (callback: (data: any) => void) => wsService.onJobFailed(callback),
    onResultUpdate: (callback: (data: any) => void) => wsService.onResultUpdate(callback),
  }
}
