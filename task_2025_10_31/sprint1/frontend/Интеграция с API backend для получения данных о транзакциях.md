# Техническое задание: Интеграция с API backend для получения данных о транзакциях

## Общая информация
- **Приоритет:** normal
- **Оценка:** 3 SP
- **Исполнитель:** frontend
- **Срок выполнения:** 3 дня

## Цель
Обеспечить надежную интеграцию с API backend для получения, обработки и отображения данных о транзакциях, включая обработку ошибок, кэширование и оптимизацию производительности.

## Требования

### Функциональные требования
1. **API Integration:** Интеграция с REST API endpoints
2. **Data Fetching:** Получение данных о транзакциях
3. **Error Handling:** Обработка ошибок API
4. **Caching:** Кэширование данных для производительности
5. **Real-time Updates:** Обновление данных в реальном времени
6. **Offline Support:** Работа в офлайн режиме

### Нефункциональные требования
1. **Performance:** Время отклика < 500ms
2. **Reliability:** 99.9% uptime для API calls
3. **Security:** Защита от XSS, CSRF
4. **Scalability:** Поддержка 10,000+ запросов
5. **Monitoring:** Отслеживание API performance

## Архитектура API интеграции

### 1. API Service Structure
```
src/
├── services/
│   ├── api/
│   │   ├── client.ts
│   │   ├── endpoints.ts
│   │   ├── interceptors.ts
│   │   └── types.ts
│   ├── transactionService.ts
│   ├── authService.ts
│   └── cacheService.ts
├── hooks/
│   ├── useApi.ts
│   ├── useTransactions.ts
│   ├── useCache.ts
│   └── useWebSocket.ts
├── utils/
│   ├── apiHelpers.ts
│   ├── errorHandlers.ts
│   └── validators.ts
└── types/
    ├── api.ts
    └── transaction.ts
```

### 2. API Client Configuration
```typescript
// services/api/client.ts
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { authService } from '../authService';
import { cacheService } from '../cacheService';
import { errorHandler } from '../../utils/errorHandlers';

class ApiClient {
  private client: AxiosInstance;
  private baseURL: string;
  private timeout: number;

  constructor() {
    this.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';
    this.timeout = 10000; // 10 seconds
    
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: this.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      async (config) => {
        // Add authentication token
        const token = authService.getAccessToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }

        // Add request ID for tracking
        config.headers['X-Request-ID'] = this.generateRequestId();

        // Check cache for GET requests
        if (config.method === 'get' && config.cache !== false) {
          const cachedResponse = await cacheService.get(config.url!);
          if (cachedResponse) {
            return Promise.reject({
              isCached: true,
              data: cachedResponse,
              config
            });
          }
        }

        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      async (response: AxiosResponse) => {
        // Cache successful GET responses
        if (response.config.method === 'get' && response.config.cache !== false) {
          await cacheService.set(response.config.url!, response.data);
        }

        return response;
      },
      async (error) => {
        // Handle cached responses
        if (error.isCached) {
          return Promise.resolve(error);
        }

        // Handle authentication errors
        if (error.response?.status === 401) {
          try {
            await authService.refreshToken();
            // Retry original request
            return this.client.request(error.config);
          } catch (refreshError) {
            authService.logout();
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }

        // Handle rate limiting
        if (error.response?.status === 429) {
          const retryAfter = error.response.headers['retry-after'];
          if (retryAfter) {
            await this.delay(parseInt(retryAfter) * 1000);
            return this.client.request(error.config);
          }
        }

        // Handle network errors
        if (!error.response) {
          errorHandler.handleNetworkError(error);
        }

        return Promise.reject(error);
      }
    );
  }

  private generateRequestId(): string {
    return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Public methods
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }

  async patch<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.patch<T>(url, data, config);
    return response.data;
  }
}

export const apiClient = new ApiClient();
```

