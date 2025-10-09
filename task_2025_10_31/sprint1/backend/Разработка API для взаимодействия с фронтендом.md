# Техническое задание: Разработка API для взаимодействия с фронтендом

## Общая информация
- **Приоритет:** major
- **Оценка:** 3 SP
- **Исполнитель:** backend
- **Срок выполнения:** 3 дня

## Цель
Создать RESTful API для обеспечения связи между фронтендом и бэкендом, включая аутентификацию, управление пользователями, обработку платежей и интеграцию с блокчейном.

## Требования

### Функциональные требования
1. **Authentication API:** JWT-based аутентификация
2. **User Management API:** CRUD операции с пользователями
3. **Payment API:** Обработка платежей
4. **Blockchain API:** Интеграция с смарт-контрактами
5. **Notification API:** Отправка уведомлений

### Нефункциональные требования
1. **Performance:** Время отклика < 200ms
2. **Scalability:** Поддержка до 10,000 одновременных пользователей
3. **Security:** HTTPS, JWT, rate limiting
4. **Documentation:** OpenAPI/Swagger документация
5. **Testing:** 90%+ покрытие тестами

## Архитектура API

### 1. API Gateway
```javascript
// Express.js API Gateway
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

const app = express();

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.FRONTEND_URL,
  credentials: true
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use('/api/', limiter);

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/payments', paymentRoutes);
app.use('/api/blockchain', blockchainRoutes);
app.use('/api/notifications', notificationRoutes);
```

### 2. Authentication Service
```javascript
// JWT Authentication
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

class AuthService {
  async login(email, password) {
    const user = await User.findOne({ email });
    if (!user) throw new Error('User not found');
    
    const isValidPassword = await bcrypt.compare(password, user.password);
    if (!isValidPassword) throw new Error('Invalid password');
    
    const accessToken = jwt.sign(
      { userId: user.id, email: user.email },
      process.env.JWT_SECRET,
      { expiresIn: '15m' }
    );
    
    const refreshToken = jwt.sign(
      { userId: user.id },
      process.env.JWT_REFRESH_SECRET,
      { expiresIn: '7d' }
    );
    
    return { accessToken, refreshToken, user: this.sanitizeUser(user) };
  }
  
  async refreshToken(refreshToken) {
    const decoded = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET);
    const user = await User.findById(decoded.userId);
    
    if (!user) throw new Error('User not found');
    
    const newAccessToken = jwt.sign(
      { userId: user.id, email: user.email },
      process.env.JWT_SECRET,
      { expiresIn: '15m' }
    );
    
    return { accessToken: newAccessToken };
  }
  
  sanitizeUser(user) {
    const { password, ...sanitized } = user.toObject();
    return sanitized;
  }
}
```

### 3. User Management API
```javascript
// User Controller
class UserController {
  async getProfile(req, res) {
    try {
      const user = await User.findById(req.userId);
      if (!user) return res.status(404).json({ error: 'User not found' });
      
      res.json(this.sanitizeUser(user));
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
  
  async updateProfile(req, res) {
    try {
      const { firstName, lastName, email } = req.body;
      
      const user = await User.findByIdAndUpdate(
        req.userId,
        { firstName, lastName, email },
        { new: true, runValidators: true }
      );
      
      res.json(this.sanitizeUser(user));
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
  
  async changePassword(req, res) {
    try {
      const { currentPassword, newPassword } = req.body;
      
      const user = await User.findById(req.userId);
      const isValidPassword = await bcrypt.compare(currentPassword, user.password);
      
      if (!isValidPassword) {
        return res.status(400).json({ error: 'Current password is incorrect' });
      }
      
      const hashedPassword = await bcrypt.hash(newPassword, 12);
      await User.findByIdAndUpdate(req.userId, { password: hashedPassword });
      
      res.json({ message: 'Password updated successfully' });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
}
```

