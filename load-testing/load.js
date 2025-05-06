import http from 'k6/http';
import { check, group, sleep } from 'k6';

// Configuration options
export const target = 10; // Number of virtual users
export const options = {
  stages: [
    { duration: '30s', target: target }, // Ramp-up from 0 to target users
    { duration: '5m', target: target },  // Stay at target users for 5 minutes
    { duration: '30s', target: 0 },      // Ramp-down to 0 users
  ],
  thresholds: {
    'http_req_duration': ['p(99)<2000'], // 99% of requests must complete below 2s
    'http_req_failed': ['rate<0.01'],    // Less than 1% of requests can fail
  },
};

// Fixed texts used for 95% of requests (to test caching)
const fixed = [
  "I love you!",
  "I hate you!",
  "I am a Kubernetes Cluster!"
];

// Random texts used for 5% of requests (to test model performance)
const random_texts = [
  "I love you!",
  "I hate you!",
  "I am a Kubernetes Cluster!",
  "I ran to the store",
  "The students are very good in this class",
  "Working on Saturday morning is brutal",
  "How much wood could a wood chuck chuck if a wood chuck could chuck wood?",
  "A Wood chuck would chuck as much wood as a wood chuck could chuck if a wood chuck could chuck wood",
  "Food is very tasty",
  "Welcome to the thunderdome",
  "This product exceeded my expectations",
  "Customer service was terrible",
  "I'm feeling neutral about this experience",
  "The quality is outstanding",
  "I would not recommend this to anyone",
  "Best purchase I've made this year",
  "Complete waste of money",
  "It works exactly as advertised",
  "I had a problem with the delivery",
  "The interface is intuitive and user-friendly"
];

// Generate payload based on cache rate
const generatePayload = (cacheRate = 0.95) => {
  const rand = Math.random();
  let text;
  
  if (rand > cacheRate) {
    // For 5% of requests, use random texts
    text = random_texts
      .map(value => ({ value, sort: Math.random() }))
      .sort((a, b) => a.sort - b.sort)
      .slice(0, 3) // Take 3 random texts
      .map(({ value }) => value);
  } else {
    // For 95% of requests, use fixed texts (to benefit from caching)
    text = fixed;
  }
  
  return { text };
};

// Get base URL from environment or use default
const BASE_URL = __ENV.API_URL || 'http://localhost:8000';
const CACHE_RATE = 0.95;

// Main test function
export default () => {
  const payload = JSON.stringify(generatePayload(CACHE_RATE));
  
  group('Sentiment Analysis API', () => {
    // Test prediction endpoint
    const predictResponse = http.post(
      `${BASE_URL}/api/bulk-predict`,
      payload,
      {
        headers: { 'Content-Type': 'application/json' }
      }
    );
    
    // Check if request was successful
    check(predictResponse, {
      'predict status is 200': (r) => r.status === 200,
      'predict response has predictions': (r) => JSON.parse(r.body).predictions !== undefined,
      'predict response has correct format': (r) => {
        const body = JSON.parse(r.body);
        return Array.isArray(body.predictions) && 
               Array.isArray(body.predictions[0]) &&
               typeof body.predictions[0][0].label === 'string' &&
               typeof body.predictions[0][0].score === 'number';
      }
    });
    
    // Test health endpoint
    const healthResponse = http.get(`${BASE_URL}/api/health`);
    
    check(healthResponse, {
      'health status is 200': (r) => r.status === 200,
      'health response shows healthy': (r) => JSON.parse(r.body).status === 'healthy'
    });
  });
  
  // Add a small sleep between iterations to make the test more realistic
  sleep(0.5);
};