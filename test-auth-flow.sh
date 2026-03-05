#!/bin/bash

API_URL="http://localhost:8000"

echo "===== REGISTER USER ====="

curl -s -X POST $API_URL/auth/register \
-H "Content-Type: application/json" \
-d '{"username":"testuser","email":"test@example.com","password":"Test@123"}'

echo ""
echo "===== LOGIN USER ====="

LOGIN_RESPONSE=$(curl -s -X POST $API_URL/auth/login \
-H "Content-Type: application/json" \
-d '{"email":"test@example.com","password":"Test@123"}')

echo $LOGIN_RESPONSE

ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')
REFRESH_TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.refresh_token')

echo ""
echo "ACCESS TOKEN:"
echo $ACCESS_TOKEN

echo ""
echo "REFRESH TOKEN:"
echo $REFRESH_TOKEN

echo ""
echo "===== ACCESS PROFILE ====="

curl -s $API_URL/auth/profile \
-H "Authorization: Bearer $ACCESS_TOKEN"

echo ""
echo ""
echo "===== REFRESH TOKEN ====="

curl -s -X POST "$API_URL/auth/refresh?refresh_token=$REFRESH_TOKEN"

echo ""
echo ""
echo "===== LOGOUT ====="

curl -s -X POST "$API_URL/auth/logout?refresh_token=$REFRESH_TOKEN"

echo ""
echo "===== FLOW COMPLETE ====="