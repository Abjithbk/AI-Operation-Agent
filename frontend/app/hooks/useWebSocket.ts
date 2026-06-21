import { useCallback, useEffect, useRef, useState } from "react";


export function useWebSocket() {
    const ws = useRef<WebSocket | null>(null)
    const [isConnected,setIsConnected] = useState(false)
    const messageCallback = useRef<((data:any) => void) | null>(null)
    const reconnectTimeout = useRef<NodeJS.Timeout | null>(null)
    const isConnecting = useRef(false)
    useEffect(() => {
        const wsUrl: string | undefined = process.env.NEXT_PUBLIC_WS_URL

        if(ws.current || isConnecting.current) {
            return;
        }

        if (!wsUrl) {
            return
        }

        const connect = () => {
            if(isConnecting.current) return
            isConnecting.current = true;
            console.log('🔌 Connecting to WebSocket...');
            try {
        ws.current = new WebSocket(wsUrl);

        ws.current.onopen = () => {
          console.log('✅ WebSocket connected');
          setIsConnected(true);
          isConnecting.current = false;
        };

        ws.current.onclose = (event) => {
          console.log('❌ WebSocket closed:', event.code);
          setIsConnected(false);
          ws.current = null;
          isConnecting.current = false;

          // Auto-reconnect after 3 seconds
          if (!reconnectTimeout.current) {
            reconnectTimeout.current = setTimeout(() => {
              reconnectTimeout.current = null;
              connect();
            }, 3000);
          }
        };

        ws.current.onerror = (error) => {
          console.error('❌ WebSocket error');
          isConnecting.current = false;
        };

        ws.current.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            if (messageCallback.current) {
              messageCallback.current(data);
            }
          } catch (error) {
            console.error('❌ Failed to parse message:', error);
          }
        };
      } catch (error) {
        console.error('❌ Failed to create WebSocket:', error);
        isConnecting.current = false;
      }
        };
        connect()
        return () => {
      if (reconnectTimeout.current) {
        clearTimeout(reconnectTimeout.current);
        reconnectTimeout.current = null;
      }
      if (ws.current) {
        console.log('🔌 Closing WebSocket');
        ws.current.close();
        ws.current = null;
      }
      isConnecting.current = false;
    };
    },[])

    const onMessage = useCallback((callback : (data:any) => void) => {
        messageCallback.current = callback
    },[]);
    return {isConnected,onMessage}

}