#!/bin/bash

# Remove existing zip files
echo "Cleaning up old packages..."
rm -rf ./package/*.zip

# Create layer/python directory if it doesn't exist
echo "Creating layer/python directory..."
mkdir -p layer/python

# Install Python packages for the Lambda layer
echo "Installing Python dependencies..."
pip3 install --platform manylinux2014_x86_64 --only-binary=:all: -r requirements.txt -t ./layer/python

# Package the layer into a ZIP file
echo "Packaging the Lambda layer..."
cd layer
zip -r ../package/lambda_layer.zip .
cd ..

# Package the Lambda function into a ZIP file
echo "Packaging the Lambda function..."
cd function/
zip -r ../package/lambda_transform.zip .
cd ..

echo "Build complete. Packages are in the ./package directory."