### 3. Transaction Service
```typescript
// services/transactionService.ts
import { apiClient } from './api/client';
import { Transaction, TransactionFilters, TransactionResponse } from '../types/transaction';

export class TransactionService {
  private baseEndpoint = '/transactions';

  async getTransactions(params: {
    userId: string;
    page?: number;
    limit?: number;
    filters?: TransactionFilters;
    sort?: string;
    order?: 'asc' | 'desc';
  }): Promise<TransactionResponse> {
    const queryParams = new URLSearchParams();
    
    if (params.page) queryParams.append('page', params.page.toString());
    if (params.limit) queryParams.append('limit', params.limit.toString());
    if (params.sort) queryParams.append('sort', params.sort);
    if (params.order) queryParams.append('order', params.order);
    
    // Add filters to query params
    if (params.filters) {
      Object.entries(params.filters).forEach(([key, value]) => {
        if (value !== null && value !== undefined && value !== '') {
          queryParams.append(key, value.toString());
        }
      });
    }

    const url = `${this.baseEndpoint}?${queryParams.toString()}`;
    
    return await apiClient.get<TransactionResponse>(url, {
      cache: true,
      timeout: 15000
    });
  }

  async getTransactionById(id: string): Promise<Transaction> {
    return await apiClient.get<Transaction>(`${this.baseEndpoint}/${id}`, {
      cache: true
    });
  }

  async createTransaction(data: {
    amount: number;
    currency: string;
    description: string;
    paymentMethod: string;
    recipientId?: string;
  }): Promise<Transaction> {
    return await apiClient.post<Transaction>(this.baseEndpoint, data, {
      cache: false
    });
  }

  async updateTransaction(id: string, data: Partial<Transaction>): Promise<Transaction> {
    return await apiClient.put<Transaction>(`${this.baseEndpoint}/${id}`, data, {
      cache: false
    });
  }

  async deleteTransaction(id: string): Promise<void> {
    await apiClient.delete(`${this.baseEndpoint}/${id}`, {
      cache: false
    });
  }

  async exportTransactions(params: {
    userId: string;
    format: 'csv' | 'pdf' | 'excel';
    filters?: TransactionFilters;
    selectedIds?: string[];
  }): Promise<Blob> {
    const queryParams = new URLSearchParams();
    queryParams.append('format', params.format);
    
    if (params.filters) {
      Object.entries(params.filters).forEach(([key, value]) => {
        if (value !== null && value !== undefined && value !== '') {
          queryParams.append(key, value.toString());
        }
      });
    }
    
    if (params.selectedIds?.length) {
      params.selectedIds.forEach(id => queryParams.append('ids', id));
    }

    const response = await apiClient.client.get(
      `${this.baseEndpoint}/export?${queryParams.toString()}`,
      {
        responseType: 'blob',
        cache: false
      }
    );

    return response.data;
  }

  async getTransactionStatistics(params: {
    userId: string;
    period: 'day' | 'week' | 'month' | 'year';
    startDate?: string;
    endDate?: string;
  }): Promise<{
    totalAmount: number;
    totalCount: number;
    averageAmount: number;
    topCategories: Array<{ category: string; amount: number; count: number }>;
    monthlyTrend: Array<{ month: string; amount: number; count: number }>;
  }> {
    const queryParams = new URLSearchParams();
    queryParams.append('period', params.period);
    
    if (params.startDate) queryParams.append('startDate', params.startDate);
    if (params.endDate) queryParams.append('endDate', params.endDate);

    return await apiClient.get(`${this.baseEndpoint}/statistics?${queryParams.toString()}`, {
      cache: true,
      timeout: 20000
    });
  }
}

export const transactionService = new TransactionService();
```

### 4. Cache Service
```typescript
// services/cacheService.ts
interface CacheItem {
  data: any;
  timestamp: number;
  ttl: number;
}

export class CacheService {
  private cache = new Map<string, CacheItem>();
  private maxSize = 1000; // Maximum number of cached items
  private defaultTTL = 5 * 60 * 1000; // 5 minutes

  async get<T>(key: string): Promise<T | null> {
    const item = this.cache.get(key);
    
    if (!item) {
      return null;
    }

    // Check if item has expired
    if (Date.now() - item.timestamp > item.ttl) {
      this.cache.delete(key);
      return null;
    }

    return item.data as T;
  }

  async set<T>(key: string, data: T, ttl?: number): Promise<void> {
    // Remove oldest items if cache is full
    if (this.cache.size >= this.maxSize) {
      const oldestKey = this.cache.keys().next().value;
      this.cache.delete(oldestKey);
    }

    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl: ttl || this.defaultTTL
    });
  }

  async delete(key: string): Promise<void> {
    this.cache.delete(key);
  }

  async clear(): Promise<void> {
    this.cache.clear();
  }

  async invalidatePattern(pattern: string): Promise<void> {
    const regex = new RegExp(pattern);
    for (const key of this.cache.keys()) {
      if (regex.test(key)) {
        this.cache.delete(key);
      }
    }
  }

  // Invalidate cache for specific user
  async invalidateUser(userId: string): Promise<void> {
    await this.invalidatePattern(`.*userId=${userId}.*`);
  }

  // Get cache statistics
  getStats(): {
    size: number;
    maxSize: number;
    hitRate: number;
  } {
    return {
      size: this.cache.size,
      maxSize: this.maxSize,
      hitRate: 0 // TODO: Implement hit rate tracking
    };
  }
}

export const cacheService = new CacheService();
```

