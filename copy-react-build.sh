#!/bin/bash

# Define the paths
REACT_APP_DIR=./frontend
DJANGO_STATIC_DIR=./freshlyapp/static
DJANGO_MEDIA_DIR=./freshlyapp/media
DJANGO_TEMPLATES_DIR=./freshlyapp/templates

# Build the React app
echo "Building the React app..."
npm run --prefix $REACT_APP_DIR build

# Ensure the target directories exist
if [ ! -d "$DJANGO_STATIC_DIR" ]; then
  echo "Creating static directory..."
  mkdir -p $DJANGO_STATIC_DIR
fi

if [ ! -d "$DJANGO_MEDIA_DIR" ]; then
  echo "Creating media directory..."
  mkdir -p $DJANGO_MEDIA_DIR
fi

# if [ ! -d "$DJANGO_TEMPLATES_DIR" ]; then
#   echo "Creating templates directory..."
#   mkdir -p $DJANGO_TEMPLATES_DIR
# fi

# Copy static files (CSS, JS)
echo "Copying static files..."
cp -r $REACT_APP_DIR/build/static/* $DJANGO_STATIC_DIR/

# Copy media files
echo "Copying media files..."
cp -r $REACT_APP_DIR/public/static/media/* $DJANGO_MEDIA_DIR/

# Copy index.html to templates directory
echo "Copying index.html to templates directory..."
cp $REACT_APP_DIR/build/index.html $DJANGO_TEMPLATES_DIR/

echo "React build files have been copied to the Django directories."

#!/bin/bash

# Define the paths
REACT_APP_DIR=./frontend
DJANGO_STATIC_DIR=./freshlyapp/static
DJANGO_MEDIA_DIR=./freshlyapp/media
DJANGO_TEMPLATES_DIR=./freshlyapp/templates

# Build the React app
echo "Building the React app..."
npm run --prefix $REACT_APP_DIR build

# Ensure the target directories exist
if [ ! -d "$DJANGO_STATIC_DIR" ]; then
  echo "Creating static directory..."
  mkdir -p $DJANGO_STATIC_DIR
fi

if [ ! -d "$DJANGO_MEDIA_DIR" ]; then
  echo "Creating media directory..."
  mkdir -p $DJANGO_MEDIA_DIR
fi

# if [ ! -d "$DJANGO_TEMPLATES_DIR" ]; then
#   echo "Creating templates directory..."
#   mkdir -p $DJANGO_TEMPLATES_DIR
# fi

# Copy static files (CSS, JS)
echo "Copying static files..."
cp -r $REACT_APP_DIR/build/static/* $DJANGO_STATIC_DIR/

# Copy media files
echo "Copying media files..."
cp -r $REACT_APP_DIR/public/static/media/* $DJANGO_MEDIA_DIR/

# Copy index.html to templates directory
echo "Copying index.html to templates directory..."
cp $REACT_APP_DIR/build/index.html $DJANGO_TEMPLATES_DIR/

echo "React build files have been copied to the Django directories."
