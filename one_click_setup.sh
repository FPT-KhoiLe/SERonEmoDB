#!/usr/bin/env bash
set -euo pipefail

# Thiết lập nhanh cho dự án
# 1. Tạo Conda environment
# 2. Cài package dưới dạng editable
# 3. Chạy pytest để kiểm tra

# Khởi tạo conda trong script để cho phép `conda activate`
eval "$(conda shell.bash hook)"

echo "🌱 Creating Conda environment..."
conda env create -f environment.yml

echo "🔄 Activating environment 'seronemodb'..."
conda activate seronemodb

echo "📦 Installing project in editable mode..."
pip install -e .

echo "🧪 Running pytest..."
pytest

echo "✅ Setup completed!"