### 5. Custom Hooks

#### useTransactions Hook
```typescript
// hooks/useTransactions.ts
import { useState, useEffect, useCallback, useRef } from 'react';
import { transactionService } from '../services/transactionService';
import { Transaction, TransactionFilters } from '../types/transaction';

interface UseTransactionsOptions {
  userId: string;
  filters?: TransactionFilters;
  page?: number;
  limit?: number;
  sort?: string;
  order?: 'asc' | 'desc';
  autoFetch?: boolean;
  cache?: boolean;
}

interface UseTransactionsReturn {
  transactions: Transaction[];
  isLoading: boolean;
  error: string | null;
  totalCount: number;
  totalPages: number;
  currentPage: number;
  refetch: () => Promise<void>;
  fetchMore: () => Promise<void>;
  hasMore: boolean;
}

export const useTransactions = ({
  userId,
  filters = {},
  page = 1,
  limit = 20,
  sort = 'createdAt',
  order = 'desc',
  autoFetch = true,
  cache = true
}: UseTransactionsOptions): UseTransactionsReturn => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [totalCount, setTotalCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(page);
  const [hasMore, setHasMore] = useState(true);
  
  const abortControllerRef = useRef<AbortController | null>(null);

  const fetchTransactions = useCallback(async (pageNum: number = 1, append: boolean = false) => {
    // Cancel previous request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    // Create new abort controller
    abortControllerRef.current = new AbortController();

    setIsLoading(true);
    setError(null);

    try {
      const response = await transactionService.getTransactions({
        userId,
        page: pageNum,
        limit,
        filters,
        sort,
        order
      });

      if (append) {
        setTransactions(prev => [...prev, ...response.data]);
      } else {
        setTransactions(response.data);
      }

      setTotalCount(response.total);
      setCurrentPage(pageNum);
      setHasMore(pageNum < Math.ceil(response.total / limit));
    } catch (err: any) {
      if (err.name !== 'AbortError') {
        setError(err.message || 'Failed to fetch transactions');
      }
    } finally {
      setIsLoading(false);
    }
  }, [userId, filters, limit, sort, order]);

  const refetch = useCallback(async () => {
    await fetchTransactions(1, false);
  }, [fetchTransactions]);

  const fetchMore = useCallback(async () => {
    if (!isLoading && hasMore) {
      await fetchTransactions(currentPage + 1, true);
    }
  }, [fetchTransactions, currentPage, hasMore, isLoading]);

  useEffect(() => {
    if (autoFetch) {
      fetchTransactions();
    }

    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, [fetchTransactions, autoFetch]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  return {
    transactions,
    isLoading,
    error,
    totalCount,
    totalPages: Math.ceil(totalCount / limit),
    currentPage,
    refetch,
    fetchMore,
    hasMore
  };
};
```

#### useWebSocket Hook
```typescript
// hooks/useWebSocket.ts
import { useEffect, useRef, useState } from 'react';

interface UseWebSocketOptions {
  url: string;
  onMessage?: (data: any) => void;
  onError?: (error: Event) => void;
  onOpen?: () => void;
  onClose?: () => void;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
}

export const useWebSocket = ({
  url,
  onMessage,
  onError,
  onOpen,
  onClose,
  reconnectInterval = 5000,
  maxReconnectAttempts = 5
}: UseWebSocketOptions) => {
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const reconnectAttemptsRef = useRef(0);

  const connect = () => {
    try {
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
        setError(null);
        reconnectAttemptsRef.current = 0;
        onOpen?.();
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          onMessage?.(data);
        } catch (err) {
          console.error('Failed to parse WebSocket message:', err);
        }
      };

      ws.onerror = (error) => {
        setError('WebSocket connection error');
        onError?.(error);
      };

      ws.onclose = () => {
        setIsConnected(false);
        onClose?.();
        
        // Attempt to reconnect
        if (reconnectAttemptsRef.current < maxReconnectAttempts) {
          reconnectAttemptsRef.current++;
          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, reconnectInterval);
        }
      };
    } catch (err) {
      setError('Failed to create WebSocket connection');
    }
  };

  const disconnect = () => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  };

  const sendMessage = (message: any) => {
    if (wsRef.current && isConnected) {
      wsRef.current.send(JSON.stringify(message));
    }
  };

  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, [url]);

  return {
    isConnected,
    error,
    sendMessage,
    connect,
    disconnect
  };
};
```