### 4. Payment Processing API
```javascript
// Payment Controller
class PaymentController {
  async processPayment(req, res) {
    try {
      const { amount, currency, paymentMethod, description } = req.body;
      
      // Validate payment data
      const validation = this.validatePaymentData({
        amount, currency, paymentMethod, description
      });
      
      if (!validation.isValid) {
        return res.status(400).json({ error: validation.errors });
      }
      
      // Create payment record
      const payment = new Payment({
        userId: req.userId,
        amount,
        currency,
        paymentMethod,
        description,
        status: 'pending'
      });
      
      await payment.save();
      
      // Process payment based on method
      let result;
      switch (paymentMethod) {
        case 'card':
          result = await this.processCardPayment(payment);
          break;
        case 'crypto':
          result = await this.processCryptoPayment(payment);
          break;
        default:
          throw new Error('Unsupported payment method');
      }
      
      // Update payment status
      payment.status = result.success ? 'completed' : 'failed';
      payment.transactionId = result.transactionId;
      await payment.save();
      
      res.json({
        paymentId: payment._id,
        status: payment.status,
        transactionId: payment.transactionId
      });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
  
  async getPaymentHistory(req, res) {
    try {
      const { page = 1, limit = 10, status } = req.query;
      
      const filter = { userId: req.userId };
      if (status) filter.status = status;
      
      const payments = await Payment.find(filter)
        .sort({ createdAt: -1 })
        .limit(limit * 1)
        .skip((page - 1) * limit);
      
      const total = await Payment.countDocuments(filter);
      
      res.json({
        payments,
        pagination: {
          page: parseInt(page),
          limit: parseInt(limit),
          total,
          pages: Math.ceil(total / limit)
        }
      });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
}
```

### 5. Blockchain Integration API
```javascript
// Blockchain Controller
const { ethers } = require('ethers');

class BlockchainController {
  constructor() {
    this.provider = new ethers.providers.JsonRpcProvider(process.env.ETHEREUM_RPC_URL);
    this.wallet = new ethers.Wallet(process.env.PRIVATE_KEY, this.provider);
    this.contract = new ethers.Contract(
      process.env.CONTRACT_ADDRESS,
      contractABI,
      this.wallet
    );
  }
  
  async getBalance(req, res) {
    try {
      const { address } = req.params;
      
      // Validate Ethereum address
      if (!ethers.utils.isAddress(address)) {
        return res.status(400).json({ error: 'Invalid Ethereum address' });
      }
      
      const balance = await this.contract.getBalance(address);
      
      res.json({
        address,
        balance: ethers.utils.formatEther(balance),
        balanceWei: balance.toString()
      });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
  
  async processBlockchainPayment(req, res) {
    try {
      const { to, amount, description } = req.body;
      
      // Validate inputs
      if (!ethers.utils.isAddress(to)) {
        return res.status(400).json({ error: 'Invalid recipient address' });
      }
      
      const amountWei = ethers.utils.parseEther(amount.toString());
      
      // Call smart contract
      const tx = await this.contract.processPayment(
        to,
        amountWei,
        description,
        { gasLimit: 100000 }
      );
      
      // Wait for transaction confirmation
      const receipt = await tx.wait();
      
      res.json({
        transactionHash: tx.hash,
        blockNumber: receipt.blockNumber,
        gasUsed: receipt.gasUsed.toString(),
        status: receipt.status
      });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
  
  async getTransactionHistory(req, res) {
    try {
      const { address } = req.params;
      const { page = 1, limit = 10 } = req.query;
      
      // Get transactions from blockchain
      const filter = this.contract.filters.PaymentProcessed(address);
      const events = await this.contract.queryFilter(filter);
      
      // Paginate results
      const startIndex = (page - 1) * limit;
      const endIndex = startIndex + parseInt(limit);
      const paginatedEvents = events.slice(startIndex, endIndex);
      
      const transactions = paginatedEvents.map(event => ({
        transactionHash: event.transactionHash,
        blockNumber: event.blockNumber,
        from: event.args.from,
        to: event.args.to,
        amount: ethers.utils.formatEther(event.args.amount),
        timestamp: new Date(event.args.timestamp * 1000)
      }));
      
      res.json({
        transactions,
        pagination: {
          page: parseInt(page),
          limit: parseInt(limit),
          total: events.length,
          pages: Math.ceil(events.length / limit)
        }
      });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
}
```

## API Endpoints

### 1. Authentication Endpoints
```yaml
POST /api/auth/register
  description: Register new user
  requestBody:
    email: string
    password: string
    firstName: string
    lastName: string
  response:
    accessToken: string
    refreshToken: string
    user: object

POST /api/auth/login
  description: User login
  requestBody:
    email: string
    password: string
  response:
    accessToken: string
    refreshToken: string
    user: object

POST /api/auth/refresh
  description: Refresh access token
  requestBody:
    refreshToken: string
  response:
    accessToken: string

POST /api/auth/logout
  description: User logout
  headers:
    Authorization: Bearer <token>
  response:
    message: string
```

