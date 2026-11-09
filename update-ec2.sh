#!/usr/bin/env bash
# ==============================================================================
# Student Document System - Quick Update Script for EC2
# ==============================================================================

set -e

echo "🔄 Pulling latest code..."
git pull origin main || git pull

echo "🏗️ Rebuilding and restarting containers..."
sudo docker compose -f docker-compose.yml --env-file .env.production up -d --build

echo "🧹 Cleaning up old Docker images..."
sudo docker image prune -f

echo "✅ Update complete!"
sudo docker compose ps