### 6. Error Handling
```typescript
// utils/errorHandlers.ts
export class ErrorHandler {
  handleNetworkError(error: any) {
    console.error('Network error:', error);
    
    // Show user-friendly message
    this.showNotification('Network connection lost. Please check your internet connection.', 'error');
  }

  handleApiError(error: any) {
    console.error('API error:', error);
    
    const status = error.response?.status;
    const message = error.response?.data?.message || error.message;

    switch (status) {
      case 400:
        this.showNotification('Invalid request. Please check your input.', 'error');
        break;
      case 401:
        this.showNotification('Authentication required. Please log in again.', 'error');
        break;
      case 403:
        this.showNotification('Access denied. You don\'t have permission to perform this action.', 'error');
        break;
      case 404:
        this.showNotification('Resource not found.', 'error');
        break;
      case 429:
        this.showNotification('Too many requests. Please try again later.', 'warning');
        break;
      case 500:
        this.showNotification('Server error. Please try again later.', 'error');
        break;
      default:
        this.showNotification(message || 'An unexpected error occurred.', 'error');
    }
  }

  private showNotification(message: string, type: 'error' | 'warning' | 'info') {
    // Implementation depends on your notification system
    console.log(`${type.toUpperCase()}: ${message}`);
  }
}

export const errorHandler = new ErrorHandler();
```

### 7. API Types
```typescript
// types/api.ts
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

export interface ApiError {
  message: string;
  code: string;
  details?: any;
}

// types/transaction.ts
export interface Transaction {
  id: string;
  userId: string;
  amount: number;
  currency: string;
  description: string;
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'cancelled' | 'refunded';
  type: 'payment' | 'refund' | 'transfer' | 'withdrawal';
  paymentMethod: string;
  createdAt: string;
  updatedAt: string;
  metadata?: {
    reference?: string;
    category?: string;
    tags?: string[];
  };
}

export interface TransactionFilters {
  status?: string;
  type?: string;
  paymentMethod?: string;
  amountMin?: number;
  amountMax?: number;
  dateFrom?: string;
  dateTo?: string;
  search?: string;
}

export interface TransactionResponse {
  data: Transaction[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}
```

## Критерии приемки

### 1. API Integration
- [ ] Все endpoints интегрированы
- [ ] Error handling работает
- [ ] Authentication функционирует
- [ ] Request/response interceptors активны
- [ ] Retry logic работает

### 2. Performance
- [ ] Response time < 500ms
- [ ] Caching работает корректно
- [ ] Memory usage оптимизирован
- [ ] Bundle size оптимизирован
- [ ] Network requests минимизированы

### 3. Reliability
- [ ] Offline support работает
- [ ] Error recovery функционирует
- [ ] Retry mechanisms активны
- [ ] Timeout handling работает
- [ ] Connection pooling настроен

### 4. Security
- [ ] XSS protection активна
- [ ] CSRF protection работает
- [ ] Input validation функционирует
- [ ] Secure token storage
- [ ] HTTPS enforced

### 5. Testing
- [ ] Unit tests покрывают 90%+ кода
- [ ] Integration tests проходят
- [ ] API tests работают
- [ ] Error scenarios протестированы
- [ ] Performance tests пройдены

## Риски и митигация

### Риски
1. **API downtime**
   - Митигация: Retry mechanisms, fallback strategies, offline support

2. **Network latency**
   - Митигация: Caching, request optimization, CDN

3. **Data inconsistency**
   - Митигация: Real-time updates, cache invalidation, optimistic updates

## Deliverables

1. **API Integration**
   - API client
   - Service layer
   - Custom hooks
   - Error handling

2. **Caching System**
   - Cache service
   - Cache strategies
   - Invalidation logic
   - Performance optimization

3. **Testing Suite**
   - Unit tests
   - Integration tests
   - API tests
   - Error scenario tests

4. **Documentation**
   - API documentation
   - Integration guide
   - Error handling guide
   - Performance guide

## Временные рамки

- **День 1:** API client, service layer, basic integration
- **День 2:** Caching system, error handling, retry logic
- **День 3:** Testing, optimization, documentation