### 2. User Management Endpoints
```yaml
GET /api/users/profile
  description: Get user profile
  headers:
    Authorization: Bearer <token>
  response:
    id: string
    email: string
    firstName: string
    lastName: string
    createdAt: string

PUT /api/users/profile
  description: Update user profile
  headers:
    Authorization: Bearer <token>
  requestBody:
    firstName: string
    lastName: string
    email: string
  response:
    user: object

POST /api/users/change-password
  description: Change user password
  headers:
    Authorization: Bearer <token>
  requestBody:
    currentPassword: string
    newPassword: string
  response:
    message: string
```

### 3. Payment Endpoints
```yaml
POST /api/payments/process
  description: Process payment
  headers:
    Authorization: Bearer <token>
  requestBody:
    amount: number
    currency: string
    paymentMethod: string
    description: string
  response:
    paymentId: string
    status: string
    transactionId: string

GET /api/payments/history
  description: Get payment history
  headers:
    Authorization: Bearer <token>
  query:
    page: number
    limit: number
    status: string
  response:
    payments: array
    pagination: object

GET /api/payments/{paymentId}
  description: Get payment details
  headers:
    Authorization: Bearer <token>
  response:
    payment: object
```

### 4. Blockchain Endpoints
```yaml
GET /api/blockchain/balance/{address}
  description: Get blockchain balance
  headers:
    Authorization: Bearer <token>
  response:
    address: string
    balance: string
    balanceWei: string

POST /api/blockchain/payment
  description: Process blockchain payment
  headers:
    Authorization: Bearer <token>
  requestBody:
    to: string
    amount: string
    description: string
  response:
    transactionHash: string
    blockNumber: number
    gasUsed: string
    status: number

GET /api/blockchain/transactions/{address}
  description: Get transaction history
  headers:
    Authorization: Bearer <token>
  query:
    page: number
    limit: number
  response:
    transactions: array
    pagination: object
```

## Middleware

### 1. Authentication Middleware
```javascript
const jwt = require('jsonwebtoken');

const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }
  
  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid or expired token' });
    }
    
    req.userId = user.userId;
    req.userEmail = user.email;
    next();
  });
};
```

### 2. Validation Middleware
```javascript
const { body, validationResult } = require('express-validator');

const validatePayment = [
  body('amount').isNumeric().withMessage('Amount must be a number'),
  body('currency').isLength({ min: 3, max: 3 }).withMessage('Currency must be 3 characters'),
  body('paymentMethod').isIn(['card', 'crypto']).withMessage('Invalid payment method'),
  body('description').isLength({ min: 1, max: 255 }).withMessage('Description required'),
  
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    next();
  }
];
```

### 3. Error Handling Middleware
```javascript
const errorHandler = (err, req, res, next) => {
  console.error(err.stack);
  
  if (err.name === 'ValidationError') {
    return res.status(400).json({
      error: 'Validation Error',
      details: err.message
    });
  }
  
  if (err.name === 'CastError') {
    return res.status(400).json({
      error: 'Invalid ID format'
    });
  }
  
  if (err.code === 11000) {
    return res.status(400).json({
      error: 'Duplicate field value'
    });
  }
  
  res.status(500).json({
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
  });
};
```

## Database Models

### 1. User Model
```javascript
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true
  },
  password: {
    type: String,
    required: true,
    minlength: 6
  },
  firstName: {
    type: String,
    required: true,
    trim: true
  },
  lastName: {
    type: String,
    required: true,
    trim: true
  },
  isActive: {
    type: Boolean,
    default: true
  },
  lastLogin: {
    type: Date
  }
}, {
  timestamps: true
});

// Hash password before saving
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

// Compare password method
userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', userSchema);
```

### 2. Payment Model
```javascript
const paymentSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  amount: {
    type: Number,
    required: true,
    min: 0
  },
  currency: {
    type: String,
    required: true,
    default: 'USD'
  },
  paymentMethod: {
    type: String,
    required: true,
    enum: ['card', 'crypto', 'bank_transfer']
  },
  description: {
    type: String,
    required: true
  },
  status: {
    type: String,
    required: true,
    enum: ['pending', 'processing', 'completed', 'failed', 'cancelled'],
    default: 'pending'
  },
  transactionId: {
    type: String
  },
  blockchainHash: {
    type: String
  },
  metadata: {
    type: mongoose.Schema.Types.Mixed
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Payment', paymentSchema);
```

## Testing

