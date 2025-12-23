// lib/useWebSocket.ts
import { useEffect, useRef, useState, useCallback } from "react"

interface UseWebSocketOptions {
  url: string
  onMessage?: (data: any) => void          // JSON / text
  onBinary?: (data: ArrayBuffer) => void   // audio / raw bytes
  onOpen?: () => void
  onClose?: () => void
  onError?: (error: Event) => void
  autoConnect?: boolean
}

export const useWebSocket = (options: UseWebSocketOptions) => {
  const {
    url,
    onMessage,
    onBinary,
    onOpen,
    onClose,
    onError,
    autoConnect = false,
  } = options

  const [isConnected, setIsConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)

  const callbacksRef = useRef({
    onMessage,
    onBinary,
    onOpen,
    onClose,
    onError,
  })

  // keep callbacks fresh without reconnecting
  useEffect(() => {
    callbacksRef.current = {
      onMessage,
      onBinary,
      onOpen,
      onClose,
      onError,
    }
  }, [onMessage, onBinary, onOpen, onClose, onError])

  const connect = useCallback(() => {
    if (wsRef.current) return

    const ws = new WebSocket(url)
    ws.binaryType = "arraybuffer"
    wsRef.current = ws

    ws.onopen = () => {
      setIsConnected(true)
      callbacksRef.current.onOpen?.()
    }

    ws.onmessage = (event) => {
      const data = event.data

      // binary path
      if (data instanceof ArrayBuffer) {
        callbacksRef.current.onBinary?.(data)
        return
      }

      // text / JSON path
      try {
        callbacksRef.current.onMessage?.(JSON.parse(data))
      } catch {
        callbacksRef.current.onMessage?.(data)
      }
    }

    ws.onerror = (e) => callbacksRef.current.onError?.(e)

    ws.onclose = () => {
      wsRef.current = null
      setIsConnected(false)
      callbacksRef.current.onClose?.()
    }
  }, [url])

  const disconnect = useCallback(() => {
    wsRef.current?.close(1000)
    wsRef.current = null
    setIsConnected(false)
  }, [])

  const sendMessage = useCallback((data: any) => {
    if (wsRef.current?.readyState !== WebSocket.OPEN) return false
    wsRef.current.send(typeof data === "string" ? data : JSON.stringify(data))
    return true
  }, [])

  const sendBinary = useCallback((data: ArrayBuffer | Blob) => {
    if (wsRef.current?.readyState !== WebSocket.OPEN) return false
    wsRef.current.send(data)
    return true
  }, [])

  useEffect(() => {
    if (autoConnect) connect()
    return () => wsRef.current?.close(1000)
  }, [url])

  return {
    isConnected,
    connect,
    disconnect,
    sendMessage,
    sendBinary,
  }
}