### 1. Unit Tests
```javascript
const request = require('supertest');
const app = require('../app');
const User = require('../models/User');

describe('Authentication API', () => {
  beforeEach(async () => {
    await User.deleteMany({});
  });
  
  describe('POST /api/auth/register', () => {
    it('should register a new user', async () => {
      const userData = {
        email: 'test@example.com',
        password: 'password123',
        firstName: 'John',
        lastName: 'Doe'
      };
      
      const response = await request(app)
        .post('/api/auth/register')
        .send(userData)
        .expect(201);
      
      expect(response.body).toHaveProperty('accessToken');
      expect(response.body).toHaveProperty('refreshToken');
      expect(response.body.user.email).toBe(userData.email);
    });
    
    it('should not register user with existing email', async () => {
      const userData = {
        email: 'test@example.com',
        password: 'password123',
        firstName: 'John',
        lastName: 'Doe'
      };
      
      // Create first user
      await request(app)
        .post('/api/auth/register')
        .send(userData);
      
      // Try to create second user with same email
      const response = await request(app)
        .post('/api/auth/register')
        .send(userData)
        .expect(400);
      
      expect(response.body.error).toContain('duplicate');
    });
  });
  
  describe('POST /api/auth/login', () => {
    beforeEach(async () => {
      const userData = {
        email: 'test@example.com',
        password: 'password123',
        firstName: 'John',
        lastName: 'Doe'
      };
      
      await request(app)
        .post('/api/auth/register')
        .send(userData);
    });
    
    it('should login with valid credentials', async () => {
      const loginData = {
        email: 'test@example.com',
        password: 'password123'
      };
      
      const response = await request(app)
        .post('/api/auth/login')
        .send(loginData)
        .expect(200);
      
      expect(response.body).toHaveProperty('accessToken');
      expect(response.body).toHaveProperty('refreshToken');
    });
    
    it('should not login with invalid credentials', async () => {
      const loginData = {
        email: 'test@example.com',
        password: 'wrongpassword'
      };
      
      const response = await request(app)
        .post('/api/auth/login')
        .send(loginData)
        .expect(401);
      
      expect(response.body.error).toContain('Invalid password');
    });
  });
});
```

### 2. Integration Tests
```javascript
describe('Payment API Integration', () => {
  let authToken;
  let userId;
  
  beforeEach(async () => {
    // Create test user and get auth token
    const userData = {
      email: 'test@example.com',
      password: 'password123',
      firstName: 'John',
      lastName: 'Doe'
    };
    
    const registerResponse = await request(app)
      .post('/api/auth/register')
      .send(userData);
    
    authToken = registerResponse.body.accessToken;
    userId = registerResponse.body.user.id;
  });
  
  describe('POST /api/payments/process', () => {
    it('should process payment successfully', async () => {
      const paymentData = {
        amount: 100.50,
        currency: 'USD',
        paymentMethod: 'card',
        description: 'Test payment'
      };
      
      const response = await request(app)
        .post('/api/payments/process')
        .set('Authorization', `Bearer ${authToken}`)
        .send(paymentData)
        .expect(200);
      
      expect(response.body).toHaveProperty('paymentId');
      expect(response.body).toHaveProperty('status');
      expect(response.body.status).toBe('completed');
    });
  });
});
```

## Критерии приемки

### 1. API Functionality
- [ ] Все endpoints работают корректно
- [ ] Authentication функционирует
- [ ] User management работает
- [ ] Payment processing активен
- [ ] Blockchain integration работает

### 2. Security
- [ ] JWT authentication работает
- [ ] Rate limiting активен
- [ ] Input validation работает
- [ ] CORS настроен корректно
- [ ] HTTPS enforced

### 3. Performance
- [ ] Response time < 200ms
- [ ] Handles 1000+ concurrent requests
- [ ] Database queries оптимизированы
- [ ] Caching implemented
- [ ] Error handling работает

### 4. Testing
- [ ] Unit tests покрывают 90%+ кода
- [ ] Integration tests проходят
- [ ] API tests работают
- [ ] Load tests пройдены
- [ ] Security tests пройдены

## Риски и митигация

### Риски
1. **API performance issues**
   - Митигация: Load testing, caching, optimization

2. **Security vulnerabilities**
   - Митигация: Security testing, input validation, authentication

3. **Database bottlenecks**
   - Митигация: Query optimization, indexing, connection pooling

## Deliverables

1. **API Implementation**
   - Express.js server
   - All endpoints implemented
   - Middleware configured
   - Database models

2. **Testing Suite**
   - Unit tests
   - Integration tests
   - API tests
   - Load tests

3. **Documentation**
   - OpenAPI specification
   - API documentation
   - Deployment guide
   - Testing guide

## Временные рамки

- **День 1:** API structure, authentication, user management
- **День 2:** Payment processing, blockchain integration
- **День 3:** Testing, documentation, deployment